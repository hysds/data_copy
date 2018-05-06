FROM hysds/pge-base:latest

MAINTAINER mkarim "Mohammed.R.Karim@jpl.nasa.gov"
LABEL description="Copying data to user selected destination"

ARG id
ARG gid
#Change UID and GID from build
USER root
RUN set -ex && \
  usermod -u ${id} ops && \
  groupmod -g ${gid} ops && \
  chown -R ops:ops /home/ops/ /data && \
  usermod -g ${gid} ops

# create work directory
RUN set -ex \
 && mkdir -p /data/work \
 && chmod -R 755 /data \
 && chown -R ops:ops /data


# provision Data Move PGE
USER ops
COPY . /home/ops/verdi/ops/data_copy

# set entrypoint
WORKDIR /home/ops
CMD ["/bin/bash", "--login"]
