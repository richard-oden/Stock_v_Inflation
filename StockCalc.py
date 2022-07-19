from fileinput import close
import requests
import json
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import datetime as dt
import os
import csv
from csv import writer
from csv import reader
from urllib.request import urlretrieve

from sqlalchemy import true
from api_keys import alpha_key

# Delete csv files
for folder, subfolders, files in os.walk('Stock_Growth/csv_files/'):        
    for file in files: 
        if file.endswith('.csv'): 
            path = os.path.join(folder, file) 
            os.remove(path)

header = ['sort', 'timestamp', 'open', 'high', 'low' , 'close' , 'adjusted close' , 'volume' , 'dividend amount' , 'ticker']

with open('Stock_Growth/csv_files/temp.csv', 'w', encoding='UTF8') as f:
    writer1 = csv.writer(f)

    # write the header
    writer1.writerow(header)

def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            # Pass the list / row in the transform function to add column text for this row
            transform_row(row, csv_reader.line_num)
            # Write the updated row / list to the output file
            csv_writer.writerow(row)
# Define desired stocks with ticker. Loop until input equals "null"
SYMBs = []
SYMB_Input = []
while SYMB_Input != "":
    SYMB_Input = input("Enter stock symbol. Press Enter/Return key when finished:")
    SYMBs.append(SYMB_Input)

# Stock performance - Loop through user defined stocks
for SYMB in SYMBs:
    if SYMB == "":
        break
    # Pull csv and save as "temp_stk"
    stk = pd.read_csv("https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=" + SYMB +"&apikey=" + alpha_key + "&datatype=csv")  
    stk.head()
    stk.to_csv('Stock_Growth/csv_files/temp_stk.csv')

    # Add column with stocks' ticker
    ticker = SYMB
    add_column_in_csv('Stock_Growth/csv_files/temp_stk.csv', 'Stock_Growth/csv_files/temp_stk1.csv', lambda row, line_num: row.append(ticker))

    # Append each individual stock pull to master "temp.csv" file
    csv_list = ['Stock_Growth/csv_files/temp_stk1.csv']
   
    for csv_file in csv_list:
        df = pd.read_csv(csv_file)
        df.to_csv('Stock_Growth/csv_files/temp.csv', mode ='a', header=False, index=False)

# Sort data by ticker, date(descending)
# csvData = pd.read_csv("Stock_Growth/csv_files/temp.csv")
# csvData.sort_values(["ticker", "sort"], 
#                     axis=0,
#                     ascending=[True, False], 
#                     inplace=True)
# csvData.to_csv("Stock_Growth/csv_files/temp1.csv")

# Sort by date WIP
csvData = pd.read_csv("Stock_Growth/csv_files/temp.csv")
# csvData['timestamp'] = pd.to_datetime(csvData.date, infer_datetime_format = True)
# csvData.sort_values(["ticker"],by = 'timestamp', ascending = True, inplace = True)
csvData = sorted(csvData, key = lambda row: dt.datetime.strptime(row[1], "%Y-%m-%d"))
csvData.to_csv("Stock_Growth/csv_files/temp1.csv")

# Inflation USD - Pull and save inflation data for US as "temp_inf.csv"
infl = pd.read_csv("https://www.alphavantage.co/query?function=INFLATION&apikey=" + alpha_key + "&datatype=csv")   
infl.head()

infl.to_csv('Stock_Growth/csv_files/temp_inf.csv')
