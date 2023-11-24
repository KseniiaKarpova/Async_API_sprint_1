#!/bin/sh

echo "Waiting for postgres and elastic search"
while ! (nc -z elasticsearch 9200 && nc -z postgres 5432 && nc -z cache 6379); do
  sleep 0.1
done
exec "$@"