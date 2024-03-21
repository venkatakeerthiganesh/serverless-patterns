# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import json
import os

dynamodb_client = boto3.client('dynamodb')

# Read the DynamoDB table name from environment variable
dynamodb_table_name = os.environ.get('DYNAMODB_TABLE_NAME')

def insert_item(body):
  # Insert data into DynamoDB table
  try:
    dynamodb_client.put_item(
      TableName=dynamodb_table_name, 
      Item={
          'id': {'S': body['id']}, 
          'Weather': {'S': body['Weather']}
      })
    return {
        'statusCode': 200,
        'body': 'Successfully inserted data!'
    }
  except Exception as e:
    return {
      'statusCode': 502,
      'body': f'Internal Error while inserting data into DynamoDB: {str(e)}'
    }

def delete_item(body):
    try:
        # Extract the id from the path parameters
        id = body['id']

        # Delete the item from DynamoDB table
        dynamodb_client.delete_item(
            TableName=dynamodb_table_name,
            Key={
                'id': {'S': id}
            }
        )

        return {
            'statusCode': 200,
            'body': f'Successfully deleted item with id: {id}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error deleting item from DynamoDB: {str(e)}'
        }

def lambda_handler(event, context):
  authorized_user = False

  # Check if the authorization token is present in the request headers
  if 'authorizationToken' not in event:
    return {
      'statusCode': 403,
      'body': 'Requested resource is forbidden'
    }
  
  # Validate the authorization token
  token = event['authorizationToken']

  if token != 'allowme':
    authorized_user = False
    return {
      'statusCode': 403,
      'body': 'Requested resource is forbidden'
    }
  elif token == 'allowme':
    authorized_user = True

  if authorized_user:
    # Extract JSON data from the request body
    try:
      body = json.loads(event['body'])
    except Exception as e:
      return {
        'statusCode': 400,
        'body': 'Request body is not valid JSON.'
      }
    
    if event['httpMethod'] == 'POST':
      # Validate the presence of 'id' and 'Weather' attributes
      if 'id' not in body or 'Weather' not in body:
        return {
          'statusCode': 400,
          'body': 'Both "id" and "Weather" attributes are required in the request.'
        }

      # Validate that no other attributes are present
      if len(body) != 2:
        return {
          'statusCode': 400,
          'body': 'Only "id" and "Weather" attributes are allowed in the request.'
        }
      return insert_item(event)

    elif event['httpMethod'] == 'DELETE':
      return delete_item(body)
