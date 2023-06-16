from os import access
import os
import jwt.utils
import time
import math
import requests
import uuid


token = jwt.encode(
    {
        "aud": "doordash",
        "iss": os.environ["DOORDASH_KEY"],#Developer ID
        "kid": os.environ["DD_KID"],#Key ID
        "exp": str(math.floor(time.time() + 300)),
        "iat": str(math.floor(time.time())),
    },
    jwt.utils.base64url_decode(os.environ["DD_SS"]),#Signing secret
    algorithm="HS256",
    headers={"dd-ver": "DD-JWT-V1"})


def deliver(business_address, 
            business_name, 
            business_phone, 
            business_instruct, 
            dropoff_addr, 
            dropoff_name, 
            dropoff_num, 
            dropoff_instruct, 
            num):
    """Simulate a DoorDash Delivery. Not confirmed to work yet."""
    endpoint = "https://openapi.doordash.com/drive/v2/deliveries/"

    headers = {"Accept-Encoding": "application/json",
               "Authorization": "Bearer " + token,
               "Content-Type": "application/json"}

    request_body = { # Modify pickup and drop off addresses below
        "external_delivery_id": str(uuid.uuid4()),
        "pickup_address": business_address,
        "pickup_business_name": business_name,
        "pickup_phone_number": business_phone,
        "pickup_instructions": business_instruct,
        "dropoff_address": dropoff_addr,
        "dropoff_business_name": dropoff_name,
        "dropoff_phone_number": dropoff_num,
        "dropoff_instructions": dropoff_instruct,
        "order_value": num
    }

    create_delivery = requests.post(endpoint, headers=headers, json=request_body) # Create POST request
    return "Status code(HTTP Format): " + str(create_delivery.status_code)

#print(deliver("901 Market Street 6th Floor San Francisco, CA 94103", "Wells Fargo SF Downtown", "+16505555555", "Enter gate code 1234 on the callbox.", "901 Market Street 6th Floor San Francisco, CA 94103", "Wells Fargo SF Downtown", "+16505555555", "Enter gate code 1234 on the callbox.", 1))
