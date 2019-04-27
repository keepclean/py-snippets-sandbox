import bisect
import itertools
import json
import random

def gen_test_case():
    result = list()
    for rack in range(random.randint(1, 5)):
        metals_in_rack = list()
        for metal in range(1, random.randint(2, 10)):
            name = "94m{}".format(random.randint(1 + 10 * rack, 10 + 10 * rack))
            if name not in metals_in_rack:
                metals_in_rack.append(name)
                result.append({
                    "name": name,
                    "rack": "rack_{}".format(rack)
                })
    
    return result


while True:
    by_rack = dict()
    for item in gen_test_case():
        rack = item['rack']
        by_rack.setdefault(rack, [])
        bisect.insort(by_rack[rack], item['name'])


    dms_number = random.randint(1, 4)
    metals_needed = 5 - dms_number
    consul_servers = ['94dm{}'.format(m) for m in range(1, dms_number + 1)]

    racks = itertools.cycle(by_rack[r] for r in sorted(by_rack.keys()))
    for i in range(metals_needed):
        for m in racks.next():
            if m not in consul_servers:
                consul_servers.append(m)
                break

    print "Test case"
    print json.dumps(by_rack)
    print json.dumps(consul_servers, indent=2)
    print "##########"

    again = raw_input("Do you want more? (y/n): ")
    if again not in ('y', 'yes'):
        break