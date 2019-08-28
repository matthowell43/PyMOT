## TODO move all analytics from core.py to this file


class FaultScanner():

    def __init__(self):

        comments = []

        # placeholder values, used to test GUI
        self.brakeFaultsTotal = 2
        self.brakeFaultsLatest = 1
        self.suspensionFaultsTotal = 5
        self.suspensionFaultsLatest = 2

        # various lists with fault descriptions that PyMOT tries to locate
        # regex searches on these lists will not be case-sensitive
        self.faultLocationTerms = ['nearside', 'near-side', 'offside', 'off-side', 'front', 'rear', 'o/s', 'n/s', 'os', 'ns']
        self.brakeFaultsTerms = ['brake', 'brakes', 'disc', 'discs', 'pad', 'pads', 'pad(s)',
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

        if comments is not None:
            self.brake_fault_scanner(comments)

        #
    def brake_fault_scanner(self, comments):
        latest_brake_faults = []
        historic_brake_faults = []
        brake_fault_count = 0

        # first need to ensure the braking system is mentioned in the comment

        # use regex to find brake fault comments, then added unaltered to corresponding lists.

        # todo assign these variables directly to FaultScanner vars instead of return
        # returns two lists: one for the latest MOT alone, and the other containing everything except the latest.
        return latest_brake_faults, historic_brake_faults, brake_fault_count