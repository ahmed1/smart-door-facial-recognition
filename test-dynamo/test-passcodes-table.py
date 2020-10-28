from decimal import Decimal
import json
import boto3

from datetime import datetime, timezone, timedelta
import time

# need epoch timestamp in seconds, not milliseconds -- number type
# timetolive
# confirm that it converts the time properly
def load_passcode(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('passcodes')
#    for restaurant in restaurants:
#        restaurant["insertedAtTimestamp"] = str(datetime.datetime.now())
    row = {}
    row['faceId'] = "1234"
    row['passcode'] = "5678"
    second_offset = 300
    
    
    timetolive = round((datetime.now(tz=timezone.utc) - datetime(1970, 1,1, tzinfo=timezone.utc) + timedelta(seconds=second_offset)).total_seconds())
    print(timetolive)
    row['ttl'] = timetolive
    table.put_item(Item=row)


if __name__ == '__main__':
    
    load_passcode()
#    with open("data/db/db.json") as json_file:
#        restaurant_list = json.load(json_file, parse_float=Decimal)

    
#    load_restaurants(restaurant_list)
    
