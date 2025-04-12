
# Payslip Generator

## Project Overview
This project generates payslips for employees, calculates their net salary, creates PDF payslips, and emails them. 

## How to Set Up
1. Clone this repository.
2. Install dependencies using `pip`:
   ```bash
   pip install pandas fpdf python-dotenv
   ```
3. Set up your `.env` file with your email credentials.

## How to Run
1. Place your `employees.xlsx` file in the project directory.
2. Run the script:
   ```bash
   python payslip_generator.py
   ```

## Email Configuration
Make sure to use valid email credentials in the `.env` file. For Gmail accounts, you may need to create an app password if 2FA is enabled.

   