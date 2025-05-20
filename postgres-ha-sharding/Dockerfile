ARG PG_VERSION=17.4

FROM postgres:${PG_VERSION}

ARG CITUS_VERSION=13.0.3
ENV PG_MAJOR=${PG_VERSION%%.*}

RUN set -ex \
    && export DEBIAN_FRONTEND=noninteractive \
    && echo 'APT::Install-Recommends "0";\nAPT::Install-Suggests "0";' > /etc/apt/apt.conf.d/01norecommend \
    && apt-get update -y \
    && apt-get install -y curl jq less python3-pip python3-venv \
    && apt-get install -y postgresql-server-dev-$PG_MAJOR \
          git gcc make autoconf \
          libc6-dev flex libcurl4-gnutls-dev \
          libicu-dev libkrb5-dev liblz4-dev \
          libpam0g-dev libreadline-dev libselinux1-dev \
          libssl-dev libxslt1-dev libzstd-dev uuid-dev \
    && git clone --depth 1 -b "v$CITUS_VERSION" https://github.com/citusdata/citus.git \
    && MAKEFLAGS="-j $(grep -c ^processor /proc/cpuinfo)" \
    && cd citus && ./configure && make install && cd ../ && rm -rf /citus \
    && python3 -m venv /opt/patroni && /opt/patroni/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/patroni/bin/pip install --no-cache-dir patroni[psycopg3,etcd3] \
    && ln -s /opt/patroni/bin/patroni /usr/local/bin/patroni \
    && ln -s /opt/patroni/bin/patronictl /usr/local/bin/patronictl \
    # Clean up
    && apt-get purge -y --allow-remove-essential \
          postgresql-server-dev-$PG_MAJOR git gcc make autoconf \
          libc6-dev flex libicu-dev libkrb5-dev liblz4-dev \
          libpam0g-dev libreadline-dev libselinux1-dev libssl-dev libxslt1-dev libzstd-dev uuid-dev \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* /root/.cache

# Expose the ports for PostgreSQL and Patroni
EXPOSE 5432 8008

COPY run.sh /
RUN chmod +x /run.sh \
    && chown postgres:postgres /run.sh \
    && chown -R postgres:postgres /opt/patroni

USER postgres

CMD ["/bin/bash", "/run.sh"]