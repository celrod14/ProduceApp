from tkinter import *
import mysql.connector
from decimal import *
from datetime import date
from dbconfig import *

class ProduceApp(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.background = '#D3D3D3'
        self.config(bg='#D3D3D3')
        self.ordered = False

        self.conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name_product
        )

        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM tblproducts order by price desc')

        self.rows = self.cursor.fetchall()
        self.products = []
        self.prices = []

        for row in self.rows:
            self.products.append(row[0].title())
            self.prices.append(row[1])

        self.conn.close()

        # shipping dictionary
        self.shipping = {
            '1 Day' : 20.00,
            '2 Days' : 15.00,
            '3 Days' : 10.00
        }

        self.lblProducts = list(self.products)
        self.lblPrices = list(self.prices)
        self.entQuantity = list(self.products)

        self.createWidgets()

    def createWidgets(self):
        self.row = 1
        self.col = 1
        self.lblHeader = Label(self, text='Produce App', font=('Arial', 25, 'bold'), background=self.background)
        self.lblHeader.grid(row=self.row, column=1, sticky=NSEW, columnspan=3, ipadx=3, ipady=8)
        self.row += 1

        self.lblProductTitle = Label(self, text='Produce', font=('Arial', 15), background=self.background)
        self.lblProductTitle.grid(row=self.row, column=self.col, sticky=NSEW, ipadx=10)
        self.col += 1

        self.lblPriceTitle = Label(self, text='Price', font=('Arial', 15), background=self.background)
        self.lblPriceTitle.grid(row=self.row, column=self.col, sticky=NSEW, ipadx=10)
        self.col += 1

        self.lblQuantityTitle = Label(self, text='Quantity', font=('Arial', 15), background=self.background)
        self.lblQuantityTitle.grid(row=self.row, column=self.col, sticky=NSEW, ipadx=10)

        for i in range(len(self.products)):
            self.row += 1
            self.lblProducts[i] = Label(self,text=self.products[i], background=self.background)
            self.lblProducts[i].grid(row=self.row, column=1, ipadx = 3, sticky=NSEW)

            self.lblPrices[i] = Label(self, text=self.prices[i], background=self.background)
            self.lblPrices[i].grid(row=self.row, column=2, ipadx = 3, sticky=NSEW)

            self.entQuantity[i] = Entry(self, width=10, background='white')
            self.entQuantity[i].grid(row=self.row, column=3, ipadx = 3, sticky=NSEW)

        self.row += 2

        self.ship = StringVar()
        self.rdoDay1 = Radiobutton(self, text='1 Day', value='1 Day', background=self.background, variable=self.ship)
        self.rdoDay1.grid(row=self.row, column=1, ipadx=3, sticky=NSEW)
        self.rdoDay1.select()

        self.rdoDay2 = Radiobutton(self, text='2 Days', value='2 Days', background=self.background, variable=self.ship)
        self.rdoDay2.grid(row=self.row, column=2, ipadx=3, sticky=NSEW)

        self.rdoDay3 = Radiobutton(self, text='3 Days', value='3 Days', background=self.background, variable=self.ship)
        self.rdoDay3.grid(row=self.row, column=3, ipadx=3, sticky=NSEW)

        self.row += 2

        self.btnCalculate = Button(self, text='Calculate', bg='#582C83', command=self.Calculate)
        self.btnCalculate.grid(row=self.row, column=1, ipadx=3, sticky=NSEW, columnspan=1)

        self.lblTotalTitle = Label(self, text=('Total: '), font=('Arial', 10, 'bold'), background=self.background)
        self.lblTotalTitle.grid(row=self.row, column=2, sticky=EW, ipadx=10, padx=10)

        self.entTotal = Entry(self, width=10, background='white')
        self.entTotal.grid(row=self.row, column=3, sticky=EW, ipadx=10, padx=10)

        self.row += 2

        self.row += 1

        self.lblOrderSubmitted = Label(self, text=(''),
                                       font=('Arial', 10, 'bold'), background=self.background, fg='#A4D65E')
        self.lblOrderSubmitted.grid(row=self.row + 1, column=5, sticky=EW, ipadx=10, padx=10)

        self.row += 1

        self.btnOrder = Button(self, text='Order', background='#A4D65E', command=self.Order, state=DISABLED)
        self.btnOrder.grid(row=self.row, column=1, columnspan=3, sticky=EW)

        self.row += 1

        self.btnReset = Button(self, text='Reset', background='#27509B', command=self.Reset)
        self.btnReset.grid(row=self.row, column=1, columnspan=3, sticky=EW)

        self.row += 1

        self.btnClose = Button(self, text='Close', background='#F44336', command=w.quit)
        self.btnClose.grid(row=self.row, column=1, columnspan=3, sticky = EW)

        self.menubar = Menu(self)
        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.editMenu = Menu(self.menubar, tearoff=0)
        self.subMenu = Menu(self.menubar)
        self.menubar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_cascade(label='Order Tools', menu=self.subMenu)
        self.subMenu.add_command(label='Reset', command=self.Reset)
        self.subMenu.add_command(label='Calculate', command=self.Calculate)
        self.fileMenu.add_command(label='Close', command=w.quit)
        self.menubar.add_cascade(label='Edit', command=self.editMenu)

        w.config(menu=self.menubar)

    def Calculate(self):
        self.total = 0
        self.entTotal.delete(0, END)
        try:
            for i in range(len(self.products)):
                if (self.entQuantity[i].get()):
                    self.total += (self.prices[i] * int(self.entQuantity[i].get()))

            if(self.ship.get() == '1 Day'):
                self.total += Decimal(self.shipping['1 Day'])
            elif(self.ship.get() == '2 Days'):
                self.total += Decimal(self.shipping['2 Days'])
            elif (self.ship.get() == '3 Days'):
                self.total += Decimal(self.shipping['3 Days'])

            self.result = '${0:.2f}'.format(self.total)

            self.entTotal.insert(END, self.total)
        except Exception as e:
            print(e)
            self.entTotal.insert(END, 'ERROR')

            return

        self.btnOrder.config(state='normal')

    def Reset(self):
        self.entTotal.delete(0, END)
        self.rdoDay1.select()
        for i in range(len(self.products)):
            self.entQuantity[i].delete(0, END)
        self.lblOrderSubmitted.config(text='', bg=self.background)

    def Order(self):
        self.connOrder = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name_order
        )

        self.orderCursor = self.connOrder.cursor()
        self.val = date.today(), self.ship.get(), self.total
        self.sql = "INSERT INTO tblordersummary (orderdate, shipmethod, totalprice) values (%s, %s, %s)"
        self.orderCursor.execute(self.sql, self.val)
        self.connOrder.commit()

        self.lblOrderSubmitted.config(text=('Order ' + str(self.orderCursor.lastrowid) + ' submitted 🛒🛒🛒'), font=('Arial', 10, 'bold'), background='white', fg='#A4D65E')

        self.connOrder.close()

w = Tk()
w.title("Produce App")
w.geometry('380x380')
w.config(background='#D3D3D3') # light gray

'''************'''
# Configure rows and columns to expand
# w.grid_rowconfigure(0, weight=1)
w.grid_rowconfigure(2, weight=1)
w.grid_columnconfigure(0, weight=1)
w.grid_columnconfigure(2, weight=1)

# Create a frame to hold the app and center it
center_frame = Frame(w, background='#D3D3D3')
center_frame.grid(row=1, column=1)
'''************'''
app = ProduceApp(center_frame)
app.mainloop()
