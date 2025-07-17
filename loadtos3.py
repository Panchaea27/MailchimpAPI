import boto3
import os
from dotenv import load_dotenv

def load_to_s3_and_delete(folder_name,bucket_name,access_key,secret_key,delete):

    #establish connection to s3
    s3_client = boto3.client (
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key
    )
    #list all the files in the folder parameter
    upload_files = os.listdir(folder_name)
    
    #assumed aws folder paths
    campaigns_aws_path = 'python-mailchimp/campaigns/'
    email_act_aws_path = 'python-mailchimp/email-activity/'

    #for each file in the local folder...
    for file in upload_files:
        # if it's a campaign files in json
        if file.startswith('campaigns_') and file.endswith('.json'):
            #create an upload path for the campaign file
            upload_aws = os.path.join(campaigns_aws_path,file)
            print(upload_aws)
            #create an origin path for the campaign file
            file_path = os.path.join(folder_name,file)
            print(file_path)
            #upload the file
            s3_client.upload_file(file_path,bucket_name,upload_aws)
            #if param in function was set to Y or y, then also delete the local file
            if delete == 'Y' or delete == 'y':
                os.remove(file_path)
        #if it's an email activity json file 
        if file.startswith('emailact_id_') and file.endswith('.json'):
            #create an upload path for the file
            upload_aws = os.path.join(email_act_aws_path,file)
            print(upload_aws)
            #create an origin path for the file
            file_path = os.path.join(folder_name,file)
            print(file_path)
            #upload the actual file
            s3_client.upload_file(file_path,bucket_name,upload_aws)
            #if param in function was set to Y or y, then also delete the local file
            if delete == 'Y' or delete == 'y':
                os.remove(file_path)

