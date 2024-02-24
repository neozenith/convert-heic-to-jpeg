# HEIC to PNG/JPG

## Quickstart

### Setup

```sh
rm -rfv .venv
python3 -m venv .venv
.venv/bin/python3 -m pip install -U pip pip-tools

.venv/bin/python3 -m piptools compile --generate-hashes requirements.in --output-file requirements.txt
.venv/bin/python3 -m pip install -r requirements.txt --require-hashes --no-deps --only-binary :all:
```

### Run


```sh
.venv/bin/python3 convert.py
```

## Serverless

```sh
sam init
sam build --profile <profile>
export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock
sam local invoke

# https://stackoverflow.com/a/75347359/622276
sam deploy --profile <profile> --guided

sam list endpoints --profile <profile> --output json | jq .
sam remote invoke <LambdaFunctionName> --profile <profile> --stack-name <stack_name> --region ap-southeast-2
```

# TODO
 - Read write files in S3
 - Migrate conversion code to AWS SAM Lambda
 - Add Textract Lambda
 - Add SQS queues
 - Add Lambda for retrieving results