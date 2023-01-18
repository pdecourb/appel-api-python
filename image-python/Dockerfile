FROM layer-kraft.registry.saas.cagip.group.gca/ci-tools:latest AS ci-tools
FROM docker-remote.registry.saas.cagip.group.gca/python:alpineVERSION_IMAGE
RUN apk -U --no-cache add  curl wget  nano vim arping  gnupg ca-certificates libxml2-utils bash
COPY --from=ci-tools /usr/local/share/ca-certificates /usr/local/share/ca-certificates
RUN update-ca-certificates
RUN pip3 install --upgrade pip
RUN pip3 install \
    pyyaml configparser  requests oauthlib requests_oauthlib websocket jwt  backport cachetools \
    certifi chardet  google httplib2 idna kubernetes markupsafe  oauth2client  openshift pyasn1 \
    pyasn1_modules pylint rsa six
RUN adduser -D cats
USER cats
CMD "python3"
