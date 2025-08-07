
# QuickGO Parser
#
# What this file do?
# Containing the variables that more than one script use
#
# Code written by Zoltan Dul, PhD (2021)
# Contact me at zoltan dul [at] gmail.com
#

# taxon ids: 9606, 7955, 6239, 3702, 7227, 4896, 4932, 284812, 559292

from quickGO_get_GOslim import *
from quickGO_functions_container import *
import requests, sys
import os

# Print start time to the console
start_time = time.time()
this_file = "quickGO_query_3_one_goterm_alltaxon.py"
TimeNow("start", this_file)

# List of TaxIDs to check
list_of_taxids = [9606, 7955, 6239, 3702, 7227, 4896, 4932, 284812, 559292]
# Directory of export GO files
dir_export = "data/all_taxon/"

for go_name, go_id in GOslim_dict.items():

    go_id = "GO_0007049"
    taxid = "00000"

    # Export filename
    this_filename = dir_export + go_id + ".tsv"

    # Check file status
    if os.path.exists(this_filename):
        os.remove(this_filename)
        logging.info(this_filename + " has been removed.")

    phase_name = "\'GO Request for " + go_id.replace("_", ":") + " (" + go_name + ")\'"
    logging.info(phase_name + " start.")

    req_url = GOSlimRequestURL_AllTaxon(go_id)
    #req_url = "https://www.ebi.ac.uk/QuickGO/services/annotation/downloadSearch?goId=GO%3A0003014&goUsageRelationships=is_a%2Cpart_of%2Coccurs_in"
    r = requests.get(req_url, headers={"Accept": "text/tsv"})

    if not r.ok:
        logging.error(r)
        r.raise_for_status()
        # sys.exit()
        continue

    responseBody = r.text
    responseBodyArray = responseBody.split("\n")

    # Remove the last line, while it is an empty line
    responseBodyArray.pop()

    phase_name = "\'GO Process " + go_id.replace("_", ":") + ", lines " \
                 + str(len(responseBodyArray)) + "\'"

    TimeNow(phase_name, False, start_time)
    logging.info(phase_name + " - end.")

    WriteTSVFile(go_id, taxid, this_filename, responseBodyArray, "\t")

    #  SleepWakeUp()
    break

# Print end time to the console
TimeNow("end", this_file, start_time)
