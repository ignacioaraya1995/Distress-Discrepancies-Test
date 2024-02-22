# Real Estate Data Analysis Tool

This Python script is designed for real estate investors to analyze property distress indicators by comparing raw data against domain data, identifying discrepancies and mismatches in distress indicators, and exporting summarized results to an Excel file. The analysis focuses on various distress types such as bankruptcy, foreclosure, and tax delinquencies, among others, to aid in investment decision-making.

## Features

- **Data Processing:** Consolidates raw data from multiple CSV files, compares it against domain data from Excel files, and identifies discrepancies and mismatches.
- **Discrepancy Summary:** Generates a summary of discrepancies between raw and domain data for each distress indicator.
- **Mismatched Distress Summary:** Highlights cases where distress indicators are marked differently in raw versus domain data.
- **Excel Export:** Exports the summaries to an Excel file with two sheets for easy review and further analysis.

## Prerequisites

- Python 3.x
- Pandas Library
- Tqdm Library for progress bar visualization
- PrettyTable Library for printing tables in the console
- OpenPyXL or XlsxWriter Library for Excel file export

## Setup

1. **Install Required Libraries:**
   Ensure you have the required libraries installed. You can install them using pip:

   ```sh
   pip install pandas tqdm prettytable openpyxl xlsxwriter
   ```

2. **Directory Structure:**
   Organize your project directory as follows:

   ```
   Project/
   ├── Clients/                  # Root directory for client data
   │   ├── ClientName1/
   │   │   ├── domain data/
   │   │   ├── raw data/
   │   │   └── ...
   │   └── ClientName2/
   │       ├── domain data/
   │       ├── raw data/
   │       └── ...
   └── your_script.py            # This analysis script
   ```

   - **Domain Data:** Excel files with detailed property data, distress indicators, and other relevant information. Exclude any files with "editable" in their name.
   - **Raw Data:** CSV files with property listings and associated distress indicators.

3. **Holly Nance Domain Configuration:**
   The domain data should follow the COO configuration for export from the Holly Nance domain. Users can find this configuration in the Holly Nance domain, which includes fields for distress indicators, address, zipcode, buybox ID, likely deal score, buybox score, score, and link to the domain.

## Usage

1. **Run the Script:**
   Navigate to your project directory in the terminal and run the script:

   ```sh
   python your_script.py
   ```

2. **Review Output:**
   - The script processes each client's data, generating discrepancy and mismatch summaries printed in the console.
   - An Excel file named `<ClientName>_results.xlsx` is created in the project directory for each client, containing the discrepancy and mismatch summaries.

## Output Excel File

- **Discrepancies Summary Sheet:** Lists each distress type, the number of discrepancies, and the percentage of total properties affected, sorted by percentage.
- **Mismatched Distress Summary Sheet:** Shows distress types where the raw data marked a distress as present (1) but the domain data did not (0), including the count and percentage.

---

### Note:

- Ensure all client data is correctly placed in the respective directories under `Clients/` before running the script.
- The script automatically handles multiple raw data files per client and excludes editable domain data files.

For detailed instructions, troubleshooting, and updates, please refer to the official documentation or contact Ignacio Araya MSc.
