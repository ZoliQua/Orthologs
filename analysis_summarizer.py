
# EGGNOG RANDOM SELECTOR
#
# What this file do?
# This file get p-values from STRING DB for a randomly selected pool of proteins, randomly selecting the pool.
#
# Code written by Zoltan Dul, PhD (2021)
# Contact me at zoltan dul [at] gmail.com
#

# Import libraries
import requests  # python -m pip install requests
import pandas as pd
# Import local functions
from stringDB_functions import *
# Import local variables
from stringDB_variables import *

#######################
# SET FILE PARAMETERS #
#######################

isTest = False
dir_export = "export/"
dir_log = "logs/"
# list_goids = ["go-0000502", "go-0000902", "go-0000910", "go-0002376", "go-0003013", "go-0005975", "go-0006099",
#               "go-0006412", "go-0006629", "go-0006914", "go-0007049", "go-0007568", "go-0008361", "go-0009295",
#               "go-0051301", "go-0051726"]

list_goids = ["go-0006259", "go-0006397", "go-0006399"]


# START LOGGING
# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename1, level=logging.DEBUG)

# Current selection for test
# taxid = taxon_list[0]

bottles_list = (0.00, 0.33, 0.66, 1.00)

for str_goid in list_goids:

	row2print = [str_goid.replace("-","_")]

	########################################################
	# Open GO file in Pandas as a DataFrame for this TaxID #
	########################################################
	selected_cols = [	"Group ID",
						"Average H/M",
						"Total H/M",
						"Hit Proteins",
						"Total Proteins",
						"Hit Species",
						 "Total Species" ]

	column_name_hm_value = "Average H/M"

	go = pd.read_csv("data/" + str_goid + "-ordered.tsv", sep="\t", usecols=selected_cols)

	# Print & Log pd read
	#print(f"Pandas DataFrame have {len(go)} lines load from {str_goid} file.")

	# Logging
	log_calls = []

	# Create P-value array for the whole taxid
	p_val_array = {}

	bottle_counter = 0
	for num in bottles_list:

		if bottle_counter == (len(bottles_list) - 1):
			continue

		# Create array for H/M sums
		hm_sum_array = {}
		hm_sum = 0

		# go_sampled = go # go.sample(n=100)

		nr1 = bottles_list[bottle_counter]
		nr2 = bottles_list[bottle_counter + 1]
		go_between_average_hm = go["Average H/M"].between(nr1, nr2)
		number_of_lines = len(go[go_between_average_hm].index)
		bottle_counter += 1

		row2print.append(number_of_lines)
		row2print.append("{:.4f}".format(go[go_between_average_hm]["Hit Proteins"].mean()))
		row2print.append("{:.4f}".format(go[go_between_average_hm]["Total Proteins"].mean()))
		row2print.append("{:.4f}".format(go[go_between_average_hm]["Hit Species"].mean()))
		row2print.append("{:.4f}".format(go[go_between_average_hm]["Total Species"].mean()))

	print(row2print)


