import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

# defining functions for user date input. will check if correctly formatted
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

#load .env keys
load_dotenv()
api_key = os.getenv("API_KEY")


#timestamp for file naming
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#directory of the log 
log_dir = 'data/log'

#ensured log_dir exists
os.makedirs(log_dir, exist_ok=True)
#name of the log file. Each run of the script creates a new text file
logname = f'{log_dir}/Mailchimp_API_log_{timestamp}.txt'



#user input for 'since create date' check if correctly formatted with loop
while True:
    from_dt_input = str(input("Input the since create time date (yyyy-mm-dd format only): "))
    if is_valid_date(from_dt_input):
        break
    else:
        print("Incorrect format. Try again")

#user input for 'before create date' check if correctly formatted with loop
while True:
    till_dt_input = str(input("Input the before create time date (yyyy-mm-dd format only) Leave blank if until today (exclusive): "))
    if till_dt_input == '' and date_compare(from_dt_input,timestamp[:10]):
        break
    elif is_valid_date(till_dt_input) and date_compare(from_dt_input,till_dt_input):
        break
    else:
        print(f"Incorrect format or the before create time is lower than since create time ({from_dt_input})")

#if user left before create date empty, populate with today
if till_dt_input == '':
    till_dt_input = timestamp[:10]

#Header for the log file. 
with open(logname,'w') as file:
    file.write(f"Mailchimp Marketing API LOG. Script Start Time: {timestamp}\n")
    file.write(f"Extraction of data for the selected period: {from_dt_input} - {till_dt_input}\n")
    file.write("----------------------------\n")


#define before/since for the parameters
before_create_time = f"{till_dt_input}T00:00:00+00:00"
since_create_time = f"{from_dt_input}T00:00:00+00:00"


#define json path for campaigns
campaigns_json_path = f'data/campaigns_{timestamp}.json'

#define query parameters for api call
query_params = {
    'since_create_time': since_create_time,
    'before_create_time': before_create_time
}

#attempts for re-try loops
attempt_no = 1
max_attempt = 3
log_attempt_no = 1


############################# MAIN EXTRACTION BLOCK START ##############

# loop while attempt count allows to retry extraction if it fails
while attempt_no <= max_attempt:

    try:
        #log attempt number
        with open(logname,'a') as file:
            file.write(f"Extraction attempt number: {log_attempt_no}\n")
        #restart waittime, used if attempt fails
        waittime = 5
        #set up api connection
        client = MailchimpMarketing.Client()
        client.set_config({
        "api_key": api_key
        })
        #campaign response using dates defined by query params
        campaign_response = client.campaigns.list(**query_params)

        #list all campaign_ids (used for email activity extraction and logging)
        campaign_ids = [campaign["id"] for campaign in campaign_response.get("campaigns", [])]
        #create a json with campaign data
        with open(campaigns_json_path,'w')as file:
            json.dump(campaign_response,file,indent=4)
            #log successful extraction
            with open(logname,'a') as file:
                file.write("Campaign information extracted successfully.\n")
                file.write(f"Campaign data saved as: {campaigns_json_path}\n")
                file.write(f"Campaign IDs extracted: {campaign_ids}\n")
        # Email activity extraction block. For each Campaign ID create a JSON file
        for campaign in campaign_ids:
            email_act_response = client.reports.get_email_activity_for_campaign(campaign)
            email_json_path = f'data/emailact_id_{campaign}_{timestamp}.json'
            with open(email_json_path,'w') as file:
                json.dump(email_act_response,file,indent=4)
                # log successful extraction for each camapaign email activity
                with open(logname,'a') as file:
                    file.write(f"Email activity for campaign {campaign} extracted successfully.\n")
                    file.write(f"{campaign} email activity JSON saved as {email_json_path}\n")
        #break the while loop if extraction is successful
        break
    #except block if the API errors
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        errorforlog = "Error: {}".format(error.text)
        #save error to log file
        with open(logname,'a') as file:
                    file.write(f"Attempt Number: {log_attempt_no} has failed.\n")
                    file.write("Error from the API:\n")
                    file.write(f"{errorforlog}\n")
        # change attempt number
        max_attempt -=1
        log_attempt_no +=1
        print(f'waiting {waittime} seconds & trying again! Attempts left: {max_attempt}')
    #wait waittime and retry...
    while waittime > 0:
        print(f"{waittime} seconds left")
        time.sleep(1)
        waittime -=1
#If max attempt reaches 0, output the message + log it
if max_attempt == 0:
    print("Max attempt count reached. Extraction was not completed. See log errors for details")
    with open(logname,'a') as file:
        file.write("Max attempt count reached. Extraction was not completed.")
# otherwise log successful extraction.
else:
    print("Extraction successful.")
    with open(logname,'a') as file:
        file.write("Extraction completed.")









