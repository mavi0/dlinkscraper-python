import warnings
# no warnings, only dreams... and json
warnings.filterwarnings("ignore")

import os, json
from datetime import datetime
from telnetlib import Telnet
import urllib.request

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
            """
            Retrieves data from the CPE using TELNET and parses the output.

            Returns:
                None
                [but it prints the output as JSON]
            """
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
            # most of the data is comma separated
            bnrinfo_comma = bnrinfo.split(", ")
            # RX data is separated by RX
            bnrinfo_rx = bnrinfo.split("\nRX")

            # Just use regex, you say? I say, I'm lazy and this works but ALSO I'm not a masochist.
            # Also look at the go version of this which uses regexes, it's a mess. 
            # Because the output is a mess. And I'm a contradictory masochist.
            for line in bnrinfo_comma:
                if "NR BAND" in line:
                    self.__output['NR BAND'] = float(line.split(":")[1])
                if "EARFCN" in line:
                    self.__output['EARFCN'] = float(line.split("EARFCN:")[1].split(" ")[0])
                if "DL_bandwidth" in line:
                    self.__output['DL_bandwidth'] = float(line.split("DL_bandwidth:")[1].split("MHz")[0])
                if "physical cell ID" in line:
                    self.__output['physical cell ID'] = float(line.split("physical cell ID:")[1])
                if "averaged PUSCH TX power" in line:
                    self.__output['averaged PUSCH TX power'] = float(line.split(":")[1].split(" ")[0])
                if "averaged PUCCH TX power" in line:
                    self.__output['averaged PUCCH TX power'] = float(line.split(":")[1].split(" ")[0])
                if "RSRQ" in line:
                    self.__output['RSRQ'] = float(line.split("RSRQ ")[1].split(" ")[0])
                if "RSRP" in line:
                    self.__output['RSRP'] = float(line.split(":")[1].split(" dBm,ecio")[0])
                if "SINR" in line:
                    self.__output['SINR'] = float(line.split("SINR ")[1].split(" dB")[0])
                if "NR CQI" in line:
                    self.__output['NR CQI'] = float(line.split("NR CQI ")[1].split(",RANK")[0])
                if "RANK" in line:
                    self.__output['RANK'] = float(line.split(",RANK ")[1].split("\r")[0])
                if "Serving Beam SSB index" in line:
                    self.__output['Serving Beam SSB index'] = float(line.split("Serving Beam SSB index ")[1].split(",FR2")[0])
                if "FR2 serving Beam" in line:
                    self.__output['FR2 serving Beam'] = float(line.split("FR2 serving Beam:")[1].split(",")[0])
            
            # I know this looks like it could be a nested loop, but the output is cursed and just.. play spot the difference. 
            for line in bnrinfo_rx:
                if "0 power" in line:
                    self.__output['RX0'] = {}
                    self.__output['RX0']["power"] = float(line.split("power: ")[1].split(" dBm,ecio:")[0])
                    self.__output['RX0']["ecio"] = float(line.split("ecio: ")[1].split(" dB, rsrp:")[0])
                    self.__output['RX0']["rsrp"] = float(line.split("rsrp: ")[1].split(" dBm, phase")[0])
                    self.__output['RX0']["phase"] = float(line.split("phase: ")[1].split(" degree, sinr")[0])
                    self.__output['RX0']["sinr"] = float(line.split("sinr: ")[1].split(" dB")[0])
                if "1 power" in line:
                    self.__output['RX1'] = {}
                    self.__output['RX1']["power"] = float(line.split("power: ")[1].split(" dBm,ecio:")[0])
                    self.__output['RX1']["ecio"] = float(line.split("ecio: ")[1].split(" dB, rsrp:")[0])
                    self.__output['RX1']["rsrp"] = float(line.split("rsrp: ")[1].split(" dBm, phase")[0])
                    self.__output['RX1']["phase"] = float(line.split("phase: ")[1].split(" degree, sinr")[0])
                    self.__output['RX1']["sinr"] = float(line.split("sinr: ")[1].split(" dB")[0])
                if "2 power" in line:
                    self.__output['RX2'] = {}
                    self.__output['RX2']["power"] = float(line.split("power: ")[1].split(" dBm,ecio:")[0])
                    self.__output['RX2']["ecio"] = float(line.split("ecio: ")[1].split(" dB, rsrp:")[0])
                    self.__output['RX2']["rsrp"] = float(line.split("rsrp: ")[1].split(" dBm, phase")[0])
                    self.__output['RX2']["phase"] = float(line.split("phase: ")[1].split(" degree, sinr")[0])
                    self.__output['RX2']["sinr"] = float(line.split("sinr: ")[1].split(" dB")[0])
                if "3 power" in line:
                    self.__output['RX3'] = {}
                    self.__output['RX3']["power"] = float(line.split("power: ")[1].split(" dBm,ecio:")[0])
                    self.__output['RX3']["ecio"] = float(line.split("ecio: ")[1].split(" dB, rsrp:")[0])
                    self.__output['RX3']["rsrp"] = float(line.split("rsrp: ")[1].split(" dBm,phase: ")[0])
                    self.__output['RX3']["phase"] = float(line.split("phase: ")[1].split(" degree,sinr: ")[0])
                    self.__output['RX3']["sinr"] = float(line.split("sinr: ")[1].split(" dB")[0])

            # Print the output as JSON so it can be consumed by telegraf
            print(json.dumps(self.__output))

if __name__ == "__main__":
    scrape = Scrape()
    scrape.get_data()