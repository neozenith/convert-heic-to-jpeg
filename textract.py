import boto3
from pathlib import Path
import os
from pprint import pprint as pp
from dotenv import load_dotenv

load_dotenv()

local_dir = Path("./data/")
os.makedirs(local_dir, exist_ok=True)
print(os.environ["AWS_PROFILE"])
session = boto3.session.Session(profile_name=os.environ["AWS_PROFILE"])
s3_client = session.client('s3')
textract_client = session.client("textract")
comprehend_client = session.client("comprehend")

