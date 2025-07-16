import boto3
import os
from dotenv import load_dotenv

def load_to_s3_and_delete(folder_name,bucket_name,access_key,secret_key):
    s3_client = boto3.client (
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
    )

    upload_files = os.listdir(folder_name)
    campaigns_aws_path = 'python-mailchimp/campaigns/'
    email_act_aws_path = 'python-mailchimp/email-activity/'
    for file in upload_files:
        if file.startswith('campaigns_') and file.endswith('.json'):
            upload_aws = os.path.join(campaigns_aws_path,file)
            print(upload_aws)
            file_path = os.path.join(folder_name,file)
            print(file_path)
            s3_client.upload_file(file_path,bucket_name,upload_aws)
            os.remove(file_path)
        if file.startswith('emailact_id_') and file.endswith('.json'):
            upload_aws = os.path.join(email_act_aws_path,file)
            print(upload_aws)
            file_path = os.path.join(folder_name,file)
            print(file_path)
            s3_client.upload_file(file_path,bucket_name,upload_aws)
            os.remove(file_path)


# load_dotenv()
# folder_name = 'data/'
# bucket_name = os.getenv("BUCKET_NAME")
# access_key = os.getenv("ACCESS_KEY")
# secret_key = os.getenv("SECRET_KEY")

# load_to_s3_and_delete(folder_name,bucket_name,access_key,secret_key)