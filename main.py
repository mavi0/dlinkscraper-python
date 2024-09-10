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
        bnrinfo_comma = bnrinfo.split(", ")
        bnrinfo_rx = bnrinfo.split("\nRX")

        # bnrinfo = ['atcli at+bnrinfo\r\n\r\r\nNR BAND:77', 'EARFCN:673344 DL_bandwidth:100MHz\r\r\nphysical cell ID:431', 'averaged PUSCH TX power :1 dBm', 'averaged PUCCH TX power :4 dBm', '\r\r\nRX Power Info:\r\r\nRSRQ -14 dB', 'RSRP -79 dBm,SINR 0 dB\r\r\nRX0 power: -66 dBm,ecio: -14 dB', 'rsrp: -80 dBm', 'phase: 0 degree', 'sinr: 0 dB\r\r\nRX1 power: -67 dBm,ecio: -17 dB', 'rsrp: -84 dBm', 'phase: 0 degree', 'sinr: -4 dB\r\r\nRX2 power: -66 dBm,ecio: -16 dB', 'rsrp: -83 dBm', 'phase: 0 degree', 'sinr: -4 dB\r\r\nRX3 power: -72 dBm,ecio: -16 dB', 'rsrp: -88 dBm,phase: 0 degree,sinr: -3 dB\r\r\nNR CQI 12,RANK 2\r\r\nServing Beam SSB index 1,FR2 serving Beam:255,255\r\r\n\r\r\n\r\r\nOK']
        
        for line in bnrinfo_comma:
            if "NR BAND" in line:
                self.__output['NR BAND'] = line.split(":")[1]
            if "EARFCN" in line:
                self.__output['EARFCN'] = line.split("EARFCN:")[1].split(" ")[0]
            if "DL_bandwidth" in line:
                self.__output['DL_bandwidth'] = line.split("DL_bandwidth:")[1].split("MHz")[0]
            if "physical cell ID" in line:
                self.__output['physical cell ID'] = line.split("physical cell ID:")[1]
            if "averaged PUSCH TX power" in line:
                self.__output['averaged PUSCH TX power'] = line.split(":")[1].split(" ")[0]
            if "averaged PUCCH TX power" in line:
                self.__output['averaged PUCCH TX power'] = line.split(":")[1].split(" ")[0]
            if "RSRQ" in line:
                self.__output['RSRQ'] = line.split("RSRQ ")[1].split(" ")[0]
            if "RSRP" in line:
                self.__output['RSRP'] = line.split(":")[1].split(" dBm,ecio")[0]
            if "SINR" in line:
                self.__output['SINR'] = line.split(":")[1].split(" dBm,ecio")[0]
            if "NR CQI" in line:
                self.__output['NR CQI'] = line.split(" ")[1]
            if "RANK" in line:
                self.__output['RANK'] = line.split(" ")[1]
            if "Serving Beam SSB index" in line:
                self.__output['Serving Beam SSB index'] = line.split(" ")[1]
            if "FR2 serving Beam" in line:
                self.__output['FR2 serving Beam'] = line.split(" ")[1]
        

        # print(bnrinfo)

        print(self.__output)

        print(bnrinfo_rx)


                

if __name__ == "__main__":
    scrape = Scrape()
    scrape.get_data()