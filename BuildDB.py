import sqlite3

conn = sqlite3.connect('vulnDB.db')

cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE Severity (SevLevel INTEGER PRIMARY KEY, Name TEXT, Description TEXT)''')
    cursor.execute('''CREATE TABLE Devices (Model TEXT PRIMARY KEY, Manufacturer TEXT)''')
    conn.commit()
    cursor.execute('''CREATE TABLE Vulnerabilities (VulnID INTEGER PRIMARY KEY, SevLevel INTEGER, Name TEXT, Category TEXT, 
    Patch TEXT, PatchFileName TEXT, Manual TEXT, ManualFileName TEXT, FOREIGN KEY(SevLevel) REFERENCES Severity(SevLevel))''')
    cursor.execute('''CREATE TABLE ScanHistory (ScanID INTEGER PRIMARY KEY, Model TEXT, ScanDate TEXT, Duration INTEGER)''')
    conn.commit()
    cursor.execute('''CREATE TABLE Parameters (ScanID INTEGER, Parameter TEXT, ParameterType TEXT, PRIMARY KEY(ScanID, Parameter))''')
    cursor.execute('''CREATE TABLE DeviceVulns (Model TEXT, VulnID INTEGER, PRIMARY KEY (Model, VulnID))''')
    cursor.execute('''CREATE TABLE PenTestHistory (PenTestID INTEGER PRIMARY KEY, VulnID INTEGER, Model TEXT, SevLevel INTEGER,
    ScanID INTEGER, Result TEXT, FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), FOREIGN KEY(Model) REFERENCES Devices(Model), 
    FOREIGN KEY(VulnID) REFERENCES Vulnerabilities(VulnID), FOREIGN KEY(SevLevel) REFERENCES Severity(SevLevel),
    FOREIGN KEY(ScanID) REFERENCES ScanHistory(ScanID))''')
    conn.commit()
except sqlite3.OperationalError:
    pass
finally:
    cursor.execute('''INSERT INTO Severity VALUES (1, 'Very Dangerous', 'Could Cause severe loss of data or')''')
    cursor.execute('''INSERT INTO Devices VALUES ('NT-66NRC', 'Asus')''')
    cursor.execute('''INSERT INTO Vulnerabilities VALUES (1, 1, 'Remote Access Exploit', 'Network', 'True', 'Remote_Access.cpp', 'True', 'Applying Remote_Access patch.pdf')''')
    cursor.execute('''SELECT * FROM Severity''')
    print(cursor.fetchone())
    cursor.execute('''SELECT * FROM Devices''')
    print(cursor.fetchone())
    cursor.execute('''SELECT * FROM Vulnerabilities''')
    print(cursor.fetchone())



    #cursor.execute('''SELECT * FROM devices''')
    #print(cursor.fetchone())

