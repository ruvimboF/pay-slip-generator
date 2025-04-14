
import pandas as pd
from fpdf import FPDF
import yagmail
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("C:/Users/uncommonstudent/Desktop/PAY SLIP GENERATOR PROJECT/.env")

from pathlib import Path
import os
from dotenv import load_dotenv

# Print current working directory to verify location
print(f"Current directory: {Path.cwd()}")

# Load .env file explicitly with path verification
env_path = Path('.') / '.env'
print(f".env file exists: {env_path.exists()}")
print(f".env file contents:\n{env_path.read_text()}")

load_dotenv(dotenv_path=str(env_path))


try:
    email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')
    
    print("Environment variables loaded successfully:")
    print(f"Email address: {email}")
    print(f"Password set: {'yes' if password else 'no'}")
except Exception as e:
    print(f"Error loading environment variables: {str(e)}")                 
# Fetch email credentials from .env file
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Ensure credentials exist
if not SENDER_EMAIL or not SENDER_PASSWORD:
    raise ValueError("Email credentials are not set in the .env file!")

# Load Excel File and Strip Whitespace from Column Names
df = pd.read_excel("employees.xlsx")
df.columns = df.columns.str.strip()

# Verify Column Names (For Debugging)
print("Updated Columns in Excel File:", df.columns)

# Ensure Required Columns Exist
expected_columns = ["Employee ID", "Names", "Email", "Basic Salary", "Allowances", "Deductions"]
for col in expected_columns:
    if col not in df.columns:
        raise KeyError(f"Column '{col}' is missing from the Excel file!")

# Remove duplicate entries based on Employee ID
df = df.drop_duplicates(subset="Employee ID")

# Calculate Net Salary
df["Net Salary"] = df["Basic Salary"] + df["Allowances"] - df["Deductions"]

# Define a log file to track sent emails
sent_log = "sent_payslips.log"
if os.path.exists(sent_log):
    with open(sent_log, "r") as f:
        sent_ids = set(f.read().splitlines())
else:
    sent_ids = set()

# Function to Generate Payslip PDFs
class PayslipPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 20)
        self.set_text_color(0, 0, 0)  # Black color for header text
        self.set_fill_color(200, 200, 200)  # Light gray background
        self.cell(0, 10, "RUES AVON", ln=True, align="C", fill=True)
        self.ln(10)

    def footer(self):
        # Add page number in the footer
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"This is an automated payslip {self.page_no()}", align="C")

    def generate_payslip(self, employee):
        self.set_font("Arial", size=12)
        self.set_text_color(0, 0, 0)  # Reset text color to black

        # Structured table for employee details
        details = [
            ("Employee ID", employee["Employee ID"]),
            ("Names", employee["Names"]),
            ("Email", employee["Email"]),
            ("Basic Salary", f"${employee['Basic Salary']:.2f}"),
            ("Allowances", f"${employee['Allowances']:.2f}"),
            ("Deductions", f"${employee['Deductions']:.2f}"),
            ("Net Salary", f"${employee['Net Salary']:.2f}")
        ]
        
        for label, value in details:
            self.set_font("Arial", "B", 12)  # Bold for labels
            self.cell(50, 10, f"{label}:", border=1, align="L")
            self.set_font("Arial", "", 12)  # Regular for values
            self.cell(0, 10, str(value), border=1, ln=True, align="L")

# Generate and Save Payslip PDFs to the Specified Folder
output_folder = "C:/Users/uncommonstudent/DESKTOP/rue.rue/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)  # Create the folder if it doesn't exist

for _, row in df.iterrows():
    if row['Employee ID'] in sent_ids:
        print(f"Payslip already sent for Employee ID {row['Employee ID']}. Skipping...")
        continue

    try:
        pdf = PayslipPDF()
        pdf.add_page()
        pdf.generate_payslip(row)
        
        # Explicitly save the PDF to the desired folder
        filename = os.path.join(output_folder, f"{row['Employee ID']}_payslip.pdf")
        pdf.output(filename)
        print(f"Saved {filename}")
    except Exception as e:
        print(f"Error saving PDF for {row['Employee ID']}: {e}")
        continue

print("Payslips generated successfully!")

# Email Setup
try:
    yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
    print("✅ Connected to Gmail SMTP server.")
except Exception as e:
    print(f"❌ Failed to connect to Gmail SMTP: {e}")
    exit()

# Send Payslips via Email
for _, row in df.iterrows():
    if row['Employee ID'] in sent_ids:
        print(f"Email already sent to Employee ID {row['Employee ID']}. Skipping...")
        continue

    try:
        filename = os.path.join(output_folder, f"{row['Employee ID']}_payslip.pdf")
        print(f"📤 Sending to {row['Email']}...")

        yag.send(
            to=row["Email"],
            subject="Your Monthly Payslip",
            contents=f"Dear {row['Names']},\n\nPlease find your payslip attached.\n\nBest regards,\nYour Company",
            attachments=filename
        )
        print(f"✅ Sent to {row['Email']}")
        
        # Log the sent Employee ID to the log file
        with open(sent_log, "a") as f:
            f.write(row['Employee ID'] + "\n")
    except Exception as e:
        print(f"❌ Failed to send to {row['Email']}: {e}")

print("🏁 All payslips sent!")


