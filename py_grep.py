#!/usr/bin/env python3

################################################################################
## Module-import

import pandas as pd
from pandas.core.common import flatten
import numpy as np
import os
import sys


################################################################################
## Initialization
import argparse
parser = argparse.ArgumentParser(description = 'Search all rows of a table for a specific term.')

parser.add_argument('-i', '--input', help = "Input-file", required = True)
parser.add_argument('-n', '--sheet', nargs = '+', help = "Number or name of the excel sheet(s) in the input-file to read [default: all]", default = [])
parser.add_argument('-c', '--column', nargs = '+', help = "One or multiple columns to search in [default: all]", default = ['all'])
parser.add_argument('-s', '--search', nargs = '+', help = "One or multiple terms to search for", default = False)
parser.add_argument('-o', '--output', help = "Name of the output-directory", default = os.getcwd())
parser.add_argument('-r', '--reverse', help = "Invert the search to search everything expect the search-terms", action = 'store_true', default = False)
parser.add_argument('-d', '--deact_search_str', help = "Deactivates printing of searched-string in first row", action = 'store_true', default = False)
parser.add_argument('--md', help = "Activate output of result-file in .md-format", action = 'store_true', default = False)
parser.add_argument('--csv', help = "Activate output of result-file in .csv-format", action = 'store_true', default = False)
parser.add_argument('--tsv', help = "Deactivate output of result-file in .tsv-format", action = 'store_false', default = True)
parser.add_argument('--isnull', help = "Search for NaN [overwrites -s]", action = 'store_true', default = False)
parser.add_argument('--notnull', help = "Search for notNaN [overwrites -s]", action = 'store_true', default = False)

#parsing:
arg = parser.parse_args()

#define arguments as variables:
deactivate_search_str = arg.deact_search_str
input_file = arg.input
invert_search =  arg.reverse
sheet = arg.sheet
search_column = arg.column
search_term = arg.search
output_path = arg.output
md_output = arg.md
csv_output = arg.csv
tsv_output = arg.tsv
search_isnull = arg.isnull
search_notnull = arg.notnull

if tsv_output == False and csv_output == False and md_output == False:
	sys.exit('>> Please activate at least one output-format. <<')

if search_term == False and search_isnull == False and search_notnull == False:
	sys.exit('>> One of the following flags is required to start a search: [-s] [--isnull] [--notnull] <<')

if search_isnull == True and search_notnull == True:
	sys.exit('>> Can??t search for null & notnull at the same time. <<')


################################################################################
## Function declarations

def column_keyError(column, column_list):
	if column != 'all' and column not in column_list:
		sys.exit(">> KeyError: Column ['%s'] doesn??t exist in the dataframe. <<" %column)

def int_convert(element):
	try:
		return int(element)
	except (ValueError, TypeError):
		return element 

def range_parse(element, max_sheets):
	parsed_sheet = []
	if '-' in str(element):
		element_subparts_list = str(element).split('-')
		if element_subparts_list[0] != '':
			element_first_subpart = int(element_subparts_list[0])
		else:
			element_first_subpart = 0
		if element_subparts_list[1] != '':
			element_second_subpart = int(element_subparts_list[1]) + 1
		else:
			element_second_subpart = max_sheets
		parsed_sheet.extend(list(range(element_first_subpart,element_second_subpart)))
	else:
		parsed_sheet.append(element)
	return parsed_sheet


################################################################################
## Set up results-directory & change working-directory if necessary

#check if output-directory exists & create a Results-directory in it:
output_path = str(output_path) + '/pygrep_results'
os.makedirs(output_path, exist_ok = True)

#check if output-flag was used:
if output_path != os.getcwd():
	#change working directory to the path
	os.chdir(output_path)


################################################################################
## File-conversion

excel_extensions_list = ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']

if any(excel_extension in input_file for excel_extension in excel_extensions_list):
	max_sheet_nr = len(pd.ExcelFile(input_file).sheet_names)
	sheet = [int_convert(element) for element in sheet]
	parsed_sheet = list(flatten([range_parse(element,max_sheet_nr) for element in sheet]))

	if len(parsed_sheet) == 0:
		data = pd.concat(pd.read_excel(input_file, sheet_name = None), ignore_index = True)
	elif len(parsed_sheet) == 1:
		data = pd.read_excel(input_file, sheet_name = parsed_sheet[0])   
	else:
		data = pd.concat([pd.read_excel(input_file, sheet_name = number) for number in parsed_sheet], ignore_index = True)

elif ".csv" in input_file:
	data = pd.read_csv(input_file)

elif ".tsv" in input_file:
	data = pd.read_csv(input_file, sep='\t')

else:
	sys.exit('>> Unsupported input-file format. Use excel-, .csv- or .tsv-format instead. <<')

data = data.astype(str).replace('nan', np.nan)

[column_keyError(column, list(data.columns)) for column in search_column]


################################################################################
## Search

if search_column[0] == 'all':
	if search_isnull == True: 
		data_searched = data[data.isna().any(axis=1)]
		search_term = ['NaN']
	elif search_notnull == True:
		data_searched = data[data.notnull().any(axis=1)]
		search_term = ['not NaN']
	else:
		search_str = '|'.join(search_term)
		stacked_df = data.stack(dropna = False) # convert entire data frame into a series of values
		if invert_search == False:
			data_searched = data.iloc[stacked_df[stacked_df.str.contains(search_str, case = False, na = False)].index.get_level_values(0).drop_duplicates()]
		else:
			series_check = (~stacked_df.str.contains(search_str, case = False, na = False)).all(level=0)
			data_searched = data.iloc[series_check[series_check != False].index]

else:
	if search_isnull == True:
		data_searched = data[data[search_column].isna().any(axis=1)]
		search_term = ['NaN']
	elif search_notnull == True:
		data_searched = data[data[search_column].notnull().any(axis=1)]
		search_term = ['not NaN']
	else:
		search_str = '|'.join(search_term)
		stacked_df = data[search_column].stack(dropna = False)
		if invert_search == False:
			data_searched = data.iloc[stacked_df[stacked_df.str.contains(search_str, case = False, na = False)].index.get_level_values(0).drop_duplicates()]
		else:
			series_check = (~stacked_df.str.contains(search_str, case = False, na = False)).all(level=0)
			data_searched = data.iloc[series_check[series_check != False].index.get_level_values(0)]

################################################################################
## Output

output_file_basename = "pygrep_" + '_'.join(search_column) + "_searched" 

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
	if deactivate_search_str == False:
		result_file_md.write(searched_string)
		result_file_md.write('\n')
	result_file_md.write(result_md)
	result_file_md.close()

if csv_output == True:
	output_file_csv_name = output_file_basename + ".csv"
	result_csv = data_searched.to_csv()
	result_file_csv = open(output_file_csv_name, "w")
	if deactivate_search_str == False:
		result_file_csv.write(searched_string)
		result_file_csv.write('\n')
	result_file_csv.write(result_csv)
	result_file_csv.close()

if tsv_output == True:
	output_file_tsv_name = output_file_basename + ".tsv"
	result_tsv = data_searched.to_csv(sep='\t')
	result_file_tsv = open(output_file_tsv_name, "w")
	if deactivate_search_str == False:
		result_file_tsv.write(searched_string)
		result_file_tsv.write('\n')
	result_file_tsv.write(result_tsv)
	result_file_tsv.close()