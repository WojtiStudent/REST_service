# REST_service
---------------------------------
##### Table of contents #####
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Server flags](#server-flags)
- [Testtool flags](#testtool-flags)
-------------------------------

## Introduction ##
This is a REST service in Python which will accept a tabular data file as an input and return following data about the
file:
 - number of rows
 - number of columns
 - statitics/data about each column:
    - data type (Numeric or Text)
    - minimum value
    - maximum value
    - mean
    - 10th percentile
    - 90th percentile
    - % of missing values
    
This REST API get following endpoints:
- **/file** for uploading .csv files to the server and receiving data about that files and statistics. That usage require POST HTTP method.
- **/file/\<file_id_or_filename\>** for retrieving data about file based on file_id or general data about files with the same filename as argument. That usages require GET HTTP method.
You can also delete file via this endpoint. All you have to do is use DELETE HTTP method and pass file_id.
- **/statistics/\<filename\>/\<statistic-name\>** for retrieving specific statistic about each column in the file. That usage require GET HTTP method.

Use this **statistic-names** to get particular statistic:
**\<statistic-name\>**    | Statistic/Data
--------------------------|-------------
data_type                 | data type
minimum_val               | minimum value
maximum_val               | maximum value
mean                      | mean
percentile_10             | 10th percentile
percentile_90             | 90th percentile
percent_of_missing_values | % of missing values


## Installation ##
Python version: 3.9.11

1. Get whole project on your computer.
2. Open terminal in folder with project and enter following line to install all required packages.
```bash
pip install -r requirements.txt
```

## Usage ##
1. Run server.py.
```bash
python server.py
```
2. Now you can interact with server using f.e. testtool.py. Server accept only GET, POST and DELETE HTTP methods and get 4 ways to communicate with.
    1. POST new CSV file: 
    ```bash
    python testtool.py -m POST -p <path-to-file> -d <server_address>
    ```
    2. GET data about CSV file:
    ```bash
    python testtool.py -m GET -id <file_id> -d <server_address>
    ```
    3. DELETE data about CSV file:
    ```bash
    python testtool.py -m DELETE -id <file_id> -d <server_address>
    ```
    4. GET general data about files with passed filename:
    ```bash
    python testtool.py -m GET -f <filename> -d <server_address>
    ```
    5. GET data about specific statistic of CSV file:
    ```bash
    python testtool.py -m GET -id <file_id> -s <statistic-name> -d <server_address>
    ```
## Server flags ##
- "-p", "--port" - port on which server should run. Default 5000.
- "-dbm", "--database_name" - database name. Changing database if other database(s) exist do not delete them, but create new one. Default "statistics".

## Testtool flags ##
- "-m", "--method" - HTTP method to communicate with the server. Available options: GET, POST, DELETE. Default GET.
- "-d", "--destination" - server address. Default 127.0.0.1
- "-p", "--path" - path to file. Used only if method is POST.
- "-s", "--statistic" - name of statistic to get. Used only method is GET and file_id is passed.
- "-id", "--file_id" - file ID. Used if method is GET or DELETE.
- "-f", "--filename" - filename. Used if method is GET.
    
    
