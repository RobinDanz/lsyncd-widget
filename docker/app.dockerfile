FROM alpine:3.19

RUN apk add --no-cache lsyncd rsync bash

RUN mkdir -p /etc/lsyncd /source /target /logs

COPY docker/lsyncd.conf.lua /etc/lsyncd/
