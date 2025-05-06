ARG PG_VERSION=17.4

FROM postgres:${PG_VERSION}

RUN set -ex \
    && export DEBIAN_FRONTEND=noninteractive \
    && echo 'APT::Install-Recommends "0";\nAPT::Install-Suggests "0";' > /etc/apt/apt.conf.d/01norecommend \
    && apt-get update -y \
    && apt-get install -y curl jq less python3-pip python3-venv \
    && python3 -m venv /opt/patroni && /opt/patroni/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/patroni/bin/pip install --no-cache-dir patroni[psycopg3,etcd3] \
    && ln -s /opt/patroni/bin/patroni /usr/local/bin/patroni \
    && ln -s /opt/patroni/bin/patronictl /usr/local/bin/patronictl \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* /root/.cache

# Expose the ports for PostgreSQL and Patroni
EXPOSE 5432 8008

COPY entrypoint.sh /

USER postgres

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]