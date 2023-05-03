from oarepo/oarepo-base-development:11

# repository is mounted at /repository

# site name is at REPOSITORY_SITE_NAME environment variable
# invenio instance path is at INVENIO_INSTANCE_PATH

ARG REPOSITORY_SITE_NAME

ENV INVENIO_INSTANCE_PATH=/invenio
ENV INVENIO_VENV=/invenio-venv

RUN mkdir ${INVENIO_INSTANCE_PATH}

RUN python -m venv --system-site-packages ${INVENIO_VENV}
RUN ${INVENIO_VENV}/bin/pip install -U pip setuptools wheel

COPY sites/${REPOSITORY_SITE_NAME}/requirements.txt ${INVENIO_VENV}/requirements-orig.txt
COPY sites/${REPOSITORY_SITE_NAME}/invenio.cfg ${INVENIO_INSTANCE_PATH}

RUN cat ${INVENIO_VENV}/requirements-orig.txt | \
    egrep -iv '^-e |^cffi=|^cairocffi=|^uwsgi=|^packaging=|^pip=|^setuptools=|^pyparsing=|^xcffib=' \
    >${INVENIO_VENV}/requirements.txt
RUN cat ${INVENIO_VENV}/requirements-orig.txt | \
    grep -i '^-e ' | \
    sed 's#^-e ./../../#-e /repository/#' \
    >${INVENIO_VENV}/requirements-editable.txt

RUN ${INVENIO_VENV}/bin/pip install -r ${INVENIO_VENV}/requirements.txt --no-deps

RUN ${INVENIO_VENV}/bin/pip check || echo "check failed. cairocffi and pypackaging should be expected"

RUN python -m venv /nrp-cli
RUN /nrp-cli/bin/pip install 'oarepo-cli>=11.0.0,<12'
ENV NRP_CLI=/nrp-cli/bin/nrp-cli

WORKDIR /repository/sites/${REPOSITORY_SITE_NAME}

RUN apk add git

EXPOSE 5000

# nrp-cli development only
# RUN echo "cat ${INVENIO_VENV}/requirements-editable.txt; if [ -d /nrp-cli-sources ] ; then /nrp-cli/bin/pip uninstall -y oarepo-cli; /nrp-cli/bin/pip install -e /nrp-cli-sources; fi; /nrp-cli/bin/nrp-cli \$@" > /tmp/nrp-cli-command
# CMD /bin/sh /tmp/nrp-cli-command docker-develop \
#     --virtualenv ${INVENIO_VENV} \
#     --invenio ${INVENIO_INSTANCE_PATH}
# CMD /bin/sh -c 'while true ; do sleep 3600; done'


# without nrp-cli development
CMD $NRP_CLI docker-develop \
    --virtualenv ${INVENIO_VENV} \
    --invenio ${INVENIO_INSTANCE_PATH}