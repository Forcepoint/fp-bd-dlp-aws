# Forcepoint DLP with Amazon Web Services Security Hub

Full config.json format:
```
{
  "AwsAccountId": "string",
  "ProductArn": "ProductArn": "arn:aws:securityhub:us-east-1:111111111111:product/111111111111/default",
  "aws_access_key_id": "string",
  "aws_secret_access_key": "string",
  "region_name": "us-east-1",
  "file_location": "/XMLFileCopy/AWS",
  "HIGH": true,
  "MEDIUM": true,
  "LOW": true
  "Database_Connection": {
    "Server": "SERVER",
    "Database": "db",
    "Trusted_Connection": "yes",
    "UID": "",
    "PWD": ""
  },
  "AzureCustomerId": "",
  "AzureSharedKey": "",
  "LogName": "ForcepointDLPEvents"
}
```

**Create single .exe from windows**

1. Double click install.bat from the root directory and wait for scrolling text to stop at cloud selection options.
2. Enter 'y' for either azure or azure. Or select 'y' on both if required
3. After a minute you will see the bd-dlp-exporter.zip, this can now be distributed.