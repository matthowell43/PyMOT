## TODO move all analytics from core.py to this file

#from PyMOT.core import latest_results

import re

from pprint import pprint
from datetime import datetime

class FaultScanner():

    def __init__(self, tests):

        if tests is not None:

            self.safetyIssues = False

            self.brakeTermsDetected = set()
            self.brakeFaultsDetected = []

            self.safetyFaultsDetected = []

            # comments to be scanned
            self.historicComments = {}
            self.latestComments = {}

            # Brake fault data
            self.latest_brake_faults = []
            self.historic_brake_faults = []
            self.brake_fault_count = 0

            # placeholder values, used to test GUI
            self.brakeFaultsTotal = 2
            self.brakeFaultsLatest = 1
            self.suspensionFaultsTotal = 5
            self.suspensionFaultsLatest = 2

            # various lists with fault descriptions that PyMOT tries to locate
            # regex searches on these lists will not be case-sensitive
            self.faultLocationTerms = ['nearside', 'near-side', 'offside', 'off-side', 'front', 'rear', 'o/s', 'n/s', 'os', 'ns']
            self.brakeFaultTerms = ['disc', 'discs', 'pad', ' pads', 'pad(s)',
                                     'handbrake', 'hand-brake', 'parking', 'pipe', 'pipes', 'pipe(s)',
                                     'hose', 'cable']
            # brake system damage terms
            self.brakeDamageTerms = ['pitted', 'scored', 'weakened', 'wearing thin', 'binding', 'twisted', 'deteriorated',
                                     'imbalanced', 'lipped', '1.5mm', '1.5 mm', 'thin', 'fluctuating', 'juddering']

            # generic damage terms
            self.faultDamageTerms = ['corroded', 'damaged', 'worn', 'corroding']

            # List with safety-critical items
            ## TODO add button in interface, alert if within last two years
            self.criticalDamageTerms = ['excessively corroded', 'significantly reducing structural strength', 'bad oil leak',
                                        'severe oil leak', 'airbag', 'excessively deteriorated', 'juddering severely',
                                        'structure corroded', 'chassis corroded', 'rigidity of the assembly is significantly reduced',
                                        'engine management', 'EML', 'check engine', 'steering rack']

            self.safetyFaultTerms = []


            # extracts comments from tests

            self.latestCommentsRetrieved = False
            self.tests = []

            for test in tests:
                self.tests.append(test)

            self.fault_scanner_regex()

            self.check_safety_issues()

    # regex alternative implementation
    def fault_scanner_regex(self):
        # brake scan
        brake_fault_regex = None
        single_test = []
        date_temp = ""

        # placeholder so the scan loop can get started
        default_date = '2100.01.01 00:00:00'
        previous_date = datetime.strptime(default_date, '%Y.%m.%d %H:%M:%S').date()

        delta = None
        date_current = None

        completed_date = None

        brake_temp = set()
        critical_temp = set()

        for test in self.tests:
            # todo add new clear() for every temp list added
            brake_temp.clear()
            critical_temp.clear()

            for k, v in test.items():
                # get test date

                if k == 'completedDate':
                    completed_date = v

                    #todo move retest check to GUI code
                    #date_current = datetime.strptime(v, '%Y.%m.%d %H:%M:%S').date()
                    #date_current = date_temp.date()
                    # calc date delta for next if check
                    #delta = (previous_date - date_current).days
                    #print(delta)


                if k == 'rfrAndComments' and len(v) > 0:
                    # access nested list of dicts containing comments
                    for comment_set in v:

                        for k1, v1 in comment_set.items():

                            if k1 == 'text':
                                check_brake_present = re.search('brake', v1, re.IGNORECASE)

                                if check_brake_present:
                                    for term in self.brakeFaultTerms:
                                        brake_fault_regex = re.findall(term, v1, flags=re.IGNORECASE)

                                        if brake_fault_regex:
                                            brake_temp.add(v1)

                                # safety-critical scan
                                for term in self.criticalDamageTerms:
                                    critical_fault_regex = re.findall(term, v1, flags=re.IGNORECASE)

                                    if critical_fault_regex:
                                        critical_temp.add(v1)


                    # Store brake faults
                    brake_temp_dict = {completed_date: brake_temp.copy()}
                    self.brakeFaultsDetected.append(brake_temp_dict)

                    # Store safety-critical faults
                    critical_temp_dict = {completed_date: critical_temp.copy()}
                    self.safetyFaultsDetected.append(critical_temp_dict)



       # pprint(self.brakeFaultsDetected)
       # print("Safety-critical items")
        #pprint(self.safetyFaultsDetected)

    def check_safety_issues(self):
        brakes_latest = self.brakeFaultsDetected[0]
        safety_latest = self.safetyFaultsDetected[0]

        for k, v in safety_latest.items():
            #access comment set
            for comment in v:
                if len(comment) > 0:
                    self.safetyIssues = True

        for k, v in brakes_latest.items():
            #access comment set
            for comment in v:
                if len(comment) > 0:
                    self.safetyIssues = True

# obsolete
    def brake_fault_scanner(self):
        #return

        fault_dict_list = []

        # iterating through list of dicts
        for comment in self.comments:
            fault_dict = {}
            fault_detected = False
            comment_list_temp = []

            for k, v in comment.items():

                if k == 'text':

                    # splits the comment sentence into words to be checked individually
                    for comment_word in v.split():
                        # brake check
                        for term in self.brakeFaultTerms:
                            brake_faults = []

                            if term.lower() == comment_word.lower() and "brake".lower() in v:
                                print("Brake fault identified: " + comment + "\nTerm found: " + comment_word)
                                self.brake_fault_count = self.brake_fault_count + 1
                                brake_faults.append(v)
                                fault_detected = True

                        # suspension check
                        # todo enable after term dictionary and variables created
                        #for term in self.suspensionFaultTerms:

                if k == 'completedDate' and fault_detected:
                    fault_dict['completedDate'] = v

                # appends the temp dict to the final list- final part of method
                # end result being a list of dicts organised by test date, each one having a list of faults
                if fault_dict is not None:
                    self.faultDictList.append(fault_dict.copy())




