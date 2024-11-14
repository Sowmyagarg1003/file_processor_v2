Project Description
The CSV File Processor monitors a specified folder for new CSV files, validates their structure, and stores valid data in a PostgreSQL database. It categorizes files into three folders:
/data: Contains new files awaiting processing.
/error: Holds files with structural errors.
/done: Stores successfully processed files.

Table of Contents
1. Installation
2. Usage
3. Folder Structure
4. File Validation Rules
5. Database Schema
6. Contact

Installation
Prerequisites
1. Python 3.13 - https://www.python.org/downloads/
2. PostgreSQL - https://www.postgresql.org/download/

Setup Instructions
1. Clone the repository:
git clone https://github.com/username/file_processor_v2.git
2. Navigate into the project directory:
cd file_processor_v2
3. Install required dependencies:
pip install -r requirements.txt
4. Configure PostgreSQL Database:
The database configurations are stored in the config.py file. No manual database creation is required. When a CSV file is validated and moved to the /done folder, the application will automatically create the necessary database and tables to store the data.
Ensure that the config.py file contains the correct database connection settings, such as:
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'csv_processor_db'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'

Usage
Ensure /data, /error, and /done folders are created in the project directory.
Run the application:
python main.py
Run the database:
psql -U your_username -h your_host -d your_database

Folder Structure
-> /data: Stores new files awaiting processing.
-> /error: Stores files with structural or processing errors.
-> /done: Stores files successfully processed and stored in the database.

File Validation Rules
The application performs the following validation checks on each CSV file:
1. Encoding Detection: Detects the file encoding using chardet.
2. Delimiter Validation: Ensures the file uses the expected delimiter (default is a comma).
3. Empty Column Analysis: Calculates the percentage of missing values in each column.
4. Column Count Consistency: Verifies that each row has the same number of columns as the header.
5. Header Validation: Checks for missing or duplicate column headers.
6. Empty Values Threshold: Flags columns that exceed a specified missing values threshold (default is 30%).
7. Duplicate Rows: Detects any duplicate rows in the file.
8. Data Type Validation: Checks that columns with numeric data types contain only numeric values.
9. Double Commas Check: Detects double commas within data fields.
10. Email Format Validation: Uses a regular expression to validate email formats in the specified column.
Each of these checks ensures the data quality before processing and storage. Files failing any of these validations are moved to the /error folder.

Database Schema
The application creates a table in PostgreSQL from the CSV file's headers. Each table includes the following:
1. Primary Key: table_s_no - A serial column used as the primary key for each row.
2. Data Columns: Each column from the CSV file is stored as a TEXT type in the database.
Table Creation:
When a CSV file is processed, a table is created automatically (if it does not already exist) using the column names from the CSV header. The columns are all stored as TEXT type for simplicity, but you can modify this as needed based on your data requirements.
Example:
For a CSV file with the following headers:
Name, Age, Email
The corresponding SQL table will have:
table_s_no as the primary key.
Name, Age, Email columns as TEXT.
Inserting Data:
The application inserts the data into the table in chunks of 100 rows. This batch processing helps avoid memory issues for large files.


Contact
For any questions or feedback, please reach out to Sowmya at sowmyagarg73@gmail.com.



    


