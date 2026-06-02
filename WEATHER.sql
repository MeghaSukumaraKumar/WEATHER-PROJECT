CREATE DATABASE PROJECT_WEATHER;
USE DATABASE PROJECT_WEATHER;

CREATE SCHEMA MY_WEATHERSCHEMA;
USE SCHEMA MY_WEATHERSCHEMA;

--create table to load csv data
CREATE or replace TABLE WEATHER_TABLE(
    CITY   VARCHAR(128)
    ,time   VARCHAR(128)
    ,humidity  NUMBER(20,5)
    ,pressure_mb  VARCHAR(128)
    ,temp  NUMBER(20,5)
    ,wind_dir   VARCHAR(128)
    ,wind_speed  NUMBER(20,5)
);
select * from WEATHER_TABLE;


CREATE or replace STORAGE INTEGRATION S3_INT
TYPE = external_stage
STORAGE_PROVIDER = s3
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::590379873533:role/SNOWFLAKE_ROLE'
STORAGE_ALLOWED_LOCATIONS = ('s3://weatherpro-bucket/projectsnow/');

DESC INTEGRATION S3_INT;


--creating the file format--
CREATE or replace file format CSV_FORMAT
                    type = csv
                    field_delimiter = ','
                    skip_header = 1
                    null_if = ('NULL' , 'null')
                    empty_field_as_null = true; 

--CREATE A STAGE
CREATE or replace stage CSV_STAGE
url = 's3://weatherpro-bucket/projectsnow/'
STORAGE_INTEGRATION = S3_INT
file_format = CSV_FORMAT;

show stages;

---CREATE A SNOWPIPE TO LOAD DATA FROM S3 TO SNOWFLAKE
CREATE or replace pipe MYWEATHER_PIPE
AUTO_INGEST = TRUE
AS 
COPY INTO WEATHER_TABLE
FROM @CSV_STAGE
ON_ERROR = CONTINUE;

show pipes;

SELECT * FROM WEATHER_TABLE;


