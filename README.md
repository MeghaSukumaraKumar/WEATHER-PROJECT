Project Overview

The pipeline periodically fetches live weather data, stores it temporarily in DynamoDB, transforms the data into JSON files, and automatically loads it into Snowflake using Snowpipe.

This architecture demonstrates how modern cloud-native services can be combined to build a reliable real-time data engineering workflow.

*Architecture
OpenWeather API
        ↓
Amazon EventBridge
        ↓
AWS Lambda
        ↓
Amazon DynamoDB
        ↓
DynamoDB Streams
        ↓
AWS Lambda
        ↓
Amazon S3
        ↓
Amazon SQS Notification
        ↓
Snowpipe
        ↓
Snowflake

*Tech Stack
AWS Services
Amazon EventBridge
AWS Lambda
Amazon DynamoDB
DynamoDB Streams
Amazon S3
Amazon SQS
AWS IAM
Data Warehouse
Snowflake
Snowpipe
External Stage
Storage Integration
External API
OpenWeather API

*How It Works
1. Fetch Weather Data
Amazon EventBridge triggers a Lambda function at scheduled intervals.

The Lambda function:
Calls the OpenWeather API
Retrieves the latest weather information
Processes and structures the response data

2. Store Data in DynamoDB
The processed weather data is stored in Amazon DynamoDB.

DynamoDB serves as:
A temporary data store
An operational database
An event source for downstream processing

3. Capture Database Changes
Whenever a new record is inserted:
DynamoDB Streams capture the change event
A second Lambda function is automatically triggered

4. Export Data to Amazon S3
The second Lambda function:

Reads DynamoDB stream events
Converts the records into CSV format
Uploads them to Amazon S3

Example:

s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{FOLDER_NAME}/{file_name}",
                Body=csv_buffer.getvalue()
            )
5. Integrate Amazon S3 with Snowflake
Snowflake securely connects to the S3 bucket using:
-IAM Role
-Storage Integration
-External Stage

This allows Snowflake to continuously monitor incoming files.

6. Automatically Load Data with Snowpipe
Whenever a new CSV file arrives in S3:

Amazon S3 sends a notification to Amazon SQS
Snowpipe receives the notification
Snowflake automatically ingests the file into a target table

This enables near real-time analytics and reporting.

Repository Structure
WEATHER_PROJECT/
*Lambda/
  -To ftech data from weatherAPI and to load into nDynamoDB table:LAMBDA-DYNAMO.py
  -To load data from DynamoDB to S3 Bucket:DBSTREAM-S3.py
*README.md
*Snowflake : WEATHER.sql/
  -Storage Integration
  -File format
  -External stage
  -Snowpipe
  
..AWS Components
*Amazon EventBridge
Schedules weather data collection automatically.

*AWS Lambda
Responsible for:
-Fetching weather data from the API
-Processing DynamoDB stream events
-Uploading CSV files to Amazon S3

*Amazon DynamoDB
Stores incoming weather data and acts as an operational datastore.

*DynamoDB Streams
Captures table modifications in real time and triggers downstream processing.

*Amazon S3
Stores processed weather records as CSV files.

*Amazon SQS
Delivers S3 event notifications to Snowpipe.

*AWS IAM
Provides secure and controlled access between AWS services and Snowflake.

..Snowflake Components
*Storage Integration
*Creates a secure connection between Snowflake and Amazon S3.
*External Stage
*Represents the S3 bucket location inside Snowflake.
*Snowpipe
*Automatically loads newly added files into Snowflake tables.

..Sample Snowflake ConfiguratioN

*CREATE or replace file format CSV_FORMAT
                    type = csv
                    field_delimiter = ','
                    skip_header = 1
                    null_if = ('NULL' , 'null')
                    empty_field_as_null = true; 


*CREATE or replace stage CSV_STAGE
url = 's3://weatherpro-bucket/projectsnow/'
STORAGE_INTEGRATION = S3_INT
file_format = CSV_FORMAT;

*CREATE or replace pipe MYWEATHER_PIPE
AUTO_INGEST = TRUE
AS 
COPY INTO WEATHER_TABLE
FROM @CSV_STAGE
ON_ERROR = CONTINUE;

..Getting Started
Clone the Repository
git clone https://github.com/MeghaSukumaraKumar/WEATHER-PROJECT.git
cd WEATHER-PROJECT
Install Dependencies
pip install -r requirements.txt


..This project demonstrates:

Building event-driven architectures on AWS
Developing serverless data pipelines
Implementing real-time data ingestion patterns
Integrating AWS services with Snowflake
Designing scalable and cost-effective analytics pipelines

..Author

Megha S Kumar
