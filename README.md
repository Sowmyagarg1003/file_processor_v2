# Project Decription

The CSV File Processor monitors a specified folder for new CSV files, validates their structure, and stores valid data in a PostgreSQL database. It categorizes files into three folders:
/data: Contains new files awaiting processing.
/error: Holds files with structural errors.
/done: Stores successfully processed files.

## Installation 
### Prerequisites
1. Python 3.13 - https://www.python.org/downloads/
2. PostgreSQL - https://www.postgresql.org/download/

### Setup Instructions
1. Clone the repository:
git clone https://github.com/username/file_processor_v2.git
2. Navigate into the project directory:
cd file_processor_v2
3. Install required dependencies:
pip install -r requirements.txt
4. Configure PostgreSQL Database:
The database configurations are stored in the config.py file. No manual database creation is required. When a CSV file is validated and moved to the /done folder, the application will automatically create the necessary database and tables to store the data.

Ensure that the config.py file contains the correct database connection settings, such as:
```
DB_HOST = 'localhost'

DB_PORT = 5432

DB_NAME = 'csv_processor_db'

DB_USER = 'your_username'

DB_PASSWORD = 'your_password'
```
## Usage

Ensure /data, /error, and /done folders are created in the project directory.

### Run the application:
python main.py

### Accessing the Database from the Terminal

To access PostgreSQL from the terminal, follow these steps:

1. Open the Terminal
   
Launch your terminal or command prompt.

2. Connect to PostgreSQL
   
Use the psql command to access PostgreSQL:
```
psql -U your_username -d your_database
```

Replace your_username with your PostgreSQL username (usually postgres if you haven’t changed it) and your_database with the name of the database you want to access. For example:
```
psql -U postgres -d csv_processor_db
```

If you want to connect to the default database (postgres), you can simply use:
```
psql -U postgres
```

3. Specify the Host (Optional)
   
If you're connecting to a PostgreSQL server running on a different host, use the -h option:
```
psql -U your_username -h your_host -d your_database
```

Replace your_host with the hostname or IP address of the server.

4. Enter the Password
   
If prompted, enter the password for the specified user.

5. Common psql Commands
 
Once connected, here are some basic commands you can use:

List all databases:
```
\l
```

Connect to a database:
```
\c database_name
```

List all tables:
```
\dt
```

View a table’s structure:
```
\d table_name
```

Quit psql:
```
\q
```

### SQL Commands for Working with Tables

Once you're in the database, you can use SQL commands to query and modify tables:

Select all rows from a table:
```
SELECT * FROM table_name;
```

Drop a table:
```
DROP TABLE IF EXISTS table_name;
```

## Folder Structure

-> /data: Stores new files awaiting processing.

-> /error: Stores files with structural or processing errors.

-> /done: Stores files successfully processed and stored in the database.

## File Validation Rules

The application performs the following validation checks on each CSV file:

1. Encoding Detection: Detects the file encoding using chardet to ensure proper parsing.
   
2. Delimiter Validation: Ensures the file uses the expected delimiter (default is a comma).
   
3. Column Count Consistency: Ensures each row contains the same number of columns as defined in the header.
 
4. Header Validation: Detects missing column headers (empty header names) and also flags duplicate column names.
   
5. Duplicate Rows: Checks the file for any duplicate rows and flags them.
   
6. Data Type Validation: Validates that specific columns (e.g., "Age", "Salary") contain only numeric values. Rows with invalid data types are flagged.
    
7. Double Commas Check: Detects occurrences of double commas (,,) within data fields, which indicate potential data issues.
    
8. Regex Validation for Specific Columns: Applies regular expressions to validate data formats in specific columns:

Email: Checks for valid email addresses.
Phone: Validates phone numbers.
URL: Verifies URL formats.
Date: Ensures the format is YYYY-MM-DD.
    
9. Chunk-Based Processing: Processes large files in manageable chunks (default is 100 rows per chunk) to optimize memory usage and scalability.
        
Each of these checks ensures the data quality before processing and storage. Files failing any of these validations are moved to the /error folder.

## Database Schema

The application creates a table in PostgreSQL from the CSV file's headers. Each table includes the following:

1. Primary Key: table_s_no - A serial column used as the primary key for each row.
   
2. Data Columns: Each column from the CSV file is stored as a TEXT type in the database.
   
### Table Creation:

When a CSV file is processed, a table is created automatically (if it does not already exist) using the column names from the CSV header. The columns are all stored as TEXT type for simplicity, but you can modify this as needed based on your data requirements.

Example:

For a CSV file with the following headers:

Name, Age, Email

The corresponding SQL table will have:

table_s_no as the primary key.

Name, Age, Email columns as TEXT.

Inserting Data:

The application inserts the data into the table in chunks of 100 rows. This batch processing helps avoid memory issues for large files.


## Contact
For any questions or feedback, please reach out to Sowmya at sowmyagarg73@gmail.com.



    



