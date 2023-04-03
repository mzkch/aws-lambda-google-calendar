# aws-lambda-google-calendar

This project is a Python script that uses the Google Calendar API.
AWS services used in this project are AWS Lambda.

## Installation

1. Clone the project.
```shell
git clone https://github.com/mzkch/aws-lambda-google-calendar.git
```

2. Create a virtual environment and install the necessary libraries.
```shell
cd aws-lambda-google-calendar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Enable the Google API and create a service account. Please refer to [Google Calendar API Quickstart](https://developers.google.com/calendar/quickstart/python) for more details.

4. Save the `service_account_key.json` file containing the authentication credentials in the root directory of the project.

## Usage

1. Edit variables in `lambda_function.py` to match your environment.

2. Run the script.
```shell
python lambda_function.py
```

## Deployment

1. Create a zip file of the project.
```shell
./create_lambda_function_zip.sh
```

2. Upload the zip file `deployment.zip` to AWS Lambda. Edit the `upload_code.sh` file to match your environment.
```shell
./upload_code.sh
```

3. Add the required environment variables to the Lambda function.
