# Familial Turmoil

## Development

Start the venv environment
```
python -m venv venv
venv\Scripts\activate.bat
```

Run flask app locally
```
flask --app application run
```

## Deployment
```
eb init -p python-3.12 --region us-east-1

eb create eb-ft
```

## Clean Up
Delete the EB instance
EC2 Instance
S3 Bucket
CloudWatch Logs

