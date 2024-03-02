from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mydb import *

tv = None
data = Database(db='myexpense.db')
count = 0
selected_rowid = 0

def saveRecord():
    try:
        global data
        data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())
        messagebox.showinfo("Success", "Record saved successfully!")
        refreshData()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    global count, tv
    rows = data.fetchRecord('SELECT rowid, * FROM expense_record')
    for rec in rows:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
        
    except Exception as ep:
        pass

def update_record():
    global selected_rowid
    selected = tv.focus()
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)

def totalBalance():
    f = data.fetchRecord(query="SELECT sum(item_price) FROM expense_record")
    for i in f:
        j = i[0]
        if j is not None:
            messagebox.showinfo('Current Balance:', f"Total Expense: {j}\nBalance Remaining: {5000 - j}")
        else:
            messagebox.showinfo('Current Balance:', "No expenses recorded yet.")

def refreshData():
    global tv
    if tv is not None:
        for item in tv.get_children():
            tv.delete(item)
        fetch_records()

def deleteRow():
    global selected_rowid
    global tv
    try:
        data.removeRecord(selected_rowid)
        refreshData()
    except Exception as ep:
        messagebox.showerror('Error', ep)

ws = Tk()
ws.title('Daily Expenses')
f = ('Times new roman', 14)

namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

f2 = Frame(ws)
f2.pack()
f1 = Frame(ws, padx=10, pady=10,)
f1.pack(expand=True, fill=BOTH)

Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

submit_btn = Button(f1, text='Save Record', font=f, command=saveRecord, bg='#42602D', fg='white')
clr_btn = Button(f1, text='Clear Entry', font=f, command=clearEntries, bg='#D9B036', fg='white')
quit_btn = Button(f1, text='Exit', font=f, command=lambda: ws.destroy(), bg='#D33532', fg='white')
total_bal = Button(f1, text='Total Balance', font=f, bg='#486966', command=totalBalance)
update_btn = Button(f1, text='Update', font=f, command=update_record, bg='#C2BB00')
del_btn = Button(f1, text='Delete', font=f, command=deleteRow, bg='#BD2A2E')

submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

tv.bind("<ButtonRelease-1>", select_record)
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")
 
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

fetch_records()

ws.mainloop()
