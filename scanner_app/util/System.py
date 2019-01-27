import enum
import configparser

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
    def scan_type_for_int(scan_int):
        scan_types = {
            0: ScanType.full_scan,
            1: ScanType.script_scan,
            2: ScanType.udp_scan,
            3: ScanType.fast_scan,
            4: ScanType.detect_os_service_scan
        }
        return scan_types[int(scan_int)]

class SortType(enum.Enum):
    alphaASC = 0
    alphaDESC = 1


    @staticmethod
    def display_name_for_sort_type(type):
        displayNames = {
            0: "Alphabetical ASC",
            1: "Alphabetical DESC"
        }
        return displayNames[type]

    @staticmethod
    def sort_type_for_int(scan_int):
        sort_types = {
            0: SortType.alphaASC,
            1: SortType.alphaDESC
        }
        return sort_types[int(scan_int)]


class SettingKey():
    # Dictionary Keys
    setting_file_name = "settings.ini"
    config_key = "DEFAULT"

    # Settings Keys
    scan_type = "SCAN_TYPE"
    host_sort_type = "HOST_SORT_TYPE"
    vuln_sort_type = "VULN_SORT_TYPE"



"""Singleton implementation: https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm"""
class Settings():
    """Properties"""
    __instance = None

    """Methods"""
    # @staticmethod
    # def getInstance():
    #     """ Static access method. """
    #     if Settings.__instance == None:
    #         Settings()
    #     return Settings.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self

    @staticmethod
    def init_config():
        if not Settings.does_settings_file_exist():
            config = configparser.ConfigParser()
            config[SettingKey.config_key] = {
                SettingKey.scan_type: Settings.get_scan_type().value,
                SettingKey.host_sort_type: Settings.get_host_sort_type().value
            }

            with open(SettingKey.setting_file_name, 'w') as configfile:
                config.write(configfile)

    @staticmethod
    def does_settings_file_exist():
        config = configparser.ConfigParser()
        #  We need two 'not's here because 'not variable' will check if the file does not exist, and we want to know if
        #  it does exist, so we take another not to give us the correct value in context
        return not not config.read(SettingKey.setting_file_name)

    @staticmethod
    def get_settings_dict():
        config = configparser.ConfigParser()
        config.read(SettingKey.setting_file_name)
        return config[SettingKey.config_key]

    """Setting Methods"""

    """Scan Type"""
    @staticmethod
    def get_scan_type():
        if SettingKey.scan_type not in Settings.get_settings_dict():
            return ScanType.detect_os_service_scan

        scan_type_raw = Settings.get_settings_dict()[SettingKey.scan_type]
        return ScanType.scan_type_for_int(scan_type_raw)

    @staticmethod
    def set_scan_type(new_scan_type):
        config = configparser.ConfigParser()
        config.read(SettingKey.setting_file_name)
        config[SettingKey.config_key][SettingKey.scan_type] = str(new_scan_type.value)
        with open(SettingKey.setting_file_name, 'w') as configfile:
            config.write(configfile)

    """Host Sort Type"""

    @staticmethod
    def get_host_sort_type():
        if not SettingKey.host_sort_type in Settings.get_settings_dict():
            return SortType.alphaASC

        sort_type_raw = Settings.get_settings_dict()[SettingKey.host_sort_type]
        return SortType.sort_type_for_int(sort_type_raw)

    @staticmethod
    def set_host_sort_type(new_sort_type):
        config = configparser.ConfigParser()
        config.read(SettingKey.setting_file_name)
        config[SettingKey.config_key][SettingKey.host_sort_type] = str(new_sort_type.value)
        with open(SettingKey.setting_file_name, 'w') as configfile:
            config.write(configfile)