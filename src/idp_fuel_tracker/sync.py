import boto3
from pathlib import Path
import os
from pprint import pprint as pp
from dotenv import load_dotenv

load_dotenv()


def sync():
    local_dir = Path("./data/")
    os.makedirs(local_dir, exist_ok=True)
    print(os.environ["AWS_PROFILE"])
    session = boto3.session.Session(profile_name=os.environ["AWS_PROFILE"])
    s3_client = session.client('s3')
    response = s3_client.list_objects_v2(Bucket=os.environ["S3_BUCKET"], Prefix=os.environ["S3_KEY_PREFIX"])
    pp(response)
    for f in response['Contents']:
        if not f['Key'].endswith("/"):
            print(f['Key'])
            print(Path(f['Key']).name)
            s3_client.download_file(os.environ["S3_BUCKET"], f['Key'], local_dir / Path(f['Key']).name)
