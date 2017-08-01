# phone-number-check-and-send-example.py
# tested in python 2.7.13
# uses one non-standard Python library - requests see
# http://docs.python-requests.org/en/latest/index.html

# Combines phone number verification service and SMS API to demonstrate
# how an Enterprise can save money and improve customer engagement by
# checking an existing contact number list to see which numbers are valid/exist
# and which are mobile.
# It then only sends SMS to the valid mobile numbers.

# Dependencies
# 1) an account on developer.syniverse.com
# 2) enable service offerings for Developer Community Gateway, Phone Number Verification,
# voice and messaging offering
# 3) Application with SDC Gateway, Event subscription Services, Notification services,
# whitelisting services, SDC reporting Service, Voice & Messaging and Phone Number
# Verification Services.
# 4) have whitelisted the mobile number in the below list
# 5) the Access token for your application, as well as the appropriate channel ID for
# the country

import requests
from urllib import quote
from urlparse import urljoin

# these are some example numbers including one mobile number (already whitelisted for my account)
number_list = ['+447860438585',
               '+446543211234',
               '+442079202200',
               '+18136375000']

# this is the base url for the phone number verification service, last element in url is
# replaced with the encoded phone number in international format.
# the + needs to be encoded to %2B
pnv_base_url = 'https://api.syniverse.com/numberidentity/v3/numbers/[phonenumber]'

# this is the url for the SMS API
sms_url = 'https://api.syniverse.com/scg-external-api/api/v1/messaging/message_requests'

# this is the channel id for the UK test long code. replace it if you are using a different country
uk_channel_id = 'DJm-vHcnSBKbeK4b2FAOLQ'
# this is the access token for the application
access_token = '[Your-Access-Token]'

# these are the headers for the API requests
headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}

# this loops through the numbers in the list above,
# queries the information for each number
# evlauates whether the number is valid, and whether it is a mobile number
# if it is then it sends an SMS to the number
# if it is a landline it doesnt send the SMS
# it flags if the number is not valid.
for number in number_list:
    print '\nLooking up ' + number
    # make the url for the lookup including quoting the + correctly)
    pnv_url = urljoin(pnv_base_url, quote(number))
    pnv_response = requests.get(pnv_url, headers=headers)
    print 'number lookup response status code is ' + str(pnv_response.status_code)

    # decode the json response and extra the details
    dict_response = pnv_response.json()['numberidentity']

    # logic to check response fields for validity and type
    if dict_response['validity'] == 'true':
        print'\tThe phone number is valid'
        if dict_response['number_type'] == 'M':
            print'\t\tIt is a mobile phone number, so will send the SMS'
            sms_text = 'This a valid mobile number on ' + dict_response['carrier_name']
            payload = {'from': 'channel:' + uk_channel_id, 'to': [number], 'body': sms_text}
            sms_response = requests.post(sms_url, json=payload, headers=headers)
            print '\t\tThe SMS API response code is ' + str(sms_response.status_code)
        else:
            print'\t\tThe phone number is not mobile, so not going to send an SMS'
    else:
        print'\tThe phone number is invalid, should remove this from the list'

