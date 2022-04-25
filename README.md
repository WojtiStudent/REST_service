# REST_service
Deepsense.ai Recruitment task - Software Engineer (Python)
---------------------------------
##### Table of contents #####
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Important](#important)
-------------------------------

## Introduction ##
This is a REST service in Python which will accept a tabular data file as an input and return following data about the
file:
 - number of rows
 - number of columns
 - statitics about each column:
    - minimum value
    - maximum value
    - mean
    - 10th percentile
    - 90th percentile
    - % of missing values
    
This REST API get following endpoints:
- **/file/\<filename\>** for retrieving data about file using GET HTTP method or sending file to the server using POST HTTP method.
- **/statistics/\<filename\>/\<statistic-name\>** for retrieving specific statistic about each column in the file.

Use this **statistic-names** to get particular statistic:
**\<statistic-name\>**    | Statistic
--------------------------|-------------
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
    python testtool.py -m POST -p <path-to-file>
    ```
    2. GET data about CSV file:
    ```bash
    python testtool.py -m GET -p <filename-with-extension>
    ```
    3. DELETE data about CSV file:
    ```bash
    python testtool.py -m DELETE -p <filename-with-extension>
    ```
    4. GET data about specific statistic of CSV file:
    ```bash
    python testtool.py -m GET -p <filename-with-extension> -s <statistic-name>
    ```
## Important ##
- The server is hard-coded to run on port 5000.
    
    
