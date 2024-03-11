from typing import List
import boto3
import sys
import json
from pathlib import Path
import base64
import os
from pprint import pprint as pp
from dotenv import load_dotenv
import asyncio


load_dotenv()

local_dir = Path("./data/")




session = boto3.session.Session(profile_name=os.environ["AWS_PROFILE"], region_name=os.environ["AWS_REGION"])
s3_client = session.client('s3')
textract_client = session.client("textract")
comprehend_client = session.client("comprehend")

# TODO: 
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_document.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_expense.html
# https://docs.aws.amazon.com/textract/latest/dg/what-is.html
# https://dev.to/jbahire/text-extraction-made-easy-with-amazon-textract-12p
#
# {
#    "Document": { 
#       "Bytes": blob,
#       "S3Object": { 
#          "Bucket": "string",
#          "Name": "string",
#          "Version": "string"
#       }
#    },
#    "FeatureTypes": [ "string" ],
#    "HumanLoopConfig": { 
#       "DataAttributes": { 
#          "ContentClassifiers": [ "string" ]
#       },
#       "FlowDefinitionArn": "string",
#       "HumanLoopName": "string"
#    }
# }

def filename_filter(f):
    return any(f.name.lower().endswith(x) for x in ["jpg", "jpeg"])

async def list_files():
    os.makedirs(local_dir, exist_ok=True)
    os.makedirs(local_dir / "JPEG", exist_ok=True)
    return [f for f in Path("./data/JPEG/").iterdir() if filename_filter(f)]

async def process_document(f, overwrite=False):
    document_bytes = f.read_bytes()
    print(f)
    outputfilename: Path = f.parent / (f.name + '.json')
    print(outputfilename)
    if overwrite or not outputfilename.exists():
        response = textract_client.analyze_expense(    
            Document={
                'Bytes': document_bytes,
            }
        )
        outputfilename.write_text(json.dumps(response, indent=2))
    else:
        print(f"Skipping because {overwrite=} or {outputfilename.exists()=}")
    return outputfilename

async def process_documents():
    files: List[Path] = await list_files()
    print(files)
    results = await asyncio.gather(*[process_document(f) for f in files])
    print(results)

    #TODO: extract key values out:
    # ODO meter
    # Number of litres
    # Total price of fuel
    # Transaction date
