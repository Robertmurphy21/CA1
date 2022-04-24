#!/usr/bin/env python3
# KFC monitoring of Orders Placed
# Robert Murphy D00228588

import sys
import boto3
import json
from argparse import ArgumentParser

from KFC_common3 import *

parser = ArgumentParser(description='order monitor for KFC')
parser.add_argument('--stack', help='stack name', default='KFC')
parser.add_argument('--wait', help='wait for making order', action='store_true', default=False)
args = parser.parse_args()
stack_name=args.stack

# finding the queue URL using CloudFormation 
queue_url = None
cf_client = boto3.client('cloudformation')
response = cf_client.describe_stacks(StackName=stack_name)
outputs = response["Stacks"][0]["Outputs"]
queue_url = cf_output(outputs, "onsitequrl")

if queue_url is None:
    print("no queue URL found")
    exit

# client object for SQS
sqs = boto3.client('sqs')
wait_time_seconds = 1

while True:
    # receive
    response = sqs.receive_message(QueueUrl=queue_url, WaitTimeSeconds=wait_time_seconds, MaxNumberOfMessages=1)
    wait_time_seconds = 20

    if 'Messages' not in response:
        continue

    # loop messages
    for message in response['Messages']:
        
        # do processing work here (example just prints)
        print("order received: ")
        order = json.loads(json.loads(message['Body'])['Message'])
    
        customer = order['customer']
        print("\tfor: %s" % customer )

        items = order['items']
        for item in items:
            print("\t\t%sx %s >> %s" % ( item['quantity'], item['item'], item['requests'] ) )

        made = False
        while ( True == args.wait ):
            print(' ')
            if 'y' == input('order done [y/n]...'):
                break
            
        # delete once processed
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
        
        print("---\n\n")
