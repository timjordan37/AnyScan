import enum

"""This System class will contain a Singleton class to manage the user settings per session"""

class ScanType(enum.Enum):
    full_scan = 0
    script_scan = 1
    udp_scan = 2
    fast_scan = 3
    detect_os_service_scan = 4

    @staticmethod
    def display_name_for_scan_type(type):
        displayNames = {
            0: "Full Scan",
            1: "Script Scan",
            2: "UDP Scan",
            3: "Fast Scan",
            4: "Detect OS Service Scan"
        }
        return displayNames[type]

    @staticmethod
    def scan_type_for_int(int):
        scan_types = {
            0: ScanType.full_scan,
            1: ScanType.script_scan,
            2: ScanType.udp_scan,
            3: ScanType.fast_scan,
            4: ScanType.detect_os_service_scan
        }
        return scan_types[int]

"""Singleton implementation: https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm"""
class Settings():
    """Properties"""
    __instance = None

    scan_type = ScanType.detect_os_service_scan

    """Methods"""
    @staticmethod
    def getInstance():
        """ Static access method. """
        if Settings.__instance == None:
            Settings()
        return Settings.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Settings.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self