FROM registry.fedoraproject.org/fedora:39

ARG AUTOPACK_HOME=/opt/autopack
ARG AUTOPACK_DATA_DIR=${AUTOPACK_HOME}/data

RUN dnf install -y wget xz

RUN mkdir -p ${AUTOPACK_DATA_DIR}

RUN wget \
-O ${AUTOPACK_DATA_DIR}/rpm-specs-latest.tar.xz  \
https://src.stg.fedoraproject.org/lookaside/rpm-specs-latest.tar.xz

RUN (cd ${AUTOPACK_DATA_DIR}; tar -xvpf rpm-specs-latest.tar.xz; rm rpm-specs-latest.tar.xz)
