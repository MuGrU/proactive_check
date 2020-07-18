#!/usr/bin/env python
# coding: utf-8

import json
import re
import requests
import sys


def updateKernelBaseLine():
    r = requests.get('https://www.suse.com/support/kb/doc/?id=000019587')
    if r.status_code != 200:
        sys.exit(1)
    # transform the HTML into a huge string
    buf = r.text.replace('\n', '')
    prods = {}
    # ignore the first entry of the split, since it's the beginning of the HTML:
    # <head>...<body>...
    for table in buf.split('<h3><b>')[1:]:
        prod = re.search('([\d\w\s]+)</b></h3>', table).group(1)
        release = ''
        prods[prod] = {}

        for tr in table.split('<tr>')[1:]:
            # should be only two lines, with date and version
            # or only version
            cols = re.findall('>([\w\-\.\d]+)</td>', tr)

            # first line after a product, shows only version e.g SLE15-LTSS
            if not release and len(cols) == 0:
                release = re.search('<b>([\w\s\d]+)</b>', tr).group(1)
                prods[prod][release] = []
                continue

            # blank lines
            if len(cols) == 0:
                continue

            date = cols[0]
            version = ''
            # some products have a date, but not yet a version...
            if len(cols) == 2:
                version = cols[1]
            prods[prod][release].append({'date': date, 'version': version})
    print(json.dumps(prods, sort_keys=False, indent=4))


def grabbingSupportconfig():
    # Collecting and parsing information from supportconfig txt files via def basic_environment
     systemInformation = basic_environment()
     print(json.dumps(systemInformation, sort_keys=False, indent=True))

def basic_environment():
    with open("basic-environment.txt") as f:
        systemInformation = {}
        data = f.read()
        hostname = re.search('(Linux\s)([\D*]*)(.*)', data).group(2)
        uname = re.search('(Linux\s)([\D*]*)(.*)', data).group(3)
        kernelVersion = re.search("\d.*\.\d.*\d.*\-\d.*\.\d...", data).group().replace("-d", ".1")

# I need do discovery the properly regex for kernelVersion, I tried https://regex101.com/r/osKVNU/1 and group(3) and no donuts
#        kernelVersion = re.search('(^Linux\s)([\D*]+)([\d\.\-\.\w]+)', data).group(3)

        slesVersion = re.search("VERSION = ([\d]+)", data).group(1)
        patchLevel = re.search("PATCHLEVEL = ([\d]+)", data).group(1)
        systemInformation["basic_environment"] = {
            'hostname': hostname,
            'uname': uname,
            'slesVersion': slesVersion,
            'patchLevel': patchLevel,
            'kernelVersion': kernelVersion}
    return systemInformation

# updateKernelBaseLine()
grabbingSupportconfig()

