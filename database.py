import sqlite3

connection = sqlite3.connect("hardware_store.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Bills(
    BillId INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT,
    Customer TEXT,
    Total INTEGER,
    Discount INTEGER,
    Final INTEGER,
    Paid INTEGER,
    Pending INTEGER,
    Status TEXT
    
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Payments(
    PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
    BillId INTEGER,
    Date TEXT,
    Amount INTEGER,
    Mode TEXT
    
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS BillItems(
    ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    BillId INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    Price INTEGER,
    Total INTEGER
    
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers(
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Phone INTEGER,
    Address TEXT,
    CurrentPending INTEGER     
)
""")
connection.commit()
connection.close()