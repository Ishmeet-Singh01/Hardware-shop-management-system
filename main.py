import sqlite3
from datetime import datetime
def add_productv2():
    
    brand = str(input("Brand Name: "))
    category = str(input("Category: "))
    model_name = str(input("Model Name: "))
    size = str(input("Size: "))
    cp = str(input("Current Cost Price: "))
    sp = str(input("Suggested Price To sell: "))
    stock = str(input("Stock Present: "))
    connection = sqlite3.connect("hardware_store.db")
    cursor = connection.cursor()
    cursor.execute("""
INSERT INTO Products(
                   Brand,
                   Category,
                   Model,
                   Size,
                   CostPrice,
                   SellingPrice,
                   Stock)
                   
                   VALUES(?,?,?,?,?,?,?)
                   """,
                  ( brand,
                   category,
                   model_name,
                   size,
                   cp,
                   sp,
                   stock
                   )
                   )
    connection.commit()
    connection.close()
    print("Item Added Successfully")

def search_productv2():
    
    connection = sqlite3.connect("hardware_store.db")
    cursor = connection.cursor()

    find = str(input("Enter The Item name to search: "))
    
    
    cursor.execute("""
SELECT * FROM Products
                   WHERE Brand LIKE ?
                   OR Category LIKE?
                   OR Model LIKE ?
                   """,
                   ("%"+find+"%",
                    "%"+find+"%",
                    "%"+find+"%"))
    rows = cursor.fetchall()
    
    if rows == []:
            print("No Product Found")
    else:
        for row in rows:
            print("====  Product  ====")
            print("ID:",row[0])
            print("Brand:",row[1])          
            print("Category:",row[2])          
            print("Model:",row[3])          
            print("Stock:",row[7])          
            print("Selling Price:",row[6])     
            print("========================")     

def sell_productv2():
    connection = sqlite3.connect("hardware_store.db")
    cursor = connection.cursor()
    
    print("""
1. New Customer
          2.Existing Customer""")
    
    def add_customer():
        name = input("Enter Customer's Name:")
        phone = input("Enter Phone Number:")
        address = input("Address")
        current_pending = 0
        cursor.execute("""
    INSERT INTO Customers(
                        Name,
                        Phone,
                        Address,
                        CurrentPending
                        )VALUES(
                        ?,
                        ?,
                        ?,
                        ?)""",
                        (name,
                            phone,
                            address,
                            current_pending))
        customer_id = cursor.lastrowid
        return customer_id
    today = datetime.now().strftime("%d-%m-%Y")
    choice = int(input("Enter Your Choice: "))
    if choice == 1:
        customer_id=add_customer()
    elif choice == 2:
        search = input("Enter customer's Name or Phone:")
        cursor.execute(
            """
SELECT * FROM Customers
WHERE name LIKE ?
OR phone LIKE ?""",
("%"+search+"%",
                    "%"+search+"%")
        )
        found = cursor.fetchall()
        if found == []:
            print("No Record Found")
            print(
                """ Create New Customer ?
                1. Yes
                2. No"""
            )
            
            ch = int(input("Enter The Choice:"))
            if ch == 1:
                
                customer_id = add_customer() 
            elif ch == 2:
                print("Billing Cancelled.")
                connection.close()
                return
            else:
                print("Invalid Choice")
        else:
            for findd in found:
                print("====  Details  ====")
                print("ID:",findd[0])
                print("Name:",findd[1])          
                print("Phone:",findd[2])          
                print("Address:",findd[3])  
                print("Pending Balance:",findd[4])
                
            customer_found = False
            verify = int(input("Enter Customer ID:"))
            for findd in found:
                if findd[0]==verify:
                    customer_found = True
                    customer_id = findd[0]
                    break
            if customer_found == False:
                print("Invalid Customer ID")
                connection.close()
                return
    else:
        print("Invalid Choice")
        connection.close()
        return
    cart = []
    bill_total = 0
    while True:
        find = str(input("Enter The Item name to Buy: "))
        quantity = int(input("Enter The quantity: "))
        cursor.execute("""
SELECT * FROM Products
                   WHERE Brand LIKE ?
                   OR Category LIKE?
                   OR Model LIKE ?
                   """,
                   ("%"+find+"%",
                    "%"+find+"%",
                    "%"+find+"%"))
        rows = cursor.fetchall()
        
        if rows == []:
                print("No Product Found")
        else:
            for row in rows:
                print("====  Product  ====")
                print("ID:",row[0])
                print("Brand:",row[1])          
                print("Category:",row[2])          
                print("Model:",row[3])          
                print("Stock:",row[7])          
                print("Selling Price:",row[6])     
                print("========================") 
            
            selected_id = int(input("Enter Product ID: "))
            product_found = False
            
            for row in rows:
                if row[0] == selected_id:
                    product_found = True
                    stock = row[7]
                    
                    if quantity <= stock :
                        selling_price = row[6]
                        line_total = quantity * selling_price
                        new_stock = stock - quantity
                        cart.append([
    selected_id,
    quantity,
    selling_price,
    line_total,
    new_stock
])
                        bill_total += line_total
                    
                    else:
                        print("Not Enough Stock")
                        break
                    
            if product_found == False:
                print("Invalid Product ID")              
        print("""
1. Add Product
2. Finish Bill
""")            
        choi = int(input("Enter the Choice: "))
        if choi == 1:
            continue
        if choi == 2:
            break
    
    if bill_total == 0:
        print("No products were sold.")
        connection.close()
        return
    print("Subtoal is:",bill_total, "Ruppee")
    discount = int(input("Enter Discount amount: "))
    final_bill = bill_total-discount
    print("Discount:", discount, "Rupee")
    print("Final is:",final_bill, "Ruppee")
    mode = input("Payment Mode (Cash/UPI/Card): ").strip()
    received = int(input("Enter The Amount To pay:"))
    if received >= final_bill:
        pending = 0
        status = "Paid"
        print("Balance Cleared")
    else:
        pending = final_bill - received
        status = "Pending"
    
    cursor.execute(
        """
INSERT INTO Bills(
Date,
CustomerID,
Total,
Discount,
Final,
Paid,
Pending,
Status

)
VALUES(

?,
?,
?,
?,
?,
?,
?,
?
)""",
(today,
customer_id,
bill_total,
discount,
final_bill,
received,
pending,
status))
    bill_id = cursor.lastrowid
    cursor.execute("""SELECT CurrentPending
FROM Customers
WHERE CustomerID = ?""",(customer_id,))
    fin_pend = cursor.fetchone()
        
    fin = fin_pend[0]
    final_pending = fin + pending
    cursor.execute(""" UPDATE Customers SET CurrentPending = ? WHERE CustomerID = ? """,
                    (final_pending, customer_id))
    for item in cart:
        quantity_1 = item[1]
        sp = item[2]
        l_t = item[3]
        selected = item[0]
        new_s = item[4]

        cursor.execute(
            """INSERT INTO BillItems(
            BillId,
            ProductId,
            Quantity,
            Price,
            Total)
            VALUES(
            ?,
            ?,
            ?,
            ?,
            ?)""",(
                bill_id,
                selected,
                quantity_1,
                sp,
                l_t
            )
        )
    
        cursor.execute(""" UPDATE Products 
                       SET Stock = ? 
                       WHERE ProductID = ? """,
                    (new_s, selected))
        
    cursor.execute(
            """INSERT INTO Payments(
            BillId,
            Date,
            Amount,
            Mode)
            VALUES(
            ?,
            ?,
            ?,
            ?)""",
            (bill_id,
            today,
            received,
            mode)
        )
    connection.commit()
    connection.close()
def return_productv2():
    connection = sqlite3.connect("hardware_store.db")
    cursor = connection.cursor()
    search = input("Enter customer's Name or Phone:")
    cursor.execute(
            """
SELECT * FROM Customers
WHERE name LIKE ?
OR phone LIKE ?""",
("%"+search+"%",
                    "%"+search+"%")
        )
    found = cursor.fetchall()
    if found == []:
        print("No Customer Found")
        connection.close()
        return
    else:
        for row in found:
            print("Customer ID:",row[0])
            print("Name:",row[1])
            print("Phone:",row[2])
            print("Address:",row[3])
            print("Pending:",row[4])
        customer_found = False
        verif = int(input("Enter Customer's ID: "))
        for row in found:
            if verif == row[0]:
                customer_found= True
                customer_id = row[0]
                break
        if customer_found== False:
            print("Invalid Customer's ID")
            return
        cursor.execute(
            """
SELECT * FROM Bills
WHERE CustomerID = ?""",
(customer_id,)
        )
        bill_found = cursor.fetchall()
        
                
        if bill_found == []:
            print("No Bill Found")
            return
        else:
            for bil in bill_found:
                print("Bill ID:", bil[0])
                print("Date:", bil[1])
                print("Final:", bil[5])
                print("Pending:", bil[7])
                print("----------------")
            billi_found = False
            verify = int(input("Enter Bill ID:"))
            for bil in bill_found:
                if bil[0] == verify:
                    total = bil[3]
                    discount = bil[4]
                    paid = bil[6]
                    billi_found= True
                    bill_id = bil[0]
                    break
            if billi_found == False:
                print("Invalid Bill Id")
                return
            cursor.execute(
            """
SELECT * FROM BillItems
INNER JOIN Products
ON BillItems.ProductID = Products.ProductID
WHERE BillID = ? """,
(bill_id,)
        )
            product = cursor.fetchall()
            if product == []:
                print("No Product Found")
                return
            else:
                product_found = False
                        
                for pro in product:
                    print("Item ID:", pro[0])
                    print("Brand:", pro[7])
                    print("Category:", pro[8])
                    print("Model:", pro[9])

                    print("Product ID:", pro[2])
                    print("Quantity:", pro[3])
                    
                    print("----------------")
                check = int(input("Enter Product ID:"))
                for pro in product:
                    if check == pro[2]:
                        product_found = True
                        product_id = pro[2]
                        
                        quantityy_bought = pro[3]
                        selling_price = pro[4]
                        line_total = pro[5]
                        retur =int(input("Enter Return Quantity:"))
                        if retur <= 0:
                            print("Invalid Return Quantity")
                            return
                        if retur > quantityy_bought:
                            print("Return quantity exceeds purchased quantity")
                            return
                        if retur <= pro[3]:
                            total_bought = quantityy_bought - retur
                            return_amount = retur * selling_price
                            final = line_total - return_amount
                            current_stock = pro[13]
                            new_stock = current_stock + retur
                        
                            cursor.execute(
                                """UPDATE Products
                                SET Stock = ?
                                WHERE ProductID = ?""",
                                (new_stock,product_id)
                            )
                            item_id = pro[0]
                            cursor.execute(
                                """UPDATE BillItems
                                SET Quantity = ?,
                                 Total = ?
                                WHERE ItemID = ?""",
                                (total_bought,
                                 final,
                                 item_id)
                            )
                            
                            total = total -return_amount
                            finall = total - discount
                            pending = finall - paid
                            cursor.execute(
                                """UPDATE Bills
                                SET Total = ?,
                                Final = ?,
                                Pending = ?
                                WHERE BillID = ?""",
                                
                                (total,
                                 finall,
                                 pending,
                                 bill_id)
                            ) 
                            cursor.execute(
                                """UPDATE Customers
                                SET CurrentPending = ?
                                WHERE CustomerID = ?""",
                                (pending,customer_id)
                            )
                            print("₹", return_amount, "deducted from bill.")
                            print("New Pending:", pending)
                            break
                if product_found== False:
                    print("Invalid Product ID")
                    return
                
    connection.commit()
    connection.close()

def receive_paymentv2():
    today = datetime.now().strftime("%d-%m-%Y")
    connection = sqlite3.connect("hardware_store.db")
    cursor = connection.cursor()
    search = input("Enter customer's Name or Phone:")
    cursor.execute(
            """
SELECT * FROM Customers
WHERE name LIKE ?
OR phone LIKE ?""",
("%"+search+"%",
                    "%"+search+"%")
        )
    found = cursor.fetchall()
    if found == []:
        print("No Customer Found")
        connection.close()
        return
    else:
        for row in found:
            print("Customer ID:",row[0])
            print("Name:",row[1])
            print("Phone:",row[2])
            print("Address:",row[3])
            print("Pending:",row[4])
        customer_found = False
        verif = int(input("Enter Customer's ID: "))
        for row in found:
            if verif == row[0]:
                customer_found= True
                customer_id = row[0]
                pending = row[4]
                break
        if customer_found== False:
            print("Invalid Customer's ID")
            return
        balance = int(input("Enter The Amount To Pay:"))
        
        final = pending - balance
        cursor.execute(
            """UPDATE Customers
            SET CurrentPending = ?
            WHERE CustomerID = ?""",
            (final,customer_id)
        )
        mode = input("Payment Mode (Cash/UPI/Card): ").strip()

        cursor.execute("""
        INSERT INTO Payments(
        BillId,
        Date,
        Amount,
        Mode
        )
        VALUES(
        ?,
        ?,
        ?,
        ?
        )
        """,
        (
        None,
        today,
        balance,
        mode
        ))
    connection.commit()
    connection.close()
    print("Payment Received Successfully.")
    print("Remaining Pending:", final)
