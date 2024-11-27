import re

import chardet
import pandas as pd

#rows have same number of columns as header
def validate_column_count(df):
    expected_columns = len(df.columns)
    for idx, row in df.iterrows():
        filtered_row = [value for value in row if value != '']
        if len(filtered_row) != expected_columns:
            print(f"Error: Row {idx + 1} has an incorrect number of columns. Expected {expected_columns}, got {len(filtered_row)}.")
            return False
    return True


#missing and duplicate column names
def validate_headers(df):
    # Missing
    empty_columns = [col for col in df.columns if col.strip() == '']
    if empty_columns:
        print(f"Error: The following columns have no header names: {empty_columns}")
        return False

    # Duplicate
    duplicate_columns = df.columns[df.columns.duplicated()]
    if duplicate_columns.any():
        print(f"Error: Duplicate columns found: {duplicate_columns.tolist()}")
        return False
    
    print("Headers are valid (no missing or duplicate columns).")
    return True


#duplicate rows
def validate_duplicates(df):
    if df.duplicated().any():
        print("CSV file contains duplicate rows.")
        return False
    return True

#validates columns which should be numeric only
def validate_numeric_data(df, numeric_fields):
    for col in df.columns:
        print(f"Column '{col}' dtype: {df[col].dtype}")
        
        if col in numeric_fields:
            print(f"Validating column '{col}' for numeric values...")
            invalid_rows = df.loc[pd.to_numeric(df[col], errors='coerce').isna() & df[col].notna()]
            
            if not invalid_rows.empty:
                print(f"Column '{col}' contains non-numeric values at rows: {invalid_rows.index.tolist()}")
                return False

    print("All specified numeric columns are valid.")
    return True


#only comma delimiter
def validate_delimiter(df, expected_delimiter=','):
    for row_number, row in enumerate(df.itertuples(index=False), start=1):
        line = ','.join(map(str, row))
        if expected_delimiter not in line:
            print(f"Error: Row {row_number} does not use '{expected_delimiter}' as a delimiter consistently.")
            return False
    print(f"All rows consistently use '{expected_delimiter}' as the delimiter.")
    return True


def validate_regex(df, column_name):
    regex_patterns = {
        'Email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'Phone': r'^\+?[1-9]\d{1,14}$',
        'URL': r'^(https?|ftp)://[^\s/$.?#].[^\s]*$',
        'Date': r'^\d{4}-\d{2}-\d{2}$'  # YYYY-MM-DD
    }

    if column_name in df.columns:
        regex = re.compile(regex_patterns.get(column_name, ""))
        invalid_rows = df[column_name].apply(
            lambda x: isinstance(x, str) and not regex.match(x) if pd.notna(x) else False
        )
        if invalid_rows.any():
            print(f"Column '{column_name}' contains invalid values at rows: {invalid_rows.index.tolist()}.")
            return False
    return True

def validate_double_commas(df):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, str) and ',,' in x).any():
            print(f"Column '{col}' contains double commas.")
            return False
    return True


def validate_csv(file_path):
    try:
        print("Starting CSV validation...")

        #encoding
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        print(f"Detected encoding: {encoding}")

        #chunk
        chunk_size = 100
        chunk_number = 1

        # Process the file in chunks
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, encoding=encoding, keep_default_na=False):
            print(chunk)
            print(f"\nProcessing chunk {chunk_number} with {len(chunk)} rows")

            # Validate column count
            if not validate_column_count(chunk):
                raise ValueError(f"Validation error: Column count validation failed in chunk {chunk_number}")

            # Validate headers (only for the first chunk)
            if chunk_number == 1 and not validate_headers(chunk):
                raise ValueError("Validation error: Header validation failed.")

            # Validate duplicates
            if not validate_duplicates(chunk):
                raise ValueError(f"Validation error: Duplicate rows validation failed in chunk {chunk_number}")

            # Validate the delimiter
            if not validate_delimiter(chunk):
                raise ValueError(f"Validation error: Delimiter validation failed in chunk {chunk_number}")

            # Perform regex validations for specific columns
            for column in ["Email", "Phone", "URL", "Date"]:
                if column in chunk.columns and not validate_regex(chunk, column):
                    raise ValueError(f"Validation error: Regex validation failed for column '{column}' in chunk {chunk_number}")

            # Validate data types for numeric columns
            numeric_fields = ["Age", "Salary", "Price", "Quantity", "Height", "Weight", "Distance", "Marks"]
            if not validate_numeric_data(chunk, numeric_fields):
                
                raise ValueError(f"Validation error: Data type validation failed in chunk {chunk_number}")
            
            if not validate_double_commas(chunk):
                raise ValueError(f"Double commas validation failed in chunk {chunk_number}")

            print(f"Chunk {chunk_number} passed all validations")
            chunk_number += 1

        print(f"\nCSV file '{file_path}' passed all validations")
        return True

    except ValueError as ve:
        print(ve)
        return False
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return False
    except pd.errors.ParserError as pe:
        print(f"Parser error: {pe}")
        return False
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return False
    except Exception as e:
        print(f"Unexpected error during CSV validation: {e}")
        return False
