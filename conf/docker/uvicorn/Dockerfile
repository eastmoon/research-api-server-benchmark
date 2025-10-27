# Step : base
FROM python:slim

## Update python package manager
RUN pip install --upgrade pip

# Step : Python FastAPI
## Install FastAPI
RUN pip install \
    fastapi \
    uvicorn[standard] \
    gunicorn

## Install API server
ADD ./server /usr/local/server
ADD ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +rx /docker-entrypoint.sh

## Setting container startup
WORKDIR /usr/local/server
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["apiserver"]
