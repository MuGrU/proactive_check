#!/usr/bin/env python
# coding: utf-8

import json, re, requests, sys, os, getopt

def print_banner():
    print("=============================================================================")
    print("                     Proactive_Check Utility - Supportconfig                 ")
    print("                          Script Version: (beta)                             ")
    print("                          Script Date: 2020-07-19                            ")
    print("=============================================================================")
    print("\n")

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]

def extractSupportconfig():
    tarCommand = "tar xvJf /home/toliveira/github/proactive_check/supportconfigs/nts_linux-ivcd_200718_2314.txz"
    os.system(tarCommand)

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
#    print(json.dumps(prods, sort_keys=False, indent=4))
    return prods

def grabSupportconfig():
    # Collecting and parsing information from supportconfig txt files via def basic_environment
    #
    systemInformation = basic_environment()
#    print(json.dumps(systemInformation, sort_keys=False, indent=4))
    return systemInformation

def basic_environment():
    with open("basic-environment.txt_sap") as f:
        systemInformation = {}
        data = f.read()
        hostname = re.search('(Linux\s)([\D*]*)(.*)', data).group(2)
        uname = re.search('(Linux\s)([\D*]*)(.*)', data).group(3)
        kernelVersion = re.search("\d.*\.\d.*\d.*\-\d.*\.\d...", data).group().replace("-d", ".1")

        # I need do discovery the properly regex for kernelVersion, I tried https://regex101.com/r/osKVNU/1 and group(3) and no donuts
        #kernelVersion = re.search('(^Linux\s)([\D*]+)([\d\.\-\.\w]+)', data).group(3)

        slesVersion = re.search("VERSION = ([\d]+)", data).group(1)
        patchLevel = re.search("PATCHLEVEL = ([\d]+)", data).group(1)
        #dataKernel = updateKernelBaseLine()
        #print(json.dumps(dataKernel, sort_keys=False, indent=4))
        systemInformation["basic_environment"] = {
            'hostname': hostname,
            'uname': uname,
            'slesVersion': slesVersion,
            'patchLevel': patchLevel,
            'kernelVersion': kernelVersion,
#            'dataKernel': dataKernel}
        }
        isSAP = re.findall("sles_sap", data)
        if len(isSAP) > 0:
            systemInformation["basic_environment"].update({'isSAP': 'SLES 4 SAP'})
    return systemInformation

def print_formats():
        systemInformation = grabSupportconfig()
        print_banner()
#Mask
#       print("" + systemInformation["basic_environment"].get(""))
        print("Hostname: " + systemInformation["basic_environment"].get("hostname"))
        if "isSAP" in systemInformation["basic_environment"].keys():
            print("SLES Version: " + systemInformation["basic_environment"].get("slesVersion") + "-SP" + systemInformation["basic_environment"].get("patchLevel") + " [" + systemInformation["basic_environment"].get("isSAP") + "]")
        else:
             print("SLES Version: " + systemInformation["basic_environment"].get("slesVersion") + "-SP" + systemInformation["basic_environment"].get("patchLevel"))
        print("Installed Kernel: " + systemInformation["basic_environment"].get("kernelVersion"))

def main():

    short_options = "ho:f:vep"
    long_options = ["help", "output=", "file=", "verbose", "extract", "print"]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        #output error, and return with an error code
        print(str(err))
        sys,exit(2)

    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verbose"):
            print ("Enabling verbose mode")
        elif current_argument in ("-h", "--help"):
            print_banner()
            print("Usage: ./proactive_check arguments")
            print("=============================================================================")
            print("-----------------------------------------------------------------------------")
            print("long argument               short argument       obs               with value")
            print("-----------------------------------------------------------------------------")
            print("--help                       -h                                    no")
            print("--output                     -o                                    yes")
            print("--help                       -h                                    no")
            print("--extract                    -e                                    no")
            print("--print                      -p   ***  Run and print results ***   no")
            print("-----------------------------------------------------------------------------")
            print("Example of usage: ./proactive_check -p\n")
        elif current_argument in ("-e", "--extract"):
            extractSupportconfig()
        elif current_argument in ("-p"):
            print_formats()

#Uncomment for debug
#print_formats()

if __name__ == "__main__":
    main()

