# Tests for PyMOT 0.2


def structure_test():


    vehObj = Vehicle()

    print('\n***Object test***\n')
    print(vehObj.reg)
    print(vehObj.fuel)
    print(vehObj.make)
    print(vehObj.model)
    print(vehObj.colour)
    # pprint(vehObj.allTests)

    print('Latest MOT')
    pprint(vehObj.latestTest)

    print('\n\n ***For loop test, uses my car***')

    for test in vehObj.allTests:
        for x in test.values():
            if x == '2020.04.08':
                print('Expiry date match!')
                print(x)

    print('\n\n ***Test: Key value iteration of dict within list***')

    for test in vehObj.allTests:
        for k, v in test.items():
            if k == 'completedDate':
                print(v)

