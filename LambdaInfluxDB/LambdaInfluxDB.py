import json
import re
import base64
import boto3
from datetime import datetime
from influxdb import InfluxDBClient
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_client import InfluxDBClient, Point, WriteOptions


bucket='yahoostocks'
org='ziadaco'
token='ZlK233UlgMJqNPrMc-DAs2NY1qCHPfDxgmGBYhu4vXRcOSsT_WBvXT8lp3yuO9EL4CIh32gNhcjcML12xpDSVQ=='
url="http://34.201.151.107:8086"

client=InfluxDBClient( 
    url=url,
    token=token,
    org=org
)


def decodedata(record):
    #for record in event['Records']:
        
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        payload_json = json.loads(payload)
                
        print(payload_json)
        return payload_json


'''
def send_email(payload_json):
    response = ses.send_email(
        Source='ahmedziada100001@gmail.com',
        Destination={
            'ToAddresses': [
                'ahmedziada100002@gmail.com'
            ]
        },
        Message={
            'Subject': {
                'Data': 'Hello from Yahoo Finance'
            },
            'Body': {
                'Text': {
                    'Data': f"This email is to let you know that this {payload_json['name']} stock price dropped by 5% from it's opening price and this is it's current price: {payload_json['price']}"
                }
            }
        }
    )

    return
    
'''



def send_email(subject, body, sender, recipient):
    # Create an instance of the SES client
    ses = boto3.client('ses')
    
    # Send an email
    response = ses.send_email(
        Source='ahmedziada100001@gmail.com',
        Destination={
            'ToAddresses': [
                'ahmedziada100002@gmail.com'
            ]
        },
        Message={
            'Subject': {
                'Data': 'Hello from Yahoo Finance'
            },
            'Body': {
                'Text': {
                    'Data': f"This email is to let you know that this {payload_json['name']} stock price dropped by 5% from it's opening price and this is it's current price: {payload_json['price']}"
                }
            }
        }
    )
    
    # Return the message ID
    return response['MessageId']

def writetoinflux(payload_json):
    
        write_api = client.write_api(write_options=SYNCHRONOUS)


        name=payload_json.pop('name')
        
        write_api.write("yahoostocks", "ziadaco",
                        {
                            "measurement": "Yahoo-Stocks",
                            "tags": {"name":name} ,
                            "time":datetime.now(),
                            "fields": payload_json 
                        })
        
        return 'Done'



def lambda_handler(event, context):
    
        for record in event['Records']:
            
            decodeddata=decodedata(record)
            
            writetoinflux(decodeddata)
            
            if decodeddata['price'] < decodeddata['Open']*.95 :
                
               send_email(decodedata)
        
        