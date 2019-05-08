# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Define whether we're building a production or a development image. This will
# generally be used to control whether or not we install our development and
# test dependencies.
ARG DEVEL=no

# Copy local code to the container image.
WORKDIR /app

# Install System level requirements, this is done before everything else
# because these are rarely ever going to change.
RUN set -x \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        $(if [ "$DEVEL" = "yes" ]; then echo 'bash postgresql-client'; fi) \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy in requirements files
COPY ./requirements ./requirements

RUN ls

# Install production dependencies.
RUN pip install \
  -r requirements/main.txt \
  -r requirements/deploy.txt \
  $(if [ "$DEVEL" = "yes" ]; then echo '-r requirements/dev.txt'; fi)

# Copy in everything else
COPY . .
