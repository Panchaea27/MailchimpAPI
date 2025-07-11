#This file will be the script to pull from API

#currently in progress :)

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv
import os
import json
from datetime import datetime

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def date_compare(start_dt,end_dt):
    if datetime.strptime(start_dt,"%Y-%m-%d") > datetime.strptime(end_dt,"%Y-%m-%d"):
        return False
    else:
        return True

load_dotenv()
api_key = os.getenv("API_KEY")
server = os.getenv("SERVER")

while True:
    from_dt_input = str(input("Input the since create time date (yyyy-mm-dd format only): "))
    if is_valid_date(from_dt_input):
        break
    else:
        print("Incorrect format. Try again")

while True:
    till_dt_input = str(input("Input the before create time date (yyyy-mm-dd format only) Leave blank if until today (exclusive): "))
    if till_dt_input == '':
        break
    elif is_valid_date(till_dt_input) and date_compare(from_dt_input,till_dt_input):
        break
    else:
        print(f"Incorrect format or the before create time is lower than since create time ({from_dt_input})")




timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
default_before_create_time = f"{timestamp[:11]}T00:00:00+00:00"
since_create_time = f"{from_dt_input}T00:00:00+00:00"
user_before_create_time = f"{till_dt_input}T00:00:00+00:00"

if till_dt_input == '':
   before_create_time = default_before_create_time
else:
   before_create_time = user_before_create_time

campaigns_json_path = f'data/campaigns_{timestamp}.json'

query_params = {
    'since_create_time': since_create_time,
    'before_create_time': before_create_time
}

print(query_params)

try:
    client = MailchimpMarketing.Client()
    client.set_config({
    "api_key": api_key,

    })
    campaign_response = client.campaigns.list(**query_params)
    campaign_ids = [campaign["id"] for campaign in campaign_response.get("campaigns", [])]
    with open(campaigns_json_path,'w')as file:
       json.dump(campaign_response,file,indent=4)
    for campaign in campaign_ids:
       email_act_response = client.reports.get_email_activity_for_campaign(campaign)
       email_json_path = f'data/emailact_id_{campaign}_{timestamp}.json'
       with open(email_json_path,'w') as file:
          json.dump(email_act_response,file,indent=4)
except ApiClientError as error:
  print("Error: {}".format(error.text))









