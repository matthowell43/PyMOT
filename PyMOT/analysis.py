## TODO move all analytics from core.py to this file

from PyMOT.core import latest_results

import re

class FaultScanner():

    def __init__(self, tests):

        if tests is not None:
            # comments to be scanned
            self.historicComments = []
            self.latestComments = []

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
            self.brakeFaultTerms = ['brake', 'brakes', 'disc', 'discs', 'brake pad', ' brake pads', 'brake pad(s)',
                                     'handbrake', 'hand-brake', 'parking brake', 'brake pipe', 'brake pipes', 'brake pipe(s)',
                                     'brake hose']
            # brake system damage terms
            self.brakeDamageTerms = ['pitted', 'scored', 'weakened', 'wearing thin', 'binding', 'twisted', 'deteriorated',
                                     'imbalanced', 'lipped', '1.5mm', '1.5 mm', 'thin', 'fluctuating', 'juddering']

            # generic damage terms
            self.faultDamageTerms = ['corroded', 'damaged', 'worn', 'corroding']

            # List with safety-critical items
            ## TODO add button in interface, alert if within last two years
            self.criticalDamageTerms = ['excessively corroded', 'significantly reducing structural strength', 'bad oil leak',
                                        'severe oil leak', 'airbag', 'excessively deteriorated', 'juddering severely',
                                        'structure corroded', 'chassis corroded', 'rigidity of the assembly is significantly reduced']


            # extracts comments from tests

            self.comments = tests.get('rfrAndComments')
            for test in tests:
                self.comments.update(test.get('rfrAndComments'))


            for k, v in self.comments:
                if k = 'text':
                    self.allComments.append(v)

            self.brake_fault_scanner(self.allComments)

    def brake_fault_scanner(self, comments):

        comment_strings = []
        # takes first comment to be examined separately
        latest_comments = comments.pop(0)
        for comment in comments:









            #for comment_word in comment.split():
           #     for term in self.brakeFaultTerms:
           #         if term.lower() == comment_word.lower():
           #             print("Brake fault identified: " + comment + "\nTerm found: " + comment_word)
           #             self.brake_fault_count = self.brake_fault_count + 1
           #             self.historic_brake_faults.append(comment)

        # first need to ensure the braking system is mentioned in the comment

        # use regex to find brake fault comments, then added unaltered to corresponding lists.


        # separate block for latest test scan
       # latest_test = latest_results(tests[0])

        # todo assign these variables directly to FaultScanner vars instead of return
        # returns two lists: one for the latest MOT alone, and the other containing everything except the latest.
