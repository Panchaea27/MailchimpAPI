# Mailchimp Campaign Email Extractor

`mailchimp_campaign_emails.py` is a command-line utility that connects to the [Mailchimp Marketing API](https://mailchimp.com/developer/marketing/api/) to extract campaign metadata and related email activity. The script saves data locally as JSON files, logs all steps, and optionally uploads the results to an AWS S3 bucket using a helper function in `loadtos3.py`.

## Project Structure

```
.
├── mailchimp_campaign_emails.py       # Main script
├── loadtos3.py                        # Contains load_to_s3_and_delete()
├── .env                               # Stores Mailchimp and AWS credentials
├── requirements.txt                   # Python dependencies
└── data/
    ├── log/                           # Run logs
    ├── campaigns_<timestamp>.json     # Campaign data
    └── emailact_id_<id>_<timestamp>.json  # Email activity per campaign
```

## Features

- Interactive CLI prompts for inputting a campaign date range
- Validates user input for date format and logical range order
- Extracts campaign metadata and email activity using Mailchimp API
- Saves output as timestamped JSON files in `data/`
- Logs all operations, retries, and API errors to a file in `data/log/`
- Optionally uploads extracted files to S3 and deletes them locally

## Requirements

All Python dependencies are listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

## .env Configuration

The script expects a `.env` file in the root directory with the following keys:

```ini
API_KEY=your_mailchimp_api_key
BUCKET_NAME=your_s3_bucket_name
ACCESS_KEY=your_aws_access_key
SECRET_KEY=your_aws_secret_key
```

These are used for connecting to Mailchimp and optionally uploading to AWS S3.

## Usage

Run the script via:

```bash
python mailchimp_campaign_emails.py
```

The script will prompt you to:

1. Enter a **start date** (`YYYY-MM-DD` format)
2. Optionally enter an **end date** (leave blank to default to today)
3. Choose whether to **upload files to S3**
4. Decide whether to **delete local files** after upload

### Example Prompt Interaction

```
Input the since create time date (yyyy-mm-dd format only): 2025-07-01
Input the before create time date (yyyy-mm-dd format only) Leave blank if until today (exclusive): 2025-08-01
Would you like to upload the files to S3 bucket (Y/n) ? y
Would you like the uploaded files to be deleted after upload (Y/n)? y
```

### Input Validation

- Dates must follow the `YYYY-MM-DD` format; otherwise, the user is re-prompted.
- The end date must not be earlier than the start date.
- If the end date is left blank, it defaults to today’s date.

## Functions

### Defined in `mailchimp_campaign_emails.py`

- `is_valid_date(date_str)`  
  Validates the input date format.

- `date_compare(start_dt, end_dt)`  
  Ensures the start date is not after the end date.

### Imported from `loadtos3.py`

- `load_to_s3_and_delete(folder, bucket, access_key, secret_key, delete_flag)`  
  Uploads all files in the specified folder to the configured S3 bucket, and optionally deletes them from disk afterward.

## Logging

Each run creates a log file in `data/log/` with the following information:

- Script start time
- Date range used for extraction
- Mailchimp API results (campaign IDs, filenames)
- Retry attempts and API errors (if any)
- Upload and file deletion status

Log filenames follow this format:

```
Mailchimp_API_log_<timestamp>.txt
```

## Notes

- The script retries API calls up to 3 times in case of failure.
- All campaign and email data are saved in timestamped JSON files.
- No files are overwritten between runs due to unique filenames.

## License

Unlicensed / Public Domain — do whatever you want with this code. No attribution or credit needed ;)

## Support

For issues related to:

- Mailchimp API: Check [Mailchimp API Documentation](https://mailchimp.com/developer/marketing/api/)
- AWS S3: Check [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- Script functionality: Review the log files for detailed error information