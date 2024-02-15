Name: zxing-cpp
Version: 2.0.0
Release: 6%{?dist}
Summary: C++ port of the ZXing ("Zebra Crossing") barcode scanning library

# The entire source is ASL 2.0, except:
# - wrappers/wasm/base64ArrayBuffer.js is MIT (but is not used)
License: Apache-2.0 AND MIT
Url: https://github.com/nu-book/zxing-cpp
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: cmake(fmt)
# Use the system copy of pybind11 rather than trying to download a copy. This
# patch is unconditional, so it is not, as-is, suitable for sending upstream.
Patch0: zxing-cpp-1.2.0-system-pybind11.patch

%description
ZXing-C++ ("zebra crossing") is an open-source, multi-format 1D/2D barcode
image processing library implemented in C++.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n python3-%{name}
Summary:        Python bindings for the %{name} barcode library

BuildRequires: python3-devel
BuildRequires: pybind11-devel
BuildRequires: chrpath

Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
%{summary}.

%prep
%autosetup -p1

# don’t use unversioned “python” interpreter in tests
sed -r -i 's@(COMMAND )python@\1%{python3}@' wrappers/python/CMakeLists.txt
# we don’t need cmake as a python dependency
sed -r -i '/cmake/d' wrappers/python/pyproject.toml
# build verbosely:

%generate_buildrequires
pushd wrappers/python &>/dev/null
%pyproject_buildrequires -r
popd &>/dev/null

%build
# Setting BUILD_PYTHON_MODULE builds a Python extension shared library module,
# but we don’t get any metadata (dist-info), so it’s not terribly useful for
# packaging purposes. Instead, it seems we must re-build the whole library
# through setuptools to get that.
# CMAKE_BUILD_TYPE=RelWithDebInfo prevents the build from stripping the
# python module after it is built.  The stripping happens in
# pybind11_add_module.
%cmake -DBUILD_EXAMPLES=OFF -DBUILD_PYTHON_MODULE=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo
%cmake_build
pushd wrappers/python
# CMake respects this environment variable. We need to see the compiler
# invocations to verify the distro build flags are respected. Unfortunately,
# pybind11 does add -O3, and there doesn’t seem to be a way to turn that off.
# It’s a global pybind11 decision, not something in this package’s sources.
export VERBOSE=1
%pyproject_wheel
popd

%install
%cmake_install
pushd wrappers/python
%pyproject_install
# Now we do something sneaky: we substitute the Python extension that was built
# in the original CMake invocation, replacing the one built with setuptools. It
# is dynamically linked against the main libZXing.so, which makes it smaller,
# and it was not built with that pesky -O3 that was added by pybind11, so it
# better complies with packaging guidelines. The only problem is it contains an
# rpath that we need to remove.
popd
install -t '%{buildroot}%{python3_sitearch}' -p \
    %{_vpath_builddir}/wrappers/python/zxingcpp.*.so
chrpath --delete %{buildroot}%{python3_sitearch}/zxingcpp.*.so
pushd wrappers/python
%pyproject_save_files zxingcpp
popd

%check
%ctest

%files
%license LICENSE
%{_libdir}/libZXing.so.3
%{_libdir}/libZXing.so.%{version}

%files devel
%doc README.md
%{_includedir}/ZXing/
%{_libdir}/libZXing.so
%{_libdir}/cmake/ZXing/
%{_libdir}/pkgconfig/zxing.pc

%files -n python3-%{name} -f %{pyproject_files}
%{_libdir}/zxingcpp%{python3_ext_suffix}

%changelog
* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 2.0.0-4
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 2.0.0-3
- Rebuilt due to fmt 10 update.

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.12

* Fri Feb 24 2023 Caolán McNamara <caolanm@redhat.com> 2.0.0-1
- latest release
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Tom Stellard <tstellar@redhat.com> - 1.2.0-8
- Prevent stripping of python module

* Tue Aug 02 2022 Caolán McNamara <caolanm@redhat.com> 1.2.0-7
- Resolves: rhbz#2113772 FTBFS in Fedora rawhide/f37

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.2.0-5
- Rebuilt for Python 3.11

* Sat Apr 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.2.0-4
- Security fix for CVE-2022-28041

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Caolán McNamara <caolanm@redhat.com> 1.2.0-2
- build python bindings

* Fri Dec 10 2021 Caolán McNamara <caolanm@redhat.com> 1.2.0-1
- initial import
