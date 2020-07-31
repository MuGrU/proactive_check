#!/usr/bin/env python
# coding: utf-8

import json, re, requests, sys, os, getopt
import vercheck as vercheck

# static product list (taken from RMT and other sources)
product_list = {
    1117: { 'name': 'SUSE Linux Enterprise Server 12 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:12' },
    1118: { 'name': 'SUSE Linux Enterprise Desktop 12 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:12' },
    1322: { 'name': 'SUSE Linux Enterprise Server 12 SP1 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:12:sp1' },
    1333: { 'name': 'SUSE Linux Enterprise Desktop 12 SP1 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:12:sp1' },
    1357: { 'name': 'SUSE Linux Enterprise Server 12 SP2 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:12:sp2' },
    1358: { 'name': 'SUSE Linux Enterprise Desktop 12 SP2 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:12:sp2' },
    1421: { 'name': 'SUSE Linux Enterprise Server 12 SP3 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:12:sp3' },
    1425: { 'name': 'SUSE Linux Enterprise Desktop 12 SP3 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:12:sp3' },
    1625: { 'name': 'SUSE Linux Enterprise Server 12 SP4 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:12:sp4' },
    1629: { 'name': 'SUSE Linux Enterprise Desktop 12 SP4 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:12:sp4' },
    1878: { 'name': 'SUSE Linux Enterprise Server 12 SP5 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:12:sp5' },
    1319: { 'name': 'SUSE Linux Enterprise Server for SAP 12 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:12' },
    1346: { 'name': 'SUSE Linux Enterprise Server for SAP 12 SP1 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:12:sp1' },
    1414: { 'name': 'SUSE Linux Enterprise Server for SAP 12 SP2 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:12:sp2' },
    1426: { 'name': 'SUSE Linux Enterprise Server for SAP 12 SP3 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:12:sp3' },
    1755: { 'name': 'SUSE Linux Enterprise Server for SAP 12 SP4 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:12:sp4' },
    1880: { 'name': 'SUSE Linux Enterprise Server for SAP 12 SP5 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:12:sp5' },
    1575: { 'name': 'SUSE Linux Enterprise Server 15 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:15' },
    1609: { 'name': 'SUSE Linux Enterprise Desktop 15 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:15' },
    1763: { 'name': 'SUSE Linux Enterprise Server 15 SP1 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:15:sp1' },
    1764: { 'name': 'SUSE Linux Enterprise Desktop 15 SP1 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:15:sp1' },
    1939: { 'name': 'SUSE Linux Enterprise Server 15 SP2 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles:15:sp2' },
    1935: { 'name': 'SUSE Linux Enterprise Desktop 15 SP2 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sled:15:sp2' },
    1612: { 'name': 'SUSE Linux Enterprise Server for SAP 15 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:15' },
    1766: { 'name': 'SUSE Linux Enterprise Server for SAP 15 SP1 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:15:sp1' },
    1941: { 'name': 'SUSE Linux Enterprise Server for SAP 15 SP2 x86_64', 'arch': 'x86_64', 'identifier': 'cpe:/o:suse:sles_sap:15:sp2' },
}

def check_SLESversion():
    # Collect CPE_NAME and matches on product_list
    #CPE_NAME="cpe:/o:suse:sles_sap:12:sp4"

    regex = r"CPE_NAME=\"(.*)\""
    try:
        f = open('./basic-environment.txt', 'r')
        data = f.read()
        f.close()

        matches = re.search(regex, data)
        for p in product_list:
            if matches.group(1) == product_list[p]['identifier']:
                return p
    except Exception as e:
        print('error: {}'.format(str(e)))
    return -1

def print_banner():
    """
    ================================================================================
                    Proactive_Check Utility - Supportconfig
                             Script Version: (version)
                            Script Date: [YYYY-MM-DD]
    ================================================================================
    """
    script = 'Proactive_Check Utility - Supportconfig'
    version = 'Script Version: (beta)'
    date = 'Script Date: 2020-07-19'

    print('{:=>80}'.format('='))
    print('{:^80}'.format(script))
    print('{:^80}'.format(version))
    print('{:^80}'.format(date))
    print('{:=>80}\n'.format('='))

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]

def extractSupportconfig():
    tarCommand = 'tar xvJf /home/toliveira/github/proactive_check/supportconfigs/nts_linux-ivcd_200718_2314.txz'
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

def crawlingSupportconfig():
    # Collect and parse information from supportconfig txt files

    systemInformation = basic_environment()
    #Debug
    #print(json.dumps(systemInformation, sort_keys=False, indent=4))
    return systemInformation

def basic_environment():
    #Collect useful information from basic_environment.txt

    with open('./basic-environment.txt_sap') as f:
        systemInformation = {}
        data = f.read()
        hostname = re.search('(Linux\s)([\D*]*)(.*)', data).group(2)
        uname = re.search('(Linux\s)([\D*]*)(.*)', data).group(3)

        # Check SLES version based on product_list (hardcoded)
        prod_id = check_SLESversion()
        slesVersion = product_list[prod_id]['name']

        # kernelVersion = re.search('\d.*\.\d.*\d.*\-\d.*\.\d...', data).group().replace('-d', '.1')

        # I need do discovery the properly regex for kernelVersion, I tried https://regex101.com/r/osKVNU/1 and group(3) and no donuts
        kernelVersion = re.search('(Linux\s)([\D]+)([\.\-\w]+)', data).group(3)

        patchLevel = re.search('PATCHLEVEL = ([\d]+)', data).group(1)

        #Debug
        #print(json.dumps(dataKernel, sort_keys=False, indent=4))

        systemInformation['basic_environment'] = {
            'hostname': hostname,
            'uname': uname,
            'slesVersion': slesVersion,
            'patchLevel': patchLevel,
            'kernelVersion': kernelVersion
        }

    return systemInformation

def print_formats():
    systemInformation = crawlingSupportconfig()

    #Run the script and prints on <STDOUT> collored
    def sto_print():

        #Defining collors to use for print format
        TGREEN = '\033[32m'  # Green Text
        ENDC = '\033[m'      # Reset to Defaults
        TRED = '\033[31m'    # Red Text

        # Only for test purpose, needed to code test condition on crawlingSupportconfig()
        isSupported = False

        print_banner()
        """
        # print_banner()
        ========================================================================
                 Proactive_Check Utility - Supportconfig                     
                          Script Version: (beta)                             
                         Script Date: 2020-07-19                             
        ========================================================================
        #<header>
        [SLES Version]
        SUSE Linux Enterprise Server 12 SP4 x86_64             [ NOT SUPPORTED ]                                                               
        #</header>______________________________________________________________
        """
        if isSupported == False:

            #Searching for latest kernel version on https://scc.suse.com/api/package_search/packages?product_id={}

            prod_id = check_SLESversion()
            kernelVersion = str(systemInformation['basic_environment'].get('kernelVersion'))
            latestkenel = str(vercheck.latestkKernel(prod_id))
            print('\nServer Information:\n{:=>19}\n'.format('='))
            print('[HOSTNAME]: {0:}\n'.format(systemInformation['basic_environment'].get('hostname')))
            # <header>

            #Mask of the print
            #{1:} = [SLES Version]
            #{0:<62} = SUSE Linux Enterprise Server 12 SP4 x86_64
            #{4} = TRED
            #{2:<80} = [NOT SUPPORTED]
            #{5} = EDNC
            #{3:_>80} = </header>
            print('{1:}\n{0:<62}{4}{2:<80}\n{5}{3:_>80}\n'.format(systemInformation['basic_environment'].get('slesVersion'), '[SLES Version]', '[ OUT OF SUPPORT ]', '_', TRED, ENDC))
            # </header>

            #Debug
            #print('kv'.format(kernelVersion))
            #print(type(kernelVersion))
            #print('lk'.format(latestkenel))
            #print(type(latestkenel))

            #Needed to change the logic, just for test purpose
            if latestkenel != kernelVersion:
                print('\n[KERNEL TEST]')

                # Mask of the print
                # {3:=>80} = '.'
                # {2:.<49} = '[ FAILED ]'
                # [{1}] = Latest Kernel: '[4.12.14-95.54.1]'
                # {2:.<40} = '.'

                # Needed to check if -default can be replaced always by .1
                # [{0}] = Installed Kernel: '[4.12.14-94.41-default]'

                print('{3:.>80}\n\nLatest Kernel:{2:.<49}[{1}]\nInstalled Kernel:{2:.<40}[{0}]\n'.format(kernelVersion, latestkenel, '.', '[ FAILED ]'))
            else:
                print('Coming soon ! =)')
                #print('Installed Kernel:{1:.<80}]{1:.<80}{3:<80}'.format(systemInformation['basic_environment'].get('kernelVersion')), '-' , '[ PASSED ]')
            print('\n\n[Completed!\n')
    #Debug
    sto_print()

def main():

    short_options = 'ho:f:vep'
    long_options = ['help', 'output=', 'file=', 'verbose', 'extract', 'print', 'dir']

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        #output error, and return with an error code
        print(str(err))
        sys, exit(2)

    for current_argument, current_value in arguments:
        if current_argument in ('-v', '--verbose'):
            print ('Enabling verbose mode')
        elif current_argument in ('-h', '--help'):
            print_banner()

            #Nedded to port to Python3
            middle = '-'*80
            bottom = '='*80

            print('{:=>80}'.format('='))
            print('long argument          short argument              obs                with value')
            print('{:->80}'.format('-'))
            print('--help                       -h                                               no')
            print('--output                     -o                                              yes')
            print('--help                       -h                                               no')
            print('--extract                    -e                                               no')
            print('--print                      -p       ***  Run and print results ***          no')
            print('{:=>80}'.format('-'))
            print('Example of usage: ./proactive_check -p\n'.format())
            print('{:=>80}'.format('='))
        elif current_argument in ('-e', '--extract'):
            extractSupportconfig()
        elif current_argument in ('-p'):
            print_formats()

#Uncomment for debug
#print_formats()

if __name__ == '__main__':
    main()

