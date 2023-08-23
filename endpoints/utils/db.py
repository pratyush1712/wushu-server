import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
import boto3
from botocore.exceptions import NoCredentialsError

load_dotenv()

mongo_server_url = os.environ.get("MONGODB_URL")
client = MongoClient(mongo_server_url)
db = client[os.environ.get("DB_NAME")]

list_serv_members = db[os.environ.get("LISTSERV_MEMBERS_COLLECTION")]
eboard = db[os.environ.get("EBOARD_COLLECTION")]
members = db[os.environ.get("MEMBERS_COLLECTION")]
performances = db[os.environ.get("PERFORMANCES_COLLECTION")]

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_S3_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


def upload_to_aws(local_file, bucket, s3_file):
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
