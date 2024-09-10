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

        # Parse the output of the command and store it in the output dict
        bnrinfo = bnrinfo.decode('ascii')
        bnrinfo = bnrinfo.split(", ")

        # bnrinfo = ['atcli at+bnrinfo\r', '\r\r', 'NR BAND:77, EARFCN:673344 DL_bandwidth:100MHz\r\r', 'physical cell ID:431, averaged PUSCH TX power :1 dBm, averaged PUCCH TX power :129 dBm, \r\r', 'RX Power Info:\r\r', 'RSRQ -15 dB, RSRP -81 dBm,SINR -1 dB\r\r', 'RX0 power: -65 dBm,ecio: -13 dB, rsrp: -79 dBm, phase: 0 degree, sinr: -1 dB\r\r', 'RX1 power: -67 dBm,ecio: -18 dB, rsrp: -85 dBm, phase: 0 degree, sinr: -4 dB\r\r', 'RX2 power: -66 dBm,ecio: -18 dB, rsrp: -85 dBm, phase: 0 degree, sinr: -7 dB\r\r', 'RX3 power: -72 dBm,ecio: -13 dB, rsrp: -86 dBm,phase: 0 degree,sinr: -2 dB\r\r', 'NR CQI 10,RANK 2\r\r', 'Serving Beam SSB index 1,FR2 serving Beam:255,255\r\r', '\r\r', '\r\r', 'OK']

        # for line in bnrinfo:
        #     if "NR BAND" in line:

        

        print(bnrinfo)


                

if __name__ == "__main__":
    scrape = Scrape()
    scrape.get_data()