
FROM python:3.7.7-slim as build

# Working directory where all the setup would take place in the image
WORKDIR /brooks-insurance-api

# Install packages needed for the provisioning of the instance with python
# and other packages

RUN pip install --upgrade pip

COPY ./Pipfile /brooks-insurance-api
COPY ./Pipfile.lock /brooks-insurance-api

RUN pip install --user pipenv
RUN python3 -m pipenv install

FROM python:3.7.7-slim as app

# Working directory where all the setup would take place in the image
WORKDIR /brooks-insurance-api

# The default user that should be used
ARG USER_ID=1000
ARG GROUP_ID=1000

ARG APP_USER=appuser

# Create user and group
RUN groupadd -g ${GROUP_ID} ${APP_USER} && useradd -u ${USER_ID} -g ${APP_USER} -s /bin/sh ${APP_USER}

# Install ca certificates
RUN apt-get update \
    && apt-get install ca-certificates -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /root/ /root/
RUN chown -R ${APP_USER}:${APP_USER} /root
RUN chmod 755 /root

COPY . .
# COPY --chown=${APP_USER}:${APP_USER} . .

RUN chown -R ${APP_USER}:${APP_USER} /brooks-insurance-api
RUN chmod 755 /brooks-insurance-api

# Sert the default user
USER ${APP_USER}

RUN mkdir -p app/static

CMD ["/bin/bash", "-c", "/brooks-insurance-api/docker/start_api.sh"]
