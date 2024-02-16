FROM registry.fedoraproject.org/fedora:39

ARG AUTOPACK_HOME=/opt/autopack
ARG AUTOPACK_DATA_DIR=${AUTOPACK_HOME}/data

RUN dnf install -y wget xz python3-click nginx

RUN mkdir -p ${AUTOPACK_DATA_DIR} && \
chown -R 1001:root ${AUTOPACK_DATA_DIR} && \
chown -R 1001:root /var/log/nginx && \
chmod -R 770 /var/log/nginx

RUN wget \
-O ${AUTOPACK_DATA_DIR}/rpm-specs-latest.tar.xz  \
https://src.stg.fedoraproject.org/lookaside/rpm-specs-latest.tar.xz

RUN (cd ${AUTOPACK_DATA_DIR}; tar -xvpf rpm-specs-latest.tar.xz; rm rpm-specs-latest.tar.xz)

COPY tools/ ${AUTOPACK_HOME}/bin/

RUN mkdir -p /opt/autopack/data/rpm-specs/cmake && \
for p in `/opt/autopack/bin/pkglist-query`;do ln -s $p /opt/autopack/data/rpm-specs/cmake/$(basename $p); done

RUN /opt/autopack/bin/pkglist-query --json > /opt/autopack/data/rpm-specs/cmake.index.json

COPY files/ /

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
