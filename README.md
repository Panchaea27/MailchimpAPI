# Mailchimp Data Extraction Script

A Python script that extracts campaign and email activity data from Mailchimp Marketing API for a specified date range and optionally uploads the data to AWS S3.

## Features

- Extract campaign data for a custom date range
- Extract email activity data for each campaign
- Comprehensive logging of all operations
- Retry mechanism for API failures
- Optional S3 upload with local file cleanup
- Data validation and error handling

## Prerequisites

- Python 3.6+
- Mailchimp Marketing API account and API key
- AWS S3 bucket (optional, for upload functionality)

## Installation

1. Clone or download the script files
2. Install required dependencies:

```bash
pip install mailchimp-marketing python-dotenv boto3
```

3. Create a `.env` file in the project root with your credentials:

```env
API_KEY=your_mailchimp_api_key_here
BUCKET_NAME=your_s3_bucket_name
ACCESS_KEY=your_aws_access_key
SECRET_KEY=your_aws_secret_key
```

## Project Structure

```
project-root/
├── main_script.py          # Main extraction script
├── loadtos3.py            # S3 upload functionality
├── .env                   # Environment variables (create this)
├── data/                  # Output directory (created automatically)
│   ├── log/              # Log files
│   ├── campaigns_*.json  # Campaign data files
│   └── emailact_id_*.json # Email activity files
└── README.md
```

## Usage

1. Run the main script:

```bash
python main_script.py
```

2. Follow the interactive prompts:
   - Enter start date (YYYY-MM-DD format)
   - Enter end date (YYYY-MM-DD format, or leave blank for today)
   - Choose whether to upload to S3
   - Choose whether to delete local files after upload

## Script Workflow

### 1. Date Input & Validation

- Prompts for start and end dates
- Validates date format (YYYY-MM-DD)
- Ensures end date is after start date
- Defaults to current date if end date is blank

### 2. Data Extraction

- Connects to Mailchimp Marketing API
- Retrieves campaign data for specified date range
- For each campaign, extracts email activity data
- Implements retry mechanism (up to 3 attempts) for API failures
- Saves data as timestamped JSON files

### 3. Logging

- Creates detailed log files in `data/log/` directory
- Logs all operations, errors, and timestamps
- Includes extraction attempts and success/failure status

### 4. S3 Upload (Optional)

- Uploads files to organized S3 structure:
  - Campaigns: `python-mailchimp/campaigns/`
  - Email Activity: `python-mailchimp/email-activity/`
- Option to delete local files after successful upload

## Output Files

### Campaign Data

- **Filename**: `campaigns_YYYY-MM-DD_HH-MM-SS.json`
- **Content**: Complete campaign information for the date range

### Email Activity Data

- **Filename**: `emailact_id_{campaign_id}_YYYY-MM-DD_HH-MM-SS.json`
- **Content**: Email activity data for each individual campaign

### Log Files

- **Filename**: `Mailchimp_API_log_YYYY-MM-DD_HH-MM-SS.txt`
- **Content**: Detailed operation logs, errors, and timestamps

## Error Handling

- **API Errors**: Automatic retry with exponential backoff
- **Date Validation**: Input validation with user-friendly error messages
- **File Operations**: Comprehensive error logging
- **S3 Upload**: Error handling for AWS operations

## Environment Variables

| Variable      | Description                 | Required           |
| ------------- | --------------------------- | ------------------ |
| `API_KEY`     | Mailchimp Marketing API key | Yes                |
| `BUCKET_NAME` | AWS S3 bucket name          | Only for S3 upload |
| `ACCESS_KEY`  | AWS access key ID           | Only for S3 upload |
| `SECRET_KEY`  | AWS secret access key       | Only for S3 upload |

## S3 Folder Structure

When uploading to S3, files are organized as follows:

```
your-bucket/
├── python-mailchimp/
│   ├── campaigns/
│   │   └── campaigns_YYYY-MM-DD_HH-MM-SS.json
│   └── email-activity/
│       └── emailact_id_{campaign_id}_YYYY-MM-DD_HH-MM-SS.json
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Mailchimp API key is valid and has proper permissions
2. **Date Format Error**: Use YYYY-MM-DD format only
3. **S3 Upload Error**: Check AWS credentials and bucket permissions
4. **File Not Found**: Ensure the `data/` directory exists (created automatically)

### Rate Limiting

The script includes a retry mechanism with delays to handle API rate limits. If you encounter persistent rate limit issues, consider:

- Reducing the date range
- Running the script during off-peak hours
- Contacting Mailchimp support for rate limit increases

## Dependencies

- `mailchimp-marketing`: Official Mailchimp Marketing API library
- `python-dotenv`: Environment variable management
- `boto3`: AWS SDK for Python
- `json`: JSON data handling (built-in)
- `datetime`: Date/time operations (built-in)
- `os`: File system operations (built-in)
- `time`: Time-related functions (built-in)

## License

This script is provided as-is for educational and business purposes. Please ensure compliance with Mailchimp's API terms of service and your organization's data handling policies.

## Support

For issues related to:

- Mailchimp API: Check [Mailchimp API Documentation](https://mailchimp.com/developer/marketing/api/)
- AWS S3: Check [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- Script functionality: Review the log files for detailed error information
