import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()


def sync_files(local_dir = Path("./data/"), overwrite: bool = False):
    """Sync files from S3 to local."""
    os.makedirs(local_dir, exist_ok=True)

    session = boto3.session.Session(profile_name=os.environ["AWS_PROFILE"])
    s3_client = session.client('s3')
    response = s3_client.list_objects_v2(Bucket=os.environ["S3_BUCKET"], Prefix=os.environ["S3_KEY_PREFIX"])

    for f in response['Contents']:
        if not f['Key'].endswith("/"):
            print(f['Key'])
            print(Path(f['Key']).name)
            target_file = local_dir / Path(f['Key']).name
            if overwrite or not target_file.exists():
                s3_client.download_file(os.environ["S3_BUCKET"], f['Key'], target_file)