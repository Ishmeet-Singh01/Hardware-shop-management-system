from datetime import datetime
def add_product():
    brand = str(input("Brand Name: "))
    category = str(input("Category: "))
    model_name = str(input("Model Name: "))
    size = str(input("Size: "))
    cp = str(input("Current Cost Price: "))
    sp = str(input("Suggested Price To sell: "))
    stock = str(input("Stock Present: "))
    file = open("products.txt" , "a")
    file.write(brand + "," + category + "," + model_name + "," + size + "," + cp + "," + sp + "," + stock + "\n")
    file.close()
    print("Product Added Successfully")

def show_product():
    file = open("products.txt" , "r")
    for line in file:
        data = line.split(",")
        brand = data[0]
        category = data[1]
        model_name = data [2]
        size = data[3]
        cp = data [4]
        sp = data [5]
        stock = int(data [6])
        print("Brand Name: ", brand)
        print("Category: ", category)
        print ("Model Name: ", model_name)
        print("Size: ", size)
        print("Cost Price: ",cp)
        print("Selling Price: ",sp)
        print("Stock: ", stock)
        if stock <= 5:
            print("⚠ LOW STOCK")
        print("----------------------------------")
    file.close()

def search_product():
    file = open("products.txt" , "r")
    find = str(input("Enter The Item name to search: "))
    find_item = find.lower()
    item_found = False
    for line in file:
        data = line.split(",")
        brand = data[0]
        category = data[1]
        model_name = data [2]
        size = data[3]
        cp = data [4]
        sp = data [5]
        stock = data [6]
        Brand = brand.lower()
        
        Model = model_name.lower()
        full_name = Brand + " " + Model
        if find_item in full_name:
            item_found = True 
            print("Item Found: " +"\n" ,"Brand Name: ", brand + "\n" ,"Category: " ,category + "\n"
                  "Model Name: " ,model_name + "\n" , "Size: ", size + "\n",
                  "Cost Price: ",cp +"\n", "Selling Price: ",sp +"\n", "Stock: ", stock +"\n")
        
            
    if item_found == False:
        print("Item Not Found")
    file.close()
    print("----Searching Completed ----")

def sell_product():
    bill_file = open("bill.txt", "r")
    count = 0

    for line in bill_file:
        if line.strip() != "":
            count = count + 1

    bill_file.close()

    bill_no = 1001 + count
    print("\nBill No:", bill_no)
    today = datetime.now().strftime("%d-%m-%Y")
     
    bill_total = 0
    
    while True:
        item_found = False
        find = str(input("Enter The Item name to buy: "))
        quantity = int(input("Enter The quantity: "))
        file = open("products.txt" , "r")
        new_data = ""
        for line in file:

            data = line.split(",")
            if len(data) < 7:
                continue
            brand = data[0]
            category = data[1]
            model_name = data [2]
            size = data[3]
            cp = data [4]
            sp = data [5]
            stock = int(data [6])
            Brand = brand.lower()
            Category = category.lower()
            Model = model_name.lower()
            full_name = Brand + " " + Category + " " + Model
            find_item = find.lower()
            if find_item in full_name:
                item_found = True 
                print("Item Found: " +"\n" ,"Brand Name: ", brand + "\n" ,"Category: " ,category + "\n"
                    "Model Name: " ,model_name + "\n" , "Size: ", size + "\n",
                    "Cost Price: ",cp +"\n", "Selling Price: ",sp +"\n", "Stock: ", stock )
                if quantity <= stock :
                    
                    new_stock = stock - quantity
                    updated_line = brand + "," + category + "," + model_name + "," + size + "," + cp + "," + sp + "," + str(new_stock) + "\n"
                    new_data = new_data + updated_line
                    price_per_item = int(sp)
                    line_total = price_per_item * quantity                 
                    filees = open("sales.txt", "a")
                    sales_line = str(bill_no)+ "," + str(today) + "," + brand + "," + category+ "," + model_name + "," + str(quantity) + "," + str(price_per_item) + "," +str(line_total) + "\n"
                    filees.write(sales_line)
                    filees.close()
                    print("Sale Successfull " + "\n" , "New Stock: " , new_stock)                        
                    bill_total += line_total
                else:
                    print("Not Enough Stock")        
            
            else:
                new_data = new_data + line
        file = open("products.txt", "w")
        file.write(new_data)
        file.close()
        if item_found == False:
                print("Item Not Found")
            
        print("""
1. Add Product
2. Finish Bill
""")            
        choi = int(input("Enter the Choice: "))
        if choi == 1:
            continue
        if choi == 2:
            break
    customer = input("Customer Name: ").strip()
    if customer == "":
        customer ="Cash Customer"

    if bill_total == 0:
        print("No products were sold.")
        return
    print("Subtoal is:",bill_total, "Ruppee")
    discount = int(input("Enter Discount amount: "))
    final_bill = bill_total-discount
    print("Discount:", discount, "Rupee")
    print("Final is:",final_bill, "Ruppee")
    recieved = int(input("Enter The Amount To pay:"))
    if recieved >= final_bill:
        pending = 0
        status = "Paid"
        print("Balance Cleared")
    else:
        pending = final_bill - recieved
        status = "Pending"

    bill_line = (
        str(bill_no) + "," +
        customer + "," +
        str(today) + "," +
        str(bill_total) + "," +
        str(discount) + "," +
        str(final_bill)+ "," +
        str(recieved) + "," +
        str(pending) + "," +
        status + "\n"
    )

    file = open("bill.txt", "a")
    file.write(bill_line)
    file.close()
def return_product():
    find = str(input("Enter The Item name to return: "))
    quantity = int(input("Enter The quantity: "))
    today = datetime.now().strftime("%d-%m-%Y")
    file = open("products.txt" , "r")
    new_data = ""
    find_item = find.lower()
    item_found = False
    for line in file:
        
        data = line.split(",")
        if len(data) < 7:
            continue
        brand = data[0]
        category = data[1]
        model_name = data [2]
        size = data[3]
        cp = data [4]
        sp = data [5]
        stock = int(data [6])
        Brand = brand.lower()
        Category = category.lower()
        Model = model_name.lower()
        full_name = Brand + " " + category + " " + Model
        if find_item in full_name:
            item_found = True 
            print("Item Found: " +"\n" ,"Brand Name: ", brand + "\n" ,"Category: " ,category + "\n" , 
                    "Model Name: " ,model_name + "\n" , "Size: ", size + "\n",
                  "Cost Price: ",cp +"\n", "Selling Price: ",sp +"\n", "Stock: ", stock )
            
            new_stock = stock + quantity
            updated_line = brand + "," + category + "," + model_name + "," + size + "," + cp + "," + sp + "," + str(new_stock) + "\n"
            new_data = new_data + updated_line
            print("Return Successfull " + "\n" , "New Stock: " , new_stock)
            filees = open("return.txt", "a")
            sales_line = str(today) + "," + brand + "," + model_name + "," + str(quantity) + "\n"
            filees.write(sales_line)
            filees.close()
            
        else:
            new_data = new_data + line
           
    if item_found == False:
        print("Item Not Found")
    file.close()
    files = open("products.txt" , "w")
    files.write(new_data)
    files.close()

def low_stock():
    file = open("products.txt" , "r")
    for line in file:
        data = line.split(",")
        if len(data) < 7:
            continue
        brand = data[0]
        model_name = data [2]
        stock = int(data [6])
        if stock <=5:
            print("-------------------")
            print("Brand:", brand)
            print("Model Name:", model_name)
            print("Stock:", stock)
    file.close()

def sales_report():
    file = open("sales.txt", "r")
    sales_data = {}
    for line in file:
        data = line.split(",")
        if len(data)<4:
            continue
        date =data[0]
        brand =data[1]
        model = data[2]
        quantity= int(data[3])
        product = brand + " " + model
        
        if product in sales_data:
            sales_data[product] = sales_data[product] + quantity
        else:
            sales_data[product] = quantity
    largest = 0
    larg_item = ""
    smallest = 9999
    small_item = ""
    print("=====  SALES REPORT =====")
    if len(sales_data) == 0:
        print("No Sales")
        return 
    for ch in sales_data:
        print(ch, ":", sales_data[ch],"Sold")
        
        if sales_data[ch] > largest:
            largest = sales_data[ch]
            larg_item = ch
        if sales_data[ch] < smallest:
            smallest = sales_data[ch]
            small_item = ch

    print("Highest sold item is:", larg_item ," with", largest,"Sold")
    print("Lowest sold item is:", small_item ," with", smallest,"Sold")
    file.close()

def monthly_summary():
    find = str(input("Enter The Item name to get report: "))
    file = open("sales.txt" , "r")
    find_item = find.lower()
    item_found = False
    sales_month = {}
    for line in file:
        
        data = line.split(",")
        if len(data) < 4:
            continue
        date = data[0]
        brand = data[1]
        model_name = data [2]
        quantity = int(data[3])
        Brand = brand.lower()
        Model = model_name.lower()
        date_y = date.split("-")
        month = date_y[1]
        year = date_y[2]
        month_year = month + "-" + year
        full_name = Brand + " " + Model
        if find_item in full_name:
            if month_year in sales_month:
                sales_month[month_year] = sales_month[month_year]+quantity
            else:
                sales_month[month_year] = quantity
    
    filea = open("return.txt" , "r")
    find_item = find.lower()
    item_found = False
    return_month = {}
    for line in filea:
        
        dataa = line.split(",")
        if len(dataa) < 4:
            continue
        datea = dataa[0]
        branda = dataa[1]
        model_namea = dataa [2]
        quantitya = int(dataa[3])
        Branda = branda.lower()
        Modela = model_namea.lower()
        date_ya = datea.split("-")
        montha = date_ya[1]
        yeara = date_ya[2]
        month_yeara = montha + "-" + yeara
        full_namea = Branda + " " + Modela
        if find_item in full_namea:
            if month_yeara in return_month:
                return_month[month_yeara] = return_month[month_yeara]+quantitya
            else:
                return_month[month_yeara] = quantitya
    print(" ====  Monthly Reports  ====")   
    for month in sales_month:
        if month in sales_month:
            sales = 0
        sales = sales_month[month]   
        if month in return_month:
            returns = 0
        returns = return_month[month]

        net = sales - returns
        print("Month: ",month,"\n","\n","Product: ",model_name,"\n","Sales: ",sales,"\n","Returns: ",returns,"\n","Net: ",net, "\n")
    file.close()
    filea.close()

def recieve_payment():
    bill_no = int(input("Enter The Bill Number: "))
    file = open("bill.txt","r")
    bill_found = False
    new_data = ""
    today = datetime.now().strftime("%d-%m-%Y")
    for line in file:
        
        data = line.split(",")
        if len(data)<9:
            continue
        bill = int(data[0])
        name = data[1]
        date = data[2]
        subtotal = int(data[3])
        discount = int(data[4])
        final_bill = int(data[5])
        paid = int(data[6])
        pending =int(data[7])
        status = data[8].strip()
        if bill_no == bill:
            bill_found = True
            
            print("====  Bill Found  ====")
            print("Bill No.", str(bill) +"\n" ,"Customer's Name:",name +"\n" ,"Date:",str(date)+"\n" ,"SubTotal balance:",str(subtotal)+"\n" ,"Discount:",str(discount)+"\n" ,"Final Bill.:",str(final_bill)+"\n" ,"Paid:",str(paid)+"\n" ,"Pending:",str(pending)+"\n" ,"Status:",status+"\n")   
            if status == "Paid":
                print("This bill is already cleared.") 
                file.close()
                return
            today_payment = int(input("Enter The Amount Received Today:"))
            paid = paid + today_payment
            pending = final_bill - paid
            if pending == 0:
                status = "Paid"
            else:
                status = "Pending"
            files = open("payments.txt","a")
            final = str(bill) + "," + str(today) + "," + str(today_payment)+ "\n"
            files.write(final)
            files.close()
            
            update = (str(bill) + "," +
            name + "," +
            str(date) + "," +
            str(subtotal)+ "," +
            str(discount)+ "," +
            str(final_bill) + "," +
            str(paid) + "," +
            str(pending) + "," +
            status + "\n")
            new_data = new_data + update
            print("==== Payment Receipt ====")
            print("Bill No.:", bill)
            print("Customer Name:", name)
            print("Payment Date:",today)
            print("Paid Today:", today_payment)
            print("Total Paid:", paid)
            print("Pending:", pending)
            print("--------------------------")
        else:
            new_data=new_data + line
    filea = open("bill.txt","w")
    filea.write(new_data)
    filea.close()
    if bill_found:
        print("Done")
    if bill_found==False:
        print("Bill Not Found")


