import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import backend as bk
def clear_content(content):
    rows = content.winfo_children()
    for row in rows:
        row.destroy()
def create_input_row(parent,label_text):
    row=ttk.Frame(parent)
    row.pack(pady=10) 
    text_label = ttk.Label(row,text=label_text,font=("Segoe UI",10),width=15)
    text_label.pack(pady=10,side="left")
    entry = ttk.Entry(row, width=30)
    entry.pack(side="left",padx=5,pady=5)
    return entry
def clear_entries(entries):
    for entry in entries:
        entry.delete(0,tk.END)
def open_add_product(content):
    clear_content(content)
    title = ttk.Label(content, text = "ADD PRODUCT",font=("Segoe UI",24,"bold"))
    title.pack(fill="x",pady=15)
    form_frame =ttk.Frame(content)
    form_frame.pack(pady=30)
    brand_entry =create_input_row(form_frame,"Brand")
    category_entry =create_input_row(form_frame,"Category")
    model_entry =create_input_row(form_frame,"Model")
    size_entry =create_input_row(form_frame,"Size")
    cost_price_entry =create_input_row(form_frame,"Cost Price")
    selling_price_entry =create_input_row(form_frame,"Selling Price")
    stock_entry =create_input_row(form_frame,"Stock")
    entries = [brand_entry,category_entry,model_entry,size_entry,cost_price_entry,selling_price_entry,stock_entry]
    def on_save_clicked():
        brand=brand_entry.get().strip()
        category=category_entry.get().strip()
        model=model_entry.get().strip()
        size=size_entry.get().strip()
        cost_price=cost_price_entry.get().strip()
        selling_price=selling_price_entry.get().strip()
        stock=stock_entry.get().strip()
        success,message=bk.add_productv2(brand,category,model,size,cost_price,selling_price,stock)
        if success:
            status_label.config(text=message,foreground="green")
            clear_entries(entries)
        else :
            status_label.config(text=message,foreground ="red")
        
    
    save = ttk.Button(form_frame,text="Save Product",command=on_save_clicked)
    save.pack(pady=20)
    status_label = ttk.Label(form_frame,text="",font=("Segoe UI",20))
    status_label.pack(pady=20)
def start_gui():
    app = ttk.Window(themename = "flatly")
    app.title("Ishmeet Hardware Store")
    app.geometry("1000x1000")
    app.resizable(False,False)
    header = ttk.Frame(app)
    header.pack(fill="x")
    
    title = ttk.Label(
        header,
        text = "ISHMEET HARDWARE STORE",
        font=("Segoe UI",26,"bold")
    )
    title.pack(pady =15)
    body = ttk.Frame (app)
    body.pack(fill = "both", expand = True)
    menu = ttk.Frame(body,width = 250)
    menu.pack(side = "left",fill ="y")
    menu.pack_propagate(False)
    add_prdct_btn = ttk.Button(menu,text="📦 Add Product",command= lambda: open_add_product(content))
    add_prdct_btn.pack(fill="x",padx=10,pady=10,expand=True)
    content = ttk.Frame(body)
    content.pack(side="right",fill = "both",expand=True)
    app.mainloop()
