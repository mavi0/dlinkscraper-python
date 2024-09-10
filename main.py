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
        
        for line in bnrinfo_rx:
            if "0 power" in line:
                self.__output['RX0'] = {}
                self.__output['RX0']["power"] = line.split("power: ")[1].split(" dBm,ecio:")[0]
                self.__output['RX0']["ecio"] = line.split("ecio: ")[1].split(" dB, rsrp:")[0]
                self.__output['RX0']["rsrp"] = line.split("rsrp: ")[1].split(" dBm, phase")[0]
                self.__output['RX0']["phase"] = line.split("phase: ")[1].split(" degree, sinr")[0]
                self.__output['RX0']["sinr"] = line.split("sinr: ")[1].split(" dB")[0]
            if "1 power" in line:
                self.__output['RX1'] = {}
                self.__output['RX1']["power"] = line.split("power: ")[1].split(" dBm,ecio:")[0]
                self.__output['RX1']["ecio"] = line.split("ecio: ")[1].split(" dB, rsrp:")[0]
                self.__output['RX1']["rsrp"] = line.split("rsrp: ")[1].split(" dBm, phase")[0]
                self.__output['RX1']["phase"] = line.split("phase: ")[1].split(" degree, sinr")[0]
                self.__output['RX1']["sinr"] = line.split("sinr: ")[1].split(" dB")[0]
            if "2 power" in line:
                self.__output['RX2'] = {}
                self.__output['RX2']["power"] = line.split("power: ")[1].split(" dBm,ecio:")[0]
                self.__output['RX2']["ecio"] = line.split("ecio: ")[1].split(" dB, rsrp:")[0]
                self.__output['RX2']["rsrp"] = line.split("rsrp: ")[1].split(" dBm, phase")[0]
                self.__output['RX2']["phase"] = line.split("phase: ")[1].split(" degree, sinr")[0]
                self.__output['RX2']["sinr"] = line.split("sinr: ")[1].split(" dB")[0]
            if "3 power" in line:
                self.__output['RX3'] = {}
                self.__output['RX3']["power"] = line.split("power: ")[1].split(" dBm,ecio:")[0]
                self.__output['RX3']["ecio"] = line.split("ecio: ")[1].split(" dB, rsrp:")[0]
                self.__output['RX3']["rsrp"] = line.split("rsrp: ")[1].split(" dBm, phase")[0]
                self.__output['RX3']["phase"] = line.split("phase: ")[1].split(" degree, sinr")[0]
                self.__output['RX3']["sinr"] = line.split("sinr: ")[1].split(" dB")[0]

        print(self.__output)

if __name__ == "__main__":
    scrape = Scrape()
    scrape.get_data()