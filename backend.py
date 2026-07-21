import sqlite3
from datetime import datetime
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
        address = input("Address:")
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
def debt_report():
    connection = sqlite3.connect("hardware_store.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT *
    FROM Customers
    WHERE CurrentPending > 0
    """)

    rows = cursor.fetchall()

    if rows == []:
        print("No Pending Customers.")
        connection.close()
        return

    for row in rows:
        customerId = row[0]
        name = row[1]
        phone = row[2]
        address = row[3]
        currentpending = row[4]

        print("==== Customer's Detail ====")
        print("Customer ID:", customerId)
        print("Name:", name)
        print("Phone Number:", phone)
        print("Address:", address)
        print("Pending:", currentpending)
        print("===========================")

    connection.close()
def customer_history():
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
                customer = row[1]
                phone = row[2]
                break
        if customer_found== False:
            print("Invalid Customer's ID")
            connection.close()
            return
        cursor.execute(
            """SELECT *
            FROM Bills
            WHERE CustomerID = ?""",
            (customer_id,)
        )   
        rows = cursor.fetchall()
        if rows == []:
            print("No Bills Found.")
            connection.close()
            return
        bill_found = False
        
        for rowss in rows:    
            print("=" * 35)
            print("Bill ID:",rowss[0])
            print("Date:",rowss[1])
            print("Final:",rowss[5])
            print("Pending:",rowss[7])
            print("Status:",rowss[8])
            print("=" * 35)
        verify = int(input("Enter The Bill ID:"))   
        for rowss in rows:
            if rowss[0] ==verify:
                bill_found = True
                billid = rowss[0]
                date = rowss[1]
                final = rowss[5]
                pending = rowss[7]
                status = rowss[8]
                total = rowss[3]
                discount = rowss[4]
                paid = rowss[6]
                break
        if bill_found == False:
            print("Invalid Bill ID")
            connection.close()
            return
        
        cursor.execute(
            """SELECT *
            FROM BillItems
            INNER JOIN Products
            ON BillItems.ProductID = Products.ProductID
            WHERE BillID = ?
""",(verify,)
        )
        final_row = cursor.fetchall()
        if final_row == []:
            print("No Products Found.")
            connection.close()
            return
        print("\n====================\n")
        print(" BILL ")
        print("\n====================\n")
        print("Customer :", customer)
        print("Phone    :", phone)
        print("\n")
        print("Bill ID :",billid)
        print("Date:",date)
        print("\n","-"*35)
        for finrow in final_row:
            print("Brand      :", finrow[7])
            print("Model      :", finrow[9])
            print("Quantity   :", finrow[3])
            print("Category   :", finrow[8])
            print("Price(Each)      :", finrow[4])
            print("Total      :", finrow[5])
            print("-" * 35)
        print("Subtotal :", total)
        print("Discount :", discount)
        print("Final    :", final)
        print("Paid     :", paid)
        print("Pending  :", pending)
        print("Status   :", status)
    connection.close()   
def summary ():
        connection = sqlite3.connect("hardware_store.db")
        cursor = connection.cursor()    
        month = input("Enter Month (MM): ")
        year = input("Enter Year (YYYY): ") 
        cursor.execute(
            """
SELECT * FROM Bills
WHERE Date LIKE ?""",
("%-"+month+"-"+year,)
        )             
        rows = cursor.fetchall()

        if rows == []:
            print("No Bills Found.")
            connection.close()
            return
        bill_count = 0
        sales = 0
        discount = 0
        received = 0
        pending = 0
        for row in rows:
            bill_count += 1
            sales += row[3]
            discount += row[4]
            received += row[6]
            pending += row[7]
        print("="*40)
        print("MONTHLY SUMMARY")
        print(month + "-" + year)
        print("="*40)

        print("Bills           :", bill_count)
        print("Sales           :", sales)
        print("Discount        :", discount)
        print("Received Amount :", received)
        print("Pending Amount  :", pending)

        print("="*40)
        connection.close()
def validate_product(brand,category,model_name,size,cp,sp,stock):
    
        if brand == "" or category == "" or model_name == "":
            return False, "Incomplete Data, Check Again"
        if cp <=0 or sp <=0 :
            return False, "Invalid Price"
        if stock < 0:
            return False, "Stock Cant be negative"
        if sp < cp:
            return False, "Selling Price can not be less than cost price"
        else:
            return True, "Validation Successful"  
def add_productv2(brand,
    category,
    model_name,
    size,
    cp,
    sp,
    stock):
    try:
        cost_price = int(cp)
        selling_price = int (sp)
        stocks = int (stock)
    except ValueError:
        return False,"Enter Valid Numbers"
    status,message = validate_product(brand,category,model_name,size,cost_price,selling_price,stocks)
    if not status:
        return status,message
    return save_product(brand,category,model_name,size,cost_price,selling_price,stocks)
def save_product(brand,category,model_name,size,cost_price,selling_price,stocks):
    try:
        connection = sqlite3.connect("hardware_store.db")
    except sqlite3.Error:
        return False, "No Database Found"
    try:
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
                   cost_price,
                   selling_price,
                   stocks
                   )
                   )
    except sqlite3.Error:
        return False, "Server Error, Try Again Later"
    else:
        connection.commit()
    finally:
        connection.close()
    return True,"Item Added Successfully"