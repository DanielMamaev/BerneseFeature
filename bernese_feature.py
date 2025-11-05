import datetime
import itertools
import os
import string
import subprocess
from gps_time import GPSTime


class Bernese52:
    """
    Exaples:
    >>> list_stations = {
        'BADG': {
            "xyz": [-838281.8740,  3865775.9807,  4987625.1818],
            'mark_num': "12338M002",
            "plate": "EURA",
            "rcv_type": "JAVAD TRE_3 DELTA",
            "ant_type": "JAVRINGANT_DM   JVDM",
            "ant_HEN": [0.0280, 0.0000, 0.0000]
        },
        "NOVM": {
            "xyz": [452260.6946,  3635877.6761,  5203453.4274],
            'mark_num': "12367M002",
            "plate": "EURA",
            "rcv_type": "JPS LEGACY",
            "ant_type": "JPSREGANT_SD_E1 NONE",
            "ant_HEN": [0.0800, 0.0000, 0.0000]
        }
    }
    """
    def __init__(self, list_stations: dict[str, dict[str, list]]):
        self.list_stations = list_stations.copy()

    def make_bql_input(self):
        print("====== BQL ======")
        output = ''
        for name, val in self.list_stations.items():
            output += f"{name} {val['mark_num']:<19} {val["xyz"][0]:15.3f} {val["xyz"][1]:15.3f} {val["xyz"][2]:15.3f}\n"
        print(output)
        return output

    def make_PLD_info(self):
        print("====== PLD ======")
        output = ''
        count = 1
        for name, meta in self.list_stations.items():
            output += f"{count:3}  {name} {meta["mark_num"]:9s} \t {"":13}  {"":13}  {"":13} \t{"":6} {meta["plate"]}\n"
            count += 1
        print(output)
        return output

    def make_STA_tab_001_info(self):
        print("====== STA_001 ======")
        output = ''
        for name, meta in self.list_stations.items():
            output += f"{name:4} {meta["mark_num"]:11}      {"001":3}  {"":40}  {name+"*":20}  {"":24}\n"
        print(output)
        return output

    def make_STA_tab_002_info(self):
        print("====== STA_002 ======")
        output = ''
        for name, meta in self.list_stations.items():
            ant_NEH = meta["ant_HEN"][::-1]
            output += f"{name:4} {meta["mark_num"]:11}      {"001":3}  {"":40}  {meta["rcv_type"]:20}  {"":20}  {"999999":6}  {meta['ant_type']:20}  {"":20}  {"999999":6}  {ant_NEH[0]:8.4f}  {ant_NEH[1]:8.4f}  {ant_NEH[2]:8.4f}  {"":22}  {"":24}\n"
        print(output)
        return output
    
    def make_CLU_info(self):
        print("====== CLU ======")
        output = ''
        for name, meta in self.list_stations.items():
            output += f"{name:4} {meta["mark_num"]:11}  {"1":>3}\n"
        print(output)
        return output

    def make_ABB_info(self):
        print("====== ABB ======")
        output = ''
        alph = string.ascii_uppercase
        combinations = [''.join(pair) for pair in itertools.product(alph, repeat=2)]
        count = 0
        for name, meta in self.list_stations.items():
            output += f"{name:4} {meta["mark_num"]:11}         {name:4}     {combinations[count]:2}     {"":39}\n"
            count += 1
        print(output)
        return output  

    def make_RECEIVER(self, file_receiver: str):
        print("====== CHECK RECEIVERS ======")
        output = set()
        with open(file_receiver, "r", encoding="utf-8") as f:
            text = f.read()
            for name, val in self.list_stations.items():
                if val['rcv_type'] in text:
                    print(f"{val['rcv_type']} - OK")
                else:
                    output.add(val['rcv_type'])
                    print(f"{val['rcv_type']} - MISSING")
        print(output)

        result = self._make_RECEIVER_text(list(output))
        print(result)
        return list(output), result

    @staticmethod
    def _make_RECEIVER_text(list_receivers: list):
        print("====== RECEIVER ======")
        output = ""
        for rec in list_receivers:
            output += f"{rec:20}   {2}     C1    L1:     1     GR\n"
            output += f"{'':20}   {" "}     X2    L2:     1     \n\n"
        return output

    def apriopy_CRD(self):
        print("====== CRD ======")
        output = "TEMP: coordinate list                                           23-AUG-22 08:30\n" \
                 "--------------------------------------------------------------------------------\n"\
                 "LOCAL GEODETIC DATUM: TEMP           EPOCH: 2015-01-01 00:00:00\n\n" \
                 "NUM  STATION NAME           X (M)          Y (M)          Z (M)     FLAG     SYSTEM\n\n"
    
        count = 1
        for name, val in self.list_stations.items():
            output += f"{count:3}  {name} {val['mark_num']:9}   {val['xyz'][0]:14} {val['xyz'][1]:14} {val['xyz'][2]:14}    IGS20\n"
            count += 1
        print(output)
        return output

    @staticmethod
    def rename_COD_yyddd2wwwwd(dir_path: str):
        files = os.listdir(dir_path)
        for name in files:
            if "ERP" in name:
                continue
            dt = datetime.datetime.strptime(name[3:8], "%y%j")
            gps_week = GPSTime.from_datetime(dt).week_number
            gps_day = int(GPSTime.from_datetime(dt).time_of_week / (24 * 60 * 60))
            new_name = name[:3] + str(gps_week) + str(gps_day) + name[8:]
            os.rename(os.path.join(dir_path, name), os.path.join(dir_path, new_name))
        
    @staticmethod
    def unzip(dir_path: str):
        """Unzip .gz and .Z. Only Linux"""
        files = os.listdir(dir_path)
        for name in files:
            if name.endswith((".gz", ".Z")):
                input_path_file = os.path.join(dir_path, name)
                subprocess.run(["uncompress", input_path_file])

    @staticmethod
    def rename_COD_rnx3_to_rnx2(dir_path: str, type_file: str):
        files = os.listdir(dir_path)
        for name in files:
            if not name.endswith(type_file):
                continue
            dt = datetime.datetime.strptime(name.split("_")[1][:7], "%Y%j")
            gps_week = GPSTime.from_datetime(dt).week_number
            gps_day = int(GPSTime.from_datetime(dt).time_of_week / (24 * 60 * 60))

            suffix = ""
            if type_file == "SP3":
                suffix = ".SP3"
            elif type_file == "ION":
                suffix = ".ION"
            else:
                print(f"Неизвестный тип файла {type_file}")
            
            new_name = name[:3] + str(gps_week) + str(gps_day) + suffix
            os.rename(os.path.join(dir_path, name), os.path.join(dir_path, new_name))
