import sqlite3

class DBFunctions():
    #Setting up connection to DB
    global conn,cursor
    conn = sqlite3.connect('vulnDB.db')
    cursor = conn.cursor()

    #Saves a new device to the database
    def save_device(deviceName, deviceManufacturer, cpeURI):
        device_info = [deviceName, deviceManufacturer, cpeURI]

        try:
            cursor.execute('INSERT INTO Devices VALUES(?, ?, ?)', device_info)
            conn.commit()
        except sqlite3.IntegrityError:
            return "That device already exists in the database."

        return "Device added successfully"

    #Saving a Vulnerability to the database

    def save_vulnerability(Model, cpeName, cpe22URI, cpe23URI, versionsAffected,
                           description, CVSSScore, attackVector, attackComplexity, priviledgesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           availabilityImpact, baseScore, baseSeverity, exploitabilityScore):


        cursor.execute('SELECT MAX(VulnID) FROM Vulnerabilities')
        conn.commit()
        maxIDTuple = cursor.fetchone()
        maxID = maxIDTuple[0]
        vulnID = maxID + 1

        vulnerability_info = [vulnID, Model, cpeName, cpe22URI, cpe23URI, versionsAffected,
                           description, CVSSScore, attackVector, attackComplexity, priviledgesRequired,
                           userInteraction, confidentialityImpact, integrityImpact, availibilityImpact,
                           availabilityImpact, baseScore, baseSeverity, exploitabilityScore]
        try:
            cursor.execute('INSERT INTO Vulnerabilities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '
                           '?, ?, ?, ?, ?, ?,)', vulnerability_info)
            conn.commit()
        except sqlite3.IntegrityError:
            return "That device already exists in the database."

    #Saves a scan to the database

    def save_scan(Date, Model, Duration,):

        cursor.execute('SELECT MAX(ScanID) FROM History')
        conn.commit()
        maxIDTuple = cursor.fetchone()
        maxID = maxIDTuple[0]
        scanID = maxID + 1

        scan_info = [scanID, Date, Model, Duration]
        cursor.execute('INSERT INTO  VALUES(?, ?, ?, ?', scan_info)
        conn.commit()

