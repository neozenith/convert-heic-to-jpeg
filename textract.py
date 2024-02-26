import boto3
import sys
from pathlib import Path
import os
from pprint import pprint as pp
from dotenv import load_dotenv
import asyncio


load_dotenv()

local_dir = Path("./data/")
os.makedirs(local_dir, exist_ok=True)
print(os.environ["AWS_PROFILE"])
print(os.environ["AWS_REGION"])
session = boto3.session.Session(profile_name=os.environ["AWS_PROFILE"], region_name=os.environ["AWS_REGION"])
s3_client = session.client('s3')
textract_client = session.client("textract")
comprehend_client = session.client("comprehend")

# TODO: 
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_document.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_expense.html
# https://docs.aws.amazon.com/textract/latest/dg/what-is.html

async def main(args):
    ...



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
    loop.close()
