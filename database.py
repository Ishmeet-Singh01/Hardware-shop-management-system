import sqlite3

connection = sqlite3.connect("hardware_store.db")
cursor = connection.cursor()

# ==========================
# Products Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    Brand TEXT,
    Category TEXT,
    Model TEXT,
    Size TEXT,
    CostPrice INTEGER,
    SellingPrice INTEGER,
    Stock INTEGER
)
""")

# ==========================
# Customers Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers(
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Phone TEXT,
    Address TEXT,
    CurrentPending INTEGER DEFAULT 0
)
""")

# ==========================
# Bills Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Bills(
    BillID INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT,
    CustomerID INTEGER,
    Total INTEGER,
    Discount INTEGER,
    Final INTEGER,
    Paid INTEGER,
    Pending INTEGER,
    Status TEXT,
    FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID)
)
""")

# ==========================
# Bill Items Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS BillItems(
    ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    BillID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    Price INTEGER,
    Total INTEGER,
    FOREIGN KEY(BillID) REFERENCES Bills(BillID),
    FOREIGN KEY(ProductID) REFERENCES Products(ProductID)
)
""")

# ==========================
# Payments Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Payments(
    PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
    BillID INTEGER,
    Date TEXT,
    Amount INTEGER,
    Mode TEXT,
    FOREIGN KEY(BillID) REFERENCES Bills(BillID)
)
""")

connection.commit()
connection.close()

print("Database Created Successfully!")