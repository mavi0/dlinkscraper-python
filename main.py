import time, os, errno, copy, re
import coloredlogs, logging
from pathlib import Path
from datetime import datetime
from time import sleep
from telnetlib import Telnet
import json
import paramiko
import cmd
import time
import sys
import csv
import urllib.request


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

class Scrape:
    def __init__(self):
        self.__time = datetime.now()
        # Try to load vars from env. If not, load defaults
        self.__cpe_uname = os.environ.get('CPE_USERNAME', "root")
        self.__cpe_passwd = os.environ.get('CPE_PASSWORD', "root")
        self.__cpe_hostname = os.environ.get('CPE_HOSTNAME', "192.168.100.1")
        self.__output = {}
        self.__output['datetime'] = self.__time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_data(self):
        # Call TELNET enable url on the CPE
        try:
            urllib.request.urlopen("http://" + self.__cpe_hostname + ":8000/atsq.txt")
        except Exception as e:
            pass

        # Connect to the CPE via TELNET and login
        tn = Telnet(self.__cpe_hostname)
        tn.read_until(b"login: ")
        tn.write(self.__cpe_uname.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(self.__cpe_passwd.encode('ascii') + b"\n")
        tn.read_until(b"~ # ")
        cmd = "atcli at+bnrinfo"
        tn.write(cmd.encode('ascii') + b"\n")
        bnrinfo = tn.read_until(b"OK")
        tn.close()

        print(bnrinfo)

        # Parse the output of the command and store it in the output dict
        bnrinfo = bnrinfo.decode('ascii')
        bnrinfo = bnrinfo.split("\n")
                

if __name__ == "__main__":
    scrape = Scrape()
    scrape.get_data()