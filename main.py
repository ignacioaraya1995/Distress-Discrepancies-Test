import os
import glob
import pandas as pd
from tqdm import tqdm
import warnings
from prettytable import PrettyTable

def format_percentage(percentage):
    """
    Formats a percentage with two decimal places and a percentage symbol.
    """
    return f"{percentage:.2f}%"

def discrepancy_summary(merged_df, distress_columns_pairs):
    total_properties = len(merged_df)
    discrepancies = []

    for raw_col, domain_col in distress_columns_pairs:
        discrepancy_count = merged_df[merged_df[raw_col] != merged_df[domain_col]].shape[0]
        percentage = (discrepancy_count / total_properties) * 100
        discrepancies.append((raw_col.split('_')[0], discrepancy_count, format_percentage(percentage)))

    discrepancies.sort(key=lambda x: float(x[2].rstrip('%')), reverse=True)

    table = PrettyTable()
    table.field_names = ['Distress Type', 'Number of Discrepancies', 'Percentage']
    for item in discrepancies:
        table.add_row(item)

    # print("Discrepancy Summary by Distress Type (Sorted by Percentage):")
    # print(table)
    
    # Export the discrepancy summary to Excel
    return discrepancies

def mismatched_distress_summary(merged_df, distress_columns_pairs):
    total_properties = len(merged_df)
    mismatches = []

    for raw_col, domain_col in distress_columns_pairs:
        mismatch_count = merged_df[(merged_df[raw_col] == 1) & (merged_df[domain_col] == 0)].shape[0]
        percentage = (mismatch_count / total_properties) * 100
        mismatches.append((raw_col.split('_')[0], mismatch_count, format_percentage(percentage)))

    mismatches.sort(key=lambda x: float(x[2].rstrip('%')), reverse=True)

    table = PrettyTable()
    table.field_names = ['Distress Type', 'Number of Mismatches', 'Percentage']
    for item in mismatches:
        table.add_row(item)

    # print("Mismatched Distress Summary (Raw Data 1, Domain Data 0):")
    # print(table)
    
    # Export the mismatched distress summary to Excel
    return mismatches

def export_to_excel(client_name, discrepancies, mismatches):
    """
    Exports the discrepancies and mismatches data to an Excel file.
    """
    # Create DataFrames from the discrepancies and mismatches data
    discrepancies_df = pd.DataFrame(discrepancies, columns=['Distress Type', 'Number of Discrepancies', 'Percentage'])
    mismatches_df = pd.DataFrame(mismatches, columns=['Distress Type', 'Number of Mismatches', 'Percentage'])

    # Define the Excel file path
    excel_file_path = f"{client_name}_results.xlsx"

    # Export to Excel with separate sheets
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        discrepancies_df.to_excel(writer, sheet_name='Discrepancies Summary', index=False)
        mismatches_df.to_excel(writer, sheet_name='Mismatched Distress Summary', index=False)

    print(f"Results exported to {excel_file_path}")

def process_data(clients_root_path='Clients'):
    # Iterate through each client's folder
    for client_path in glob.glob(os.path.join(clients_root_path, '*')):
        client_name = os.path.basename(client_path)
        print(f"Processing data for client: {client_name}")

        # Find domain data file, ignoring 'editable' files
        domain_file_path = next((f for f in glob.glob(os.path.join(client_path, 'domain data', '*.xlsx')) if 'editable' not in f), None)
        if not domain_file_path:
            print(f"No suitable domain data file found for {client_name}. Skipping.")
            continue
        
        # Assuming there might be multiple raw files and we need to process each
        raw_file_paths = glob.glob(os.path.join(client_path, 'raw data', '*.csv'))
        if not raw_file_paths:
            print(f"No raw data files found for {client_name}. Skipping.")
            continue


        # Initialize an empty list to store DataFrames
        dfs = []

        for raw_file_path in raw_file_paths:
            # Load each raw data file into a DataFrame
            partial_raw_df = pd.read_csv(raw_file_path)

            # Process the individual raw_df here as needed before consolidation
            # For example, perform cleaning, filtering, or transformations specific to each raw_df
            print(f"Processing individual raw data file: {raw_file_path}")

            # Append the processed raw_df to the list
            dfs.append(partial_raw_df)

        # Consolidate all processed raw_df DataFrames into a single DataFrame
        raw_df = pd.concat(dfs, ignore_index=True)
        # Drop duplicates based on PropertyID
        raw_df.drop_duplicates(subset='PropertyID', keep='first', inplace=True)
        # Load domain data file
        domain_df = pd.read_excel(domain_file_path)
        # Now you can proceed with processing `all_raw_data` alongside `domain_df`
        print(f"Consolidated raw data for {client_name} into a single DataFrame.")
        # Save the processed data in the client's folder
        output_file_name = f"{client_name}_distress_analysis.csv"
        output_file_path = os.path.join(client_path, output_file_name)
        
        # Assuming some processing has been done, replace the following line with actual data processing and saving
        # Example: processed_df.to_csv(output_file_path, index=False)
        print(f"Prepared to save processed data to: {output_file_path}")       

        # Normalize distress indicators to 0 for '0', 'Unknown', or empty values
        domain_df.replace({'0': 0, 'Unknown': 0, '': 0}, inplace=True)
        raw_df.replace({'0': 0, 'Unknown': 0, '': 0}, inplace=True)

        # Define distress columns mapping (extend or modify as needed)
        distress_mapping = {
            "Divorce_Distress": "DIVORCE",
            "Estate_Distress": "ESTATE",
            "Senior_Distress": "55+",
            "Preforeclosure_Distress": "PRE-FORECLOSURE",
            "Inter_Family_Distress": "INTER FAMILY TRANSFER",
            "Probate_Distress": "PROBATE",
            "Tax_Delinquent_Distress": "TAXES",
            "Low_income_Distress": "LOW CREDIT",
            "Prop_Vacant_Flag": "VACANT",
            "Absentee": "ABSENTEE",
            "Bankruptcy_Distress": "BANKRUPTCY",
            "Debt-Collection_Distress": "DEBT COLLECTION",
            "Eviction_Distress": "EVICTION",
            "Judgment_Distress": "JUDGEMENT",
            "Lien_Distress": "LIENS HOA",  # Assuming you want to map to one type of lien, adjust as needed
            "Violation_Distress": "CODE VIOLATIONS"
        }

        # Merge datasets on PropertyID
        merged_df = pd.merge(raw_df, domain_df, left_on='PropertyID', right_on='PROPERTY ID (BUYBOX)', suffixes=('_raw', '_domain'))

        # Convert "BUYBOX SCORE" to integer
        merged_df['BUYBOX SCORE'] = merged_df['BUYBOX SCORE'].fillna(0).astype(int)

        # Initialize Matched column as True
        merged_df['Matched'] = True

        distress_columns_pairs = []
        # Generate columns for each distress type using domain data names
        for raw_column, domain_column in distress_mapping.items():
            raw_col_full = f"{domain_column}_raw"
            domain_col_full = f"{domain_column}_domain"
            distress_columns_pairs.append((raw_col_full, domain_col_full))

            # Ensure integer type for comparison
            merged_df[raw_col_full] = merged_df[raw_column].fillna(0).astype(int)
            merged_df[domain_col_full] = merged_df[domain_column].fillna(0).astype(int)

            # Update 'Matched' based on distress comparison
            merged_df['Matched'] &= (merged_df[raw_col_full] == merged_df[domain_col_full])

        # Initialize tqdm progress bar
        tqdm.pandas(desc="Processing Rows")
        # Apply progress bar to a dummy operation to trigger progress display
        merged_df['Matched'] = merged_df['Matched'].progress_apply(lambda x: x)
        
        export_to_excel(client_name, discrepancy_summary(merged_df, distress_columns_pairs), mismatched_distress_summary(merged_df, distress_columns_pairs))

        

        # Prepare final columns list, ensuring distress columns are adjacent and adding "ZIP" after "ADDRESS"
        additional_columns = ['PropertyID', 'ADDRESS', 'ZIP', 'COUNT OF DISTRESSES', 'LIKELY DEAL SCORE', 'BUYBOX SCORE', 'SCORE', 'LINK PROPERTIES', 'Matched']
        distress_columns_flat = [col for pair in distress_columns_pairs for col in pair]  # Flatten the list of tuples
        final_columns = additional_columns + distress_columns_flat
        final_df = merged_df[final_columns]

        # Save the final dataframe to a new CSV file
        final_df.to_csv(output_file_path, index=False)

if __name__ == '__main__':
    # Suppress warnings
    warnings.filterwarnings('ignore')
    process_data()