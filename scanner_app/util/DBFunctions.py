import ntpath
import sqlite3
import json
from pathlib import Path
from tkinter.filedialog import askopenfilename


class DBFunctions:

    # todo create docstrings for all functions
    # Saves a new device to the database
    @staticmethod
    def save_device(deviceName, deviceManufacturer, cpeURI):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        device_info = (deviceName, deviceManufacturer, cpeURI)

        print('Inside DBFunctions save_device')
        print(device_info)

        try:
            cursor.execute('''INSERT INTO Devices VALUES(?, ?, ?)''', device_info)
            conn.commit()
        except sqlite3.IntegrityError as e:
            return False

        return True

    # Saving a Vulnerability to the database
    @staticmethod
    def save_vulnerability(cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                           customScoreReason, privilegesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(VulnID) FROM Vulnerabilities')
        conn.commit()
        maxIDTuple = cursor.fetchone()

        # print("LOOK TUPLE: ", maxIDTuple)

        maxID = maxIDTuple[0]

        if maxID is None:
            maxID = 0

        vulnID = maxID + 1

        vulnerability_info = (vulnID, cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                              customScoreReason, privilegesRequired,
                              userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                              baseScore, baseSeverity, exploitabilityScore)
        try:
            cursor.execute('''INSERT INTO Vulnerabilities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           vulnerability_info)
            conn.commit()
        except sqlite3.IntegrityError:
            return False

        return True

    # Updates a Vulnerability in the DB
    @staticmethod
    def update_vuln(vulnID, cveName, description, CVSSScore, attackVector, attackComplexity, customScore,
                           customScoreReason, privilegesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           baseScore, baseSeverity, exploitabilityScore):
        conn = sqlite3.connect("vulnDB.db")
        cursor = conn.cursor()

        vulnerability_info = (cveName, description, attackVector, attackComplexity, customScore,
                              customScoreReason, privilegesRequired,
                              userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                              baseScore, baseSeverity, exploitabilityScore, vulnID)

        cursor.execute('''UPDATE Vulnerabilities 
                        SET 
                        cveName = ?,
                        description = ?,
                        attackVector = ?,
                        attackComplexity = ?,
                        customScore = ?,
                        customScoreReason = ?,
                        priviligesRequired = ?,
                        userInteraction = ?,
                        confidentialityImpact = ?,
                        integrityImpact = ?,
                        availabilityImpact = ?,
                        baseScore = ?,
                        baseSeverity = ?,
                        exploitabilityScore = ? 
                        WHERE VulnID = ?''', vulnerability_info)
        conn.commit()


    # Saves a scan to the database
    @staticmethod
    def save_scan(Date, Duration):
        """Save a scan to the Db

        :param Date: date of scan to be imported
        :param Duration: time scan took to complete
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(ScanID) FROM ScanHistory')
        conn.commit()

        maxIDTuple = cursor.fetchone()
        maxID = 0
        if maxIDTuple is not None and maxIDTuple[0] is not None:
            maxID = maxIDTuple[0]
            maxID += 1

        scanID = maxID

        scan_info = (scanID, Date, Duration)
        cursor.execute('''INSERT INTO ScanHistory VALUES(?, ?, ?)''', scan_info)
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def build_db():
        """Build database"""
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE Devices (Model TEXT PRIMARY KEY,
             Manufacturer TEXT, 
             cpeURI TEXT)''')
        cursor.execute('''CREATE TABLE CPEVulns (
            cpeURI TEXT, 
            cveName TEXT, 
            PRIMARY KEY(cpeURI, cveName))''')
        conn.commit()
        cursor.execute('''CREATE TABLE Vulnerabilities (VulnID INTEGER PRIMARY KEY, 
            cveName TEXT,
            description TEXT, 
            CVSSScore INTEGER, 
            attackVector TEXT, 
            attackComplexity TEXT, 
            customScore TEXT, 
            customScoreReason TEXT,
            priviligesRequired TEXT, 
            userInteraction TEXT, 
            confidentialityImpact TEXT, 
            integrityImpact TEXT, 
            availabilityImpact TEXT,
            baseScore TEXT, 
            baseSeverity TEXT, 
            exploitabilityScore INTEGER)''')
        cursor.execute('''CREATE TABLE ScanHistory (ScanID INTEGER PRIMARY KEY, 
            ScanDate TEXT, 
            Duration INTEGER)''')
        cursor.execute('''CREATE TABLE Hosts (HostID INTEGER PRIMARY KEY, 
            ip TEXT, 
            macAddress TEXT, 
            osFamily TEXT, 
            osGen TEXT, name TEXT, 
            vendor TEXT, 
            ScanID INTEGER, 
            FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
        conn.commit()
        cursor.execute('''CREATE TABLE Parameters (ScanID INTEGER, 
            ParameterValue TEXT, 
            ParameterType TEXT, 
            PRIMARY KEY(ScanID, ParameterType))''')
        cursor.execute('''CREATE TABLE PenTestHistory (PenTestID INTEGER PRIMARY KEY, 
            VulnID INTEGER, 
            Model TEXT,
            ScanID INTEGER, 
            Result TEXT, 
            FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), 
            FOREIGN KEY(Model) REFERENCES Devices(Model), 
            FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
        conn.commit()

    @staticmethod
    def save_host(host, scanID):
        """Saves a scan to the database

        :param host: host name
        :param scanID: scan ID
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(HostID) FROM Hosts')
        conn.commit()
        maxIDTuple = cursor.fetchone()
        maxID = 0
        if maxIDTuple is not None and maxIDTuple[0] is not None:
            maxID = maxIDTuple[0]
            maxID += 1

        hostID = maxID
        scan_info = (hostID, host._ip, host._macAddress, host._osFamily, host._osGen, host._name, host._vendor, scanID)
        cursor.execute('''INSERT INTO Hosts VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', scan_info)
        conn.commit()

    @staticmethod
    def save_cpeVuln(cpe, cve):
        """Saves a new cpe\cve combo into the cpeVulns table
        :param cpe: cpe to import to db
        :param cve; cve to import to db
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cpeVuln = (cpe, cve)

        cursor.execute('''INSERT INTO CPEVulns VALUES (?, ?)''', cpeVuln)
        conn.commit()

    def query_cves(cpe_dict):
        """query DB for CVEs according to CPEs found by scanner

        :param cpe_dict: cpe dictionary in the form {host0 : [cpe, list0], host1: [cpe, list1]
        """
        conn = sqlite3.connect('vulnDB.db')
        cves = []
        test_data = set()
        cursor = conn.cursor()
        print("CVE Query HERE")

        # CP = ["cpe:2.3:o:juniper:junos:12.1x46:d10:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d15:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d20:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d25:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d30:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d35:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d40:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d45:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d50:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d55:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d60:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.1x46:d65:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3x48:d10:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3x48:d15:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3x48:d20:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3x48:d25:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3x48:d30:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x49:d10:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x49:d20:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x49:d30:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d20:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d21:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d25:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d30:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d32:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d33:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d34:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d61:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d62:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1x53:d63:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1:*:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1:r1:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1:r2:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1:r3:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1:r4:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1:r8:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1:r9:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.2:r1:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.2:r2:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.2:r3:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.2:r4:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.2:r5:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.2:r7:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.2:r8:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1:r1:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:15.1:r2:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:*:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r1:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r10:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r2:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r3:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r4:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r5:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r6:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r7:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r8:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:12.3:r9:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:*:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d10:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d15:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d16:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d25:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d26:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d27:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d35:*:*:*:*:*:*",
        #         "cpe:2.3:o:juniper:junos:14.1x53:d50:*:*:*:*:*:*"]
        #
        # for cps in CP:
        #     cursor.execute("""SELECT * FROM CPEVulns WHERE cpeURI IS (?)""", (cps,))
        #     test_str = cursor.fetchone()
        #     if test_str:
        #         cves.append(test_str[1])
        #     else:
        #         print("NOT FOUND")
        # return cves
        # todo delete static testing to test on imported db

        cursor.execute('''SELECT cveName FROM CPEvulns''')
        for row in cursor:
            test_data.add(row[0])

        return test_data

        # for hList in cpe_dict:
        #     for cpe in cpe_dict[hList]:
        #         cursor.execute("""SELECT * FROM CPEVulns WHERE cpeURI IS (?)""", (cpe,))
        #         vul = cursor.fetchone()
        #         if vul:
        #             cves.append(vul[1])
        # return all the fun stuff
        # return cves

    @staticmethod
    def query_vulns(cve):
        """Query the database for a specific vulnerability

        :param cve: vulnerability to be searched for
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        print("Vuln Query HERE")
        cursor.execute("""SELECT * FROM Vulnerabilities WHERE cveName IS (?)""", (cve,))
        return cursor.fetchone()

    @staticmethod
    def query_report_info():
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()
        # cursor4 = conn.cursor()

        # todo change query to needed data
        #
        cursor.execute("""SELECT ip FROM Hosts""")
        cursor2.execute("""SELECT macAddress FROM Hosts""")
        cursor3.execute("""SELECT name FROM Hosts""")
        # I fixed this, but we'll want to add a range of baseScore vulns to the DB to test
        # Also, if baseScore isn't a number I'm pretty sure sqlite will consider it bigger no matter what
        # We will want to test what happens there too  
        # cursor4.execute("""SELECT * FROM Vulnerabilities WHERE baseScore >= 7.0""")
        results = (cursor.fetchall(), cursor2.fetchall(), cursor3.fetchall())
        return results

    # Imports Data from NVD JSON file
    @staticmethod
    def import_NVD_JSON():

        json_fp = Path("nvdcve-1.0-2019.json")
        nvd_json = json.loads(json_fp.read_text())
        cve_items_list = nvd_json['CVE_Items']

        i = 0
        for cve in cve_items_list:
            cve_detail = cve_items_list[i]
            cve_meta_data = cve_detail.get("cve").get("CVE_data_meta")

            description_data = cve_detail.get("cve").get("description").get("description_data")
            description = description_data[0].get("value")

            configurations = cve_detail['configurations']
            cpe_list = configurations['nodes']

            try:
                cvssV3 = cve_detail.get("impact").get("baseMetricV3").get("cvssV3")
                baseMetric = cve_detail.get("impact").get("baseMetricV3")
                DBFunctions.save_vulnerability(cve_meta_data['ID'], description, cvssV3['attackVector'],
                                               cvssV3['attackComplexity'], "", "", cvssV3['privilegesRequired'],
                                               cvssV3['userInteraction'],
                                               cvssV3['confidentialityImpact'], cvssV3['integrityImpact'],
                                               cvssV3['availabilityImpact'],
                                               cvssV3['baseScore'], cvssV3['baseSeverity'],
                                               baseMetric['exploitabilityScore'])
            except:
                DBFunctions.save_vulnerability(cve_meta_data['ID'], description, "N/A", "N/A", "", "", "N/A",
                                               "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")
            for item in cpe_list:
                try:
                    cpe_match = item['cpe_match']
                    for item in cpe_match:
                        try:
                            cpe_URI = item['cpe23Uri']
                        except:
                            cpe_URI = item['cpe22Uri']
                        DBFunctions.save_cpeVuln(cpe_URI, cve_meta_data['ID'])
                except:
                    print("No CPE Matches")

            i += 1

    # Retrieves all data for specified ScanID
    @staticmethod
    def retrieve_scanID_data(scanID):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        retrievalID = (scanID)
        cursor.execute('''SELECT * FROM ScanHistory WHERE ScanID = ? ''', retrievalID)
        results = cursor.fetchall()
        return results

    # Retrieves scanIDs and Dates for all Scans
    @staticmethod
    def retrieve_scan_history():
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT ScanID, ScanDate FROM ScanHistory''')
        results = cursor.fetchall()
        return results

    # Deletes specified ScanID
    @staticmethod
    def delete_scan_ID(scanID):
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        deleteID = (scanID)
        cursor.execute('''DELETE FROM ScanHistory WHERE ScanID = ?''', deleteID)

    @staticmethod
    def get_full_cve():
        """Returns all unique CVEs in database

        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()
        results = set()
        cursor.execute('''SELECT cveName FROM CPEvulns''')

        for row in cursor:
            results.add(row[0])

        return results


    @staticmethod
    def get_all_devices():
        """Query the database for all saved devices
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT Model, Manufacturer from Devices""", ())
        return cursor.fetchall()

    @staticmethod
    def get_all_scans():
        """Query the database for all saved scans
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT sh.ScanID as ScanID, 
                                sh.Duration as Duration, 
                                sh.ScanDate as Date, 
                                (SELECT COUNT(*) from Hosts where ScanID = sh.ScanID) as HostCount 
                                from ScanHistory sh JOIN Hosts h on sh.ScanID = h.ScanID 
                                GROUP BY sh.ScanID""", ())
        return cursor.fetchall()

    @staticmethod
    def get_all_where(query_str, query_params):
        """Query the database for all saved entiries with the given string and params
        """
        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        try:
            cursor.execute(query_str, query_params)
            conn.commit()

        except sqlite3.Error as er:
            print
            'er:', er.message

        return cursor.fetchall()

    @staticmethod
    def update_import():
        # Only takes json currently.
        #path = askopenfilename(title='Select Database file to import...', defaultextension='.db', filetypes=(("database files", "*.db"),("datafeeds", "*.json"),("all files", "*.*")))
        path = askopenfilename(title='Select Database file to import...', defaultextension='.json')
        # ntpath for os compatibility with differing separators
        # head and tail if path ends in backslash
        head, tail = ntpath.split(path)
        fname = tail or ntpath.basename(head)

        print("\n\nDB IMPORT FILE")
        print(fname)

    """Vulnerabilities Methods"""
    @staticmethod
    def get_all_vulns():
        """Query the database for all saved vulnerabilities
        """

        conn = sqlite3.connect('vulnDB.db')
        cursor = conn.cursor()

        cursor.execute("""SELECT VulnID, cveName, CVSSScore, baseScore, baseSeverity from Vulnerabilities""", ())
        return cursor.fetchall()
