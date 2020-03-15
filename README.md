# lambda-s3

Lambda function backed by S3 storage

This chalice application can be deployed to any AWS account

It allows you to access an Sqlite database as persistance layer to save state


```
USAGE:
curl -X POST -H 'Content-Type: application/json' -d @data.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/insert/default.sqlite/test

curl -X POST -H 'Content-Type: application/json' -d @select.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/select/default.sqlite

curl -X POST -H 'Content-Type: application/json' -d @delete.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/execute/default.sqlite

curl -X POST -H 'Content-Type: application/json' -d @data.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/generate_create_table/default.sqlite/test
```
