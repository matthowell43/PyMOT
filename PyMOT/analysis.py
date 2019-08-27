## TODO move all analytics from core.py to this file


class FaultScanner():

    def __init__(self):
        # placeholder values
        self.brakeFaultsTotal = 2
        self.brakeFaultsLatest = 1
        self.suspensionFaultsTotal = 5
        self.suspensionFaultsLatest = 2


        # various lists with fault descriptions that PyMOT tries to locate
        self.faultLocation = ['nearside', 'near-side', 'offside', 'off-side', 'front', 'rear', 'o/s', 'n/s', 'os', 'ns']
        self.brakeFaults = ['brake', 'brakes', 'disc', 'discs', 'pad', 'pads', 'pad(s)', 'pitted', 'scored', 'weakened',
                            'handbrake', 'hand-brake', 'parking brake', 'wearing thin', 'brake pipe', 'binding']
        self.faultDamage = ['corroded', 'damaged', 'worn']

        # List with safety-critical items
        ## TODO add button in interface, alert if within last two years
        self.criticalDamage = ['excessively corroded', 'significantly reducing structural strength', 'bad oil leak',
                               'severe oil leak', 'airbag']