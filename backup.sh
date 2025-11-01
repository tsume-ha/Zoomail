#!/bin/bash
set -euo pipefail

# get the current date and time
now=$(date +"%Y%m%d_%H%M")

# create zoomail_db_dump directory if it doesn't exist
mkdir -p ~/zoomail_db_dump

# dump the database
docker compose -f compose.prod.yaml exec -T database mariadb-dump --all-databases -uroot -p$DATABASE_PASSWORD > ~/zoomail_db_dump/zoomail_$now.sql

cd ~/zoomail_db_dump

# compress the database dump
tar -czvf zoomail_$now.tar.gz zoomail_$now.sql

# remove the uncompressed database dump
rm zoomail_$now.sql

chmod 600 zoomail_$now.tar.gz

cd -

# copy the compressed database dump to the backup server
docker run \
    --rm \
    -v ~/zoomail_db_dump:/zoomail_db_dump \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    amazon/aws-cli:latest \
    s3 cp /zoomail_db_dump/zoomail_$now.tar.gz s3://zoomail-db-dump/dumps/zoomail_$now.tar.gz
