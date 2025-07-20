import pandas as pd

def load_dataset(path):
    return pd.read_excel(path)

def get_column_description():
    return {
        "InvoiceNo": "Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction.",
        "StockCode": "Product/item code. Nominal.",
        "Description": "Product name. Nominal.",
        "Quantity": "Number of products per transaction. Integer.",
        "InvoiceDate": "Invoice date and time. Datetime.",
        "UnitPrice": "Price per unit product. Float.",
        "CustomerID": "Customer’s ID. Nominal.",
        "Country": "Country of customer. Nominal."
    }
