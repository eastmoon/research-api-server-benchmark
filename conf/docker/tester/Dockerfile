# Step : base
FROM grafana/k6

## Update tools
USER root
RUN apk add \
    bash \
    curl

## Setting container startup
WORKDIR /usr/local/test
ADD ./docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["dev"]
