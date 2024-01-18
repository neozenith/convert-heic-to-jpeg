# HEIC to PNG/JPG

## Quickstart

### Setup

```sh
python3 -m venv .venv
.venv/bin/python3 -m pip install -U pip pip-tools
.venv/bin/python3 -m piptools compile --generate-hashes requirements.in --output-file requirements.txt
.venv/bin/python3 -m pip install -r requirements.txt --require-hashes --no-deps --only-binary :all:
```

### Run


```sh
.venv/bin/python3 convert.py
```

# TODO
 - Read write files in S3
 - Migrate conversion code to AWS SAM Lambda
 - Add Textract Lambda
 - Add SQS queues
 - Add Lambda for retrieving results