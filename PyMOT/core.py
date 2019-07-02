# Version 0.3.0, created by Matt Howell. Licensed under GPL 3.0

import json
import requests
import os
from pprint import pprint
from datetime import datetime
import test
from PyMOT import apigui
from PyMOT import gui

#import apigui

# Object creation using a specified index from list, and runs mileage_check method

class Vehicle():
    # placeholder
    kind = 'car'

    def __init__(self, value):

        self.invalidReg = False
        self.motExpiry = None

        if value is None:
            print('Invalid vehicle registration. Please try again.')
            self.invalidReg = True
            self.allTests = None

        else:

            activeVehicle = {}
            for i in value:
                activeVehicle.update(i)

            self.reg = activeVehicle.get('registration')
            self.fuel = activeVehicle.get('fuelType')
            self.make = activeVehicle.get('make')
            self.model = activeVehicle.get('model')
            self.colour = activeVehicle.get('primaryColour')

            if 'motTestExpiryDate' in activeVehicle.keys():
                self.latestMileage = activeVehicle.get('motTestExpiryDate')
                print(self.latestMileage)


            if 'motTests' in activeVehicle.keys():

                self.allTests = activeVehicle.get('motTests')
                self.latestTest = next(iter(self.allTests))
                self.latestResults = latest_results(self.latestTest)
                self.firstUsedDate = get_first_used_date(activeVehicle)

                self.clockedCheck = mileage_check(self)
                self.motExpiry = mot_expiry(self.latestTest)
                self.latestMileage = latest_mileage(self)

            pprint(activeVehicle)

            if 'motTests' not in activeVehicle.keys():

                print("\n No MOT's recorded for this vehicle\n")
                self.allTests = None

#TODO use PyQt5.uic.loadUiType() to load design.ui from PyQT5 directly

#




## TODO Complete later. If it exists, import any saved vehicles from saved_vehicles.csv
#if os.path.exists('data\saved_vehicles.csv'):

def api_send(api_key: object, reg: object) -> object:
    #print(reg)
    api_url_base = 'https://beta.check-mot.service.gov.uk/trade/vehicles/mot-tests/?registration='
    headers = {'Content-type': 'application/json', 'x-api-key': '{0}'.format(api_key)}

    # remove whitespace
    reg = ''.join(reg.split())

    api_url = api_url_base + reg
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        value = response.json()

        return value



## TODO Move all analysis methods to separate .py file

def mileage_check(veh):
    # test values
    #odometerValues = [102000, 99000, 81000, 91000, 83000, 70000]

    odometerValues = []

    for test in veh.allTests:
        for k, v in test.items():
            if k == 'odometerValue':
                odometerValues.append(v)

    # Convert string values to integers
    for i in range(len(odometerValues)):
        odometerValues[i] = int(odometerValues[i])

    # Check if odometer values are only in descending order
    for x in range(len(odometerValues) - 1):
        if odometerValues[x] - odometerValues[x + 1] < 0:
            return False
    return True

def latest_mileage(veh):
    # latest MOT is always first
    for test in veh.allTests:
        for k, v in test.items():
            if k == 'odometerValue':
                return v


def get_first_used_date(veh):

    for k, v in veh.items():
        if k == 'firstUsedDate':
            return v

def latest_results(veh):

    results = []

    for k, v in veh.items():
        if k == 'testResult':
            results.append(v)
        if k == 'rfrAndComments':
            results.append(v)

    return results


def mot_expiry(veh):
    currentDate = datetime.now()

    for k, v in veh.items():

        if k == 'motTestExpiryDate':
            date = datetime.strptime(v, '%Y.%m.%d')
            return date

        if k == 'expiryDate':
            date = datetime.strptime(v, '%Y.%m.%d')
            return date

# Methods to format test results for GUI display
#fix

def latestresults_format(comments):
    for comment in comments:
        temp_text = '{0} ({1})'.format(comment['text'], comment['type'])
        formatted_comments = []
        formatted_comments.append(temp_text)

        return formatted_comments


# Tests

#test.structureTest()

# Old code from CLI

# Method to get API key from user if file not found

# UNUSED in GUI version
#def get_api_key():
#    choice = input('\nAPI key not found.\n\nOptions:\n'
#                   '1) Enter API key\n'
#                   '2) Specify API key filename\n'
#                  'Selection: ')
#    if choice == '1':
#        key = input('Please enter API key: ')
#        return key
#    if choice == '2':
#        fileloc = input('Please specify API file location relative to application root\n'
#                         ' Example: "data\mot_api.txt"\n')
#        with open(fileloc) as key:
#            key = key.read()
#            return key
#    if '1' or '2' not in choice:
#       print('\nInvalid selection, please try again')
#        get_api_key()


# Import DVSA MOT API key from text file, if file not present uses get_api_key()
# to get API key from user
#api_key = None

#if os.path.exists('data/mot_api.txt'):
#    with open('data/mot_api.txt') as key:
#        api_key = key.read()
#if api_key is None:
#    api_key = get_api_key()
