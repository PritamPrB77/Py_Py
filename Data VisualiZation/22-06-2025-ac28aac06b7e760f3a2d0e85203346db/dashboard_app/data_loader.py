import pandas as pd

def load_data():
    df_1 = pd.read_excel('./online_retail_II.xlsx', sheet_name='Year 2009-2010')
    df_2 = pd.read_excel('./online_retail_II.xlsx', sheet_name='Year 2010-2011')

    df = pd.concat([df_1, df_2], ignore_index=True)
    df = df.dropna(subset=['InvoiceDate', 'Customer ID'])
    df = df[~df['Invoice'].astype(str).str.startswith('c')]
    df = df[df['Quantity'] > 0]
    df = df[df['Price'] > 0]
    df['Revenue'] = df['Quantity'] * df['Price']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    return df