#!/usr/bin/env python3

################################################################################
## Module-import

import pandas as pd
import numpy as np
import os
import sys


################################################################################
## Initialization
import argparse
parser = argparse.ArgumentParser(description = 'Search all rows of a table for a specific term.')

parser.add_argument('-i', '--input', help = "Input-file", required = True)
parser.add_argument('-n', '--sheet_nr', help = "Number of the excel sheet in the input-file to read", default = 0)
parser.add_argument('-c', '--column', nargs = '+', help = "One or multiple columns to search in [default: all]", default = ['all'])
parser.add_argument('-s', '--search', nargs = '+', help = "One or multiple terms to search for", default = False)
parser.add_argument('-o', '--output', help = "Name of the output-directory", default = os.getcwd())
parser.add_argument('--md', help = "Activate output of result-file in .md-format", action = 'store_true', default = False)
parser.add_argument('--csv', help = "Deactivate output of result-file in .csv-format", action = 'store_false', default = True)
parser.add_argument('--isnull', help = "Search for NaN [overwrites -s]", action = 'store_true', default = False)
parser.add_argument('--notnull', help = "Search for notNaN [overwrites -s]", action = 'store_true', default = False)

#parsing:
arg = parser.parse_args()

#define arguments as variables:
input_file = arg.input
sheet_nr = int(arg.sheet_nr)
search_column = arg.column
search_term = arg.search
output_path = arg.output
md_output = arg.md
csv_output = arg.csv
search_isnull = arg.isnull
search_notnull = arg.notnull

if csv_output == False and md_output == False:
  sys.exit('Please activate at least one output-format')

if search_term == False and search_isnull == False and search_notnull == False:
  sys.exit('>> One of the following flags is required to start a search: [-s] [--isnull] [--notnull] <<')

if search_isnull == True and search_notnull == True:
  sys.exit('>> Can´t search for null & notnull at the same time. <<')

if type(sheet_nr) != int:
  sys.exit('>> Please insert a single number to define the the sheet to read from. <<')


################################################################################
## Set up results-directory & change working-directory if necessary

#check if output-directory exists & create a Results-directory in it:
output_path = str(output_path) + '/py_grep_results'
os.makedirs(output_path, exist_ok = True)

#check if output-flag was used:
if output_path != os.getcwd():
        
    #change working directory to the path
    os.chdir(output_path)


################################################################################
## Configure searched terms

if search_isnull == True:
  search_term = ['NaN']
elif search_notnull == True:
  search_term = ['not NaN']


################################################################################
## File-conversion

if ".xls" in input_file:
  data = pd.read_excel(input_file, sheet_name = sheet_nr)

elif ".csv" in input_file or ".tsv" in input_file:
  data = pd.read_csv(input_file)

else:
  sys.exit('>> Unsupported input-file format. Use .xls, .csv or .tsv instead <<')

data = data.astype(str)


################################################################################
## Search

if search_column[0] == 'all':
  if search_isnull == True: 
    data_searched = data[data.isna().any(axis=1)]
  elif search_notnull == True:
    data_searched = data[data.notnull().any(axis=1)]
  else:
    search_str = '|'.join(search_term)
    stacked_df = data.stack() # convert entire data frame into a series of values
    data_searched = data.iloc[stacked_df[stacked_df.str.contains(search_str,na=False)].index.get_level_values(0).drop_duplicates()]

else:
  if search_isnull == True:
    data_searched = data[data[search_column].isna().any(axis=1)]
  elif search_notnull == True:
    data_searched = data[data[search_column].notnull().any(axis=1)]
  else:
    data_searched = data[data[search_column].isin(search_term).any(axis=1)]


################################################################################
## Output

output_file_basename = "ROWGRAB_" + '_'.join(search_column) + "_searched" 

if len(search_column) == 1:
  search_column_str = "Searched column: ["
else:
  search_column_str = "Searched columns: ["

if len(search_term) == 1:
  search_term_str = "] for following term: ["
else:
  search_term_str = "] for following terms: ["

searched_string = search_column_str + '; '.join(search_column) + search_term_str + '; '.join(search_term) + "]."

if md_output == True:
  output_file_md_name = output_file_basename + ".md"
  result_md = data_searched.to_markdown()
  result_file_md = open(output_file_md_name, "w")
  result_file_md.write(searched_string)
  result_file_md.write('\n')
  result_file_md.write(result_md)
  result_file_md.close()

if csv_output == True:
  output_file_csv_name = output_file_basename + ".csv"
  result_csv = data_searched.to_csv()
  result_file_csv = open(output_file_csv_name, "w")
  result_file_csv.write(searched_string)
  result_file_csv.write('\n')
  result_file_csv.write(result_csv)
  result_file_csv.close()