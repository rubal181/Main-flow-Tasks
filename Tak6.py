import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")
        
        # Define the layout
        self.create_widgets()
        
        # Initialize data structures
        self.customers = pd.DataFrame(columns=['ID', 'Name', 'Email'])
        self.products = pd.DataFrame(columns=['ID', 'Name', 'Price'])
        self.transactions = pd.DataFrame(columns=['Customer_ID', 'Product_ID', 'Quantity'])
        
    def create_widgets(self):
        # Customer Management
        tk.Label(self.root, text="Customer ID").grid(row=0, column=0)
        tk.Label(self.root, text="Customer Name").grid(row=1, column=0)
        tk.Label(self.root, text="Customer Email").grid(row=2, column=0)
        
        self.cust_id = tk.Entry(self.root)
        self.cust_name = tk.Entry(self.root)
        self.cust_email = tk.Entry(self.root)
        
        self.cust_id.grid(row=0, column=1)
        self.cust_name.grid(row=1, column=1)
        self.cust_email.grid(row=2, column=1)
        
        tk.Button(self.root, text="Add Customer", command=self.add_customer).grid(row=3, column=1)
        
        # Product Management
        tk.Label(self.root, text="Product ID").grid(row=4, column=0)
        tk.Label(self.root, text="Product Name").grid(row=5, column=0)
        tk.Label(self.root, text="Product Price").grid(row=6, column=0)
        
        self.prod_id = tk.Entry(self.root)
        self.prod_name = tk.Entry(self.root)
        self.prod_price = tk.Entry(self.root)
        
        self.prod_id.grid(row=4, column=1)
        self.prod_name.grid(row=5, column=1)
        self.prod_price.grid(row=6, column=1)
        
        tk.Button(self.root, text="Add Product", command=self.add_product).grid(row=7, column=1)
        
        # Transaction Management
        tk.Label(self.root, text="Customer ID").grid(row=8, column=0)
        tk.Label(self.root, text="Product ID").grid(row=9, column=0)
        tk.Label(self.root, text="Quantity").grid(row=10, column=0)
        
        self.trans_cust_id = tk.Entry(self.root)
        self.trans_prod_id = tk.Entry(self.root)
        self.trans_quantity = tk.Entry(self.root)
        
        self.trans_cust_id.grid(row=8, column=1)
        self.trans_prod_id.grid(row=9, column=1)
        self.trans_quantity.grid(row=10, column=1)
        
        tk.Button(self.root, text="Add Transaction", command=self.add_transaction).grid(row=11, column=1)
        
        tk.Button(self.root, text="Generate Invoice", command=self.generate_invoice).grid(row=12, column=1)
        
    def add_customer(self):
        new_customer = {'ID': self.cust_id.get(), 'Name': self.cust_name.get(), 'Email': self.cust_email.get()}
        self.customers = self.customers.append(new_customer, ignore_index=True)
        messagebox.showinfo("Success", "Customer added successfully")
        
    def add_product(self):
        new_product = {'ID': self.prod_id.get(), 'Name': self.prod_name.get(), 'Price': float(self.prod_price.get())}
        self.products = self.products.append(new_product, ignore_index=True)
        messagebox.showinfo("Success", "Product added successfully")
        
    def add_transaction(self):
        new_transaction = {'Customer_ID': self.trans_cust_id.get(), 'Product_ID': self.trans_prod_id.get(), 'Quantity': int(self.trans_quantity.get())}
        self.transactions = self.transactions.append(new_transaction, ignore_index=True)
        messagebox.showinfo("Success", "Transaction added successfully")
        
    def generate_invoice(self):
        customer_id = simpledialog.askstring("Input", "Enter Customer ID:")
        transactions_for_customer = self.transactions[self.transactions['Customer_ID'] == customer_id]
        
        if transactions_for_customer.empty:
            messagebox.showwarning("No Transactions", "No transactions found for this customer.")
            return
        
        invoice_file = f"invoice_{customer_id}.pdf"
        c = canvas.Canvas(invoice_file, pagesize=letter)
        c.drawString(100, 750, f"Invoice for Customer ID: {customer_id}")
        
        y_position = 730
        total_amount = 0
        for _, transaction in transactions_for_customer.iterrows():
            product = self.products[self.products['ID'] == transaction['Product_ID']].iloc[0]
            amount = product['Price'] * transaction['Quantity']
            total_amount += amount
            c.drawString(100, y_position, f"Product: {product['Name']}, Quantity: {transaction['Quantity']}, Amount: ${amount:.2f}")
            y_position -= 20
        
        c.drawString(100, y_position, f"Total Amount: ${total_amount:.2f}")
        c.save()
        messagebox.showinfo("Success", f"Invoice generated: {invoice_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
