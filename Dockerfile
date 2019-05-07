# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Define whether we're building a production or a development image. This will
# generally be used to control whether or not we install our development and
# test dependencies.
ARG DEVEL=no

# Install production dependencies.
RUN pip install \
  -r requirements/main.txt \
  -r requirements/deploy.txt \
  $(if [ "$DEVEL" = "yes" ]; then echo '-r requirements/dev.txt'; fi)
