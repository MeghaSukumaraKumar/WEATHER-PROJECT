Architecture Overview

This project is a serverless real-time weather data pipeline built using AWS services and Snowflake.

The pipeline fetches weather data from the OpenWeather API, processes it using AWS Lambda, stores it in DynamoDB and Amazon S3, and finally ingests the data into Snowflake using Snowpipe.

---

# Tech Stack

## AWS Services
- Amazon EventBridge
- AWS Lambda
- Amazon DynamoDB
- DynamoDB Streams
- Amazon S3
- Amazon SQS
- AWS IAM

## Data Warehouse
- Snowflake
- Snowpipe
- External Stage
- Storage Integration

## API
- OpenWeather API

---

# Project Workflow

## Step 1 — Fetch Weather Data

Amazon EventBridge triggers a Lambda function on a schedule.

The Lambda function:
- Calls the OpenWeather API
- Retrieves live weather data
- Processes the response

---

## Step 2 — Store Data in DynamoDB

The Lambda function stores the weather data in Amazon DynamoDB.

This acts as:
- Temporary storage
- Operational datastore
- Event source for downstream processing

---

## Step 3 — DynamoDB Stream Trigger

Whenever new data is inserted into DynamoDB:
- DynamoDB Streams capture the change
- Another Lambda function is triggered automatically

---

## Step 4 — Store Processed Data in S3

The second Lambda function:
- Reads DynamoDB stream events
- Converts records into CSV format
- Uploads files into Amazon S3

Example:
python
s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{FOLDER_NAME}/{file_name}",
                Body=csv_buffer.getvalue()
            )

---

## Step 5 — Snowflake Integration

Snowflake connects securely to S3 using:
- IAM Role
- Storage Integration
- External Stage

Snowflake continuously monitors the S3 bucket.

---

## Step 6 — Snowpipe Auto Ingestion

When new files arrive in S3:
- S3 sends notifications to SQS
- Snowpipe automatically loads the data into Snowflake tables

This enables near real-time analytics.

---

# Architecture Flow

text
OpenWeather API
        ↓
EventBridge
        ↓
Lambda
        ↓
DynamoDB
        ↓
DynamoDB Stream
        ↓
Lambda
        ↓
Amazon S3
        ↓
SQS Notification
        ↓
Snowpipe
        ↓
Snowflake


---

# Repository Structure

text
WEATHER-PROJECT

DBSTREAM-S3.py

LAMBDA-DYNAMO.py

README.md

WEATHER.sql

requirements.txt


---

# AWS Components

## EventBridge
Schedules weather API calls automatically.

## Lambda Functions
- Fetch weather data
- Process DynamoDB stream records
- Upload CSV files to S3

## DynamoDB
Stores incoming weather data.

## DynamoDB Streams
Captures table changes in real time.

## S3 Bucket
Stores CSV weather files.

## SQS
Triggers Snowpipe notifications.

## IAM
Provides secure access between AWS and Snowflake.

---

# Snowflake Components

## Storage Integration
Secure connection between Snowflake and S3.

## External Stage
Represents the S3 location inside Snowflake.

## Snowpipe
Automatically ingests new files from S3.

---

# Example Snowflake SQL

## Create File Format

sql
CREATE or replace file format CSV_FORMAT
                    type = csv
                    field_delimiter = ','
                    skip_header = 1
                    null_if = ('NULL' , 'null')
                    empty_field_as_null = true; 



## Create Stage

sql
CREATE or replace stage CSV_STAGE
url = 's3://weatherpro-bucket/projectsnow/'
STORAGE_INTEGRATION = S3_INT
file_format = CSV_FORMAT;


## Create Snowpipe

sql
CREATE or replace pipe MYWEATHER_PIPE
AUTO_INGEST = TRUE
AS 
COPY INTO WEATHER_TABLE
FROM @CSV_STAGE
ON_ERROR = CONTINUE;

---

# Setup Instructions

## 1. Clone Repository

bash
git clone https://github.com/MeghaSukumaraKumar/WEATHER-PROJECT.git

cd weather-data-pipeline


---

## 2. Install Python Dependencies

bash
pip install -r requirements.txt


---

## 3. Configure AWS Resources

Create:
- Lambda Functions
- EventBridge Rule
- DynamoDB Table
- S3 Bucket
- SQS Queue
- IAM Roles & Policies

---

## 4. Configure Snowflake

Create:
- Storage Integration
- External Stage
- Snowpipe
- Weather Table

---



# Author

Megha S Kumar

---
