import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

from abstract_base import AbstractAnalysis
from Analysis_Utils.utils import load_dataset, get_column_description


class Analysis(AbstractAnalysis):
    def __init__(self, level):
        self.level = level
        self.dataset = load_dataset("data/Online Retail.xlsx")
        self.styles = getSampleStyleSheet()
        self.filename = f"output/analysis_report.pdf"
        os.makedirs("plots", exist_ok=True)

    def run_analysis(self):
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        story = []

        # Title
        story.append(Paragraph(f"LEVEL-{self.level} ANALYSIS", self.styles["Title"]))
        story.append(Paragraph(" ", self.styles["Normal"]))

        # Description
        story.append(Paragraph("📝 <b>Dataset Description:</b>", self.styles["Heading2"]))
        story.append(Paragraph("This is a transactional data set which contains all the transactions occurring "
                               "between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.", self.styles["BodyText"]))

        # Column Description Table
        story.append(Paragraph("<b>Column Descriptions:</b>", self.styles["Heading2"]))
        col_desc = get_column_description()
        data = [["Column", "Description"]] + [[k, v] for k, v in col_desc.items()]
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(t)

        # Dataset Info
        story.append(Paragraph("<b>Dataset Column Types:</b>", self.styles["Heading2"]))
        info = self.dataset.dtypes.reset_index().values.tolist()
        info_data = [["Column", "Type"]] + info
        story.append(Table(info_data, hAlign='LEFT'))

        # Interesting Facts
        story.append(Paragraph("<b>Interesting Facts:</b>", self.styles["Heading2"]))
        fact1 = f"1. There are {self.dataset['InvoiceNo'].nunique()} unique invoices."
        fact2 = f"2. The dataset contains transactions from {self.dataset['Country'].nunique()} countries."
        story.append(Paragraph(fact1, self.styles["BodyText"]))
        story.append(Paragraph(fact2, self.styles["BodyText"]))

        if self.level in ['2', '3']:
            self.add_plots_level2(story)

        if self.level == '3':
            self.add_plots_level3(story)

        doc.build(story)
        print(f"✅ PDF created at: {self.filename}")

    def add_plots_level2(self, story):
        story.append(Paragraph("<b>📊 Level-2 Insights:</b>", self.styles["Heading2"]))

        # Top 10 Countries
        plt.figure(figsize=(8, 4))
        self.dataset['Country'].value_counts().head(10).plot(kind='bar', color='skyblue')
        plt.title("Top 10 Countries by Transactions")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = "plots/countries.png"
        plt.savefig(path)
        plt.close()
        story.append(Paragraph("• Top 10 Countries by Number of Transactions", self.styles["BodyText"]))
        story.append(self.get_image(path))

        # Quantity Distribution
        plt.figure(figsize=(8, 4))
        sns.histplot(self.dataset["Quantity"], bins=50, kde=True)
        plt.title("Quantity Distribution")
        plt.xlim(-50, 500)
        plt.tight_layout()
        path = "plots/quantity.png"
        plt.savefig(path)
        plt.close()
        story.append(Paragraph("• Quantity Distribution", self.styles["BodyText"]))
        story.append(self.get_image(path))

        # Invoice per Month
        self.dataset['InvoiceDate'] = pd.to_datetime(self.dataset['InvoiceDate'])
        self.dataset['Month'] = self.dataset['InvoiceDate'].dt.to_period('M')
        monthly = self.dataset.groupby('Month')['InvoiceNo'].nunique()
        plt.figure(figsize=(10, 4))
        monthly.plot()
        plt.title("Invoices per Month")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = "plots/monthly.png"
        plt.savefig(path)
        plt.close()
        story.append(Paragraph("• Monthly Invoice Trend", self.styles["BodyText"]))
        story.append(self.get_image(path))

    def add_plots_level3(self, story):
        story.append(Paragraph("<b>📈 Level-3 Deep Analysis:</b>", self.styles["Heading2"]))

        # Total Sales per Country
        self.dataset['Sales'] = self.dataset['Quantity'] * self.dataset['UnitPrice']
        country_sales = self.dataset.groupby('Country')['Sales'].sum().sort_values(ascending=False)[:10]
        plt.figure(figsize=(8, 4))
        country_sales.plot(kind='bar', color='green')
        plt.title("Top Countries by Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = "plots/sales.png"
        plt.savefig(path)
        plt.close()
        story.append(Paragraph("• Total Sales per Country", self.styles["BodyText"]))
        story.append(self.get_image(path))

        # Most Sold Items
        top_items = self.dataset.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
        plt.figure(figsize=(10, 5))
        top_items.plot(kind='bar', color='orange')
        plt.title("Most Sold Products")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = "plots/top_items.png"
        plt.savefig(path)
        plt.close()
        story.append(Paragraph("• Most Sold Items", self.styles["BodyText"]))
        story.append(self.get_image(path))


        # Price Distribution
        plt.figure(figsize=(8, 4))
        sns.boxplot(self.dataset["UnitPrice"])
        plt.xlim(0, 10)
        plt.title("Price Distribution (Limited Range)")
        plt.tight_layout()
        path = "plots/price_dist.png"
        plt.savefig(path)
        plt.close()
        story.append(Paragraph("• Price Distribution", self.styles["BodyText"]))
        story.append(self.get_image(path))

    def get_image(self, path, width=400, height=200):
        from reportlab.platypus import Image
        return Image(path, width=width, height=height)

if __name__ == "__main__":
    
    level = input("Enter Analysis Level (1, 2, 3): ").strip()
    if level not in ['1', '2', '3']:
        print("❌ Invalid input. Choose 1, 2, or 3.")
    else:
        analysis = Analysis(level)
        analysis.run_analysis()
