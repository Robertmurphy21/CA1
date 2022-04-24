#!/usr/bin/env python3
# KFC Ordering System 
# Robert Murphy D00228588

import sys
import boto3
import json
from argparse import ArgumentParser
import re

from KFC_common3 import *

parser = ArgumentParser(description='order placer for KFC example')
parser.add_argument('--stack', help='stack name', default='KFC')
args = parser.parse_args()
stack_name=args.stack

# Find the Topic ARN using CloudFormation 
topic_arn = None
cf_client = boto3.client('cloudformation')
response = cf_client.describe_stacks(StackName=stack_name)
outputs = response["Stacks"][0]["Outputs"]
topic_arn = cf_output(outputs, "ordertopicarn")
menubucketname = cf_output(outputs, "menubucketname")

if topic_arn is None:
    print("no topic ARN found")
    exit

# client object for SNS
sns = boto3.client('sns')

# load menu from S3
s3 = boto3.resource('s3')
content_object = s3.Object(menubucketname, 'deals.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
deals = json.loads(file_content)

pattern = re.compile(r'(?:(\d)?(\w)(?:/(.*?)\.)?)')

while True:
    clear()
    print("KFC Takeaway - ORDER SEQUENCE\n")
    order = {}
    order['customer'] = input('enter customer name: ')
    items = []
    print("\nDeals on Display:")
    for key, value in deals.items():
        print('\t%s = %s' % (key, value))
    print("\n")
    print("Enter order as letter or letters for each item,")
    print("Use optional quantity prefix, ")
    print("Change if needed,")
    print("\n")
    order_line = input('enter order: ')
    for (quantity, product,requests) in re.findall(pattern, order_line):
        if '' == quantity:
            quantity = 1
        if product not in deals:
            print('product %s not found!' % product)
            continue
        product_name = deals[product]
        print("\t%s x\t%s" % (quantity, product_name))
        items.append({ "quantity": quantity, "item": product_name, "requests": requests})
    order['items'] = items
    sns.publish(TargetArn=topic_arn, Message=json.dumps(order))
    print('order sent')
    print(' ')

    
