import json
import pandas as pd
import boto3
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

def lambda_handler(event, context):
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    input_key = event['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3')

    obj = s3.get_object(Bucket=input_bucket, Key=input_key)
    body = obj['Body'].read().decode('utf-8')

    json_dicts = body.strip().splitlines()

    df = pd.DataFrame(columns=['id', 'status', 'amount', 'date'])
    rows_to_add = []

    for line in json_dicts:
        if line.strip():  
            try:
                py_dict = json.loads(line)
                if py_dict['status'] == 'delivered':
                    rows_to_add.append(py_dict)
            except json.JSONDecodeError as e:
                print(f"Error processing line: {line} - {e}")
    if rows_to_add:
        df = pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)

    df.to_csv('/tmp/test.csv', sep=',', index=False)
    print('test.csv file created')


    try:
        date_var = str(date.today())
        file_name = f'processed_data/{date_var}_processed_data.csv'
    except Exception as e:
        print(f"Error generating file name: {e}")
        file_name = 'processed_data/processed_data.csv'
        

    bucket_name = os.getenv('output_bucket')


    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file('/tmp/test.csv', file_name)


    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=os.getenv('TopicArn'),
        Message=f"File {input_key} has been formatted and filtered. It has been stored in {bucket_name} as {file_name}"
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
