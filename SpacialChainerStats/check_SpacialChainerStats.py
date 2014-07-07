#!/usr/bin/env python

"""
Description: Plugin to monitor spacial station running on a server.  It fetch the data from the website and process Stations-in-config value with Station-running value to find how many station are not running.

Author: 
    By: Olivier Contant olivier.contant@tritondigital.com
    Date: 2014-06-26

Last Update:
    By: Olivier Contant
    Date: 2014-06-29
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import pynagios
import lxml
import StringIO

from pynagios import Plugin
from lxml.html import parse, tostring, fromstring


def Usagemsg():
    print ('\n'
           'Program: check_SpacialChainerStats\n'
           '\n'
           '    Description: \n'
           '        Nagios check to monitor Spacial stations on chainer server.\n'
           '\n'
           '        The check monitor the number of configured station and the number of running station.\n'
           '        If % of station are not running compare to configured station, it will raise the alert.\n'
           '\n'
           '    Some help on valid Range:\n'
           '        Range are by default Exclusif: \n'
           '            Ex.: A range of 10:20 will match values that are < 10 OR >20.\n'
           '        Adding a "@" before the range means the range is inclusive.\n'
           '            Ex.: @10:20 is valid in the case that the value is >= 10 AND <= 20.\n'
           '        If start is not given, then it is assumed to be 0.\n'
           '        If end is not given, but start (x:) exists, then end is assumed to be infinity.\n'
           '            Ex.: (5:) would match < 5.\n'
           '\n\n'

           '    Usage: check_SpacialChainerStats [-(c)(w)(H)h]\n'
           '    ** Where ( ) are mandatory options\n'
           '\n'
           '    Where:\n'
           '        -c = Critical Range - Ex.: 10:20\n'
           '        -w = Warning Range - Ex.: 0:30\n'
           '        -H = Hostname - This should be the host that this check targets.\n'
           '        -t = TimeOut  - This is an int value for the timeout of this check.\n'
           '        -v = verbosity - Where additional v means more verbosity.\n'
           '        -h = Help - display this message\n'
           '\n'
           '    Author: Olivier Contant (contant.olivier@tritondigital.com)\n'
           "\n"
    )


# Calculate the number of running stations compare to the total number of stations.
class CheckSpacialStation(Plugin):
    """
    Check if value are inside normal range or will raise an alert.
    pynagios module do most of the jobs, we only set the value to compare with check value range.
    """

    StationNotRunning = None

    def CheckStation(self, StationInConfig, StationRunning):
        StationNotRunning = (int(StationRunning) * 100) / int(StationInConfig)
        return self.response_for_value(StationNotRunning, message="Station running: %s%s.  Number of Station is %s and running is %s. " % (StationNotRunning, '%', StationInConfig, StationRunning))


"""
Fetch the value from the website
Get the webpage data
"""
def GetPage(url):
    return parse(url).getroot()


# Find the span class title Stations-in-config and isolate the value
def FetchStationsInConfig(doc):
    for data in doc.xpath('/html/body/div/div[5]/div[3]/span[2]'):
        return data.text_content()


# Find the span class title Stations-running and isolate the value
def FetchStationRunning(doc):
    for data in doc.xpath('/html/body/div/div[5]/div[4]/span[2]'):
        return data.text_content()


def isempty(var_in):
    if var_in == None:
        return True
    else:
        return False


if __name__ == "__main__":
    # Declare variables, basics to validate if variables are set correctly later.
    StationInConfig = None
    StationRunning = None
    HostName = None
    doc = None
    url = None

    # Get the url of the website
    HostName = CheckSpacialStation().options.hostname
    if isempty(HostName):
        print "\nERROR: A hostname is required to get value ( Use -H [hostname] )\n\n"
        Usagemsg()
        sys.exit(1)
    HostName = HostName.replace('.spacial.int', '')

    # Set the URL to fetch Value from. *No need to validate*
    url = "http://208.80.53.113/chainer-stats-new.php?server=%s" % (HostName)

    # Get the whole page data
    doc = GetPage(url)
    if isempty(doc):
        print "\nERROR: Doc is empty\n\n"
        sys.exit(1)

    # Get Value from WebPage.
    StationInConfig = FetchStationsInConfig(doc)
    StationRunning = FetchStationRunning(doc)
    if isempty(StationInConfig) or isempty(StationRunning):
        print "\nERROR: One of Station value is empty\n\n"
        sys.exit(1)

    # Instantiate the plugin pynagios and check our value, and then exit   
    CheckSpacialStation().CheckStation(StationInConfig, StationRunning).exit()
