#!/usr/bin/env python3

################################################################
## For each protein in a list save the PNG image of
## STRING network of its 15 most confident interaction partners.
##
## Requires requests module:
## type "python -m pip install requests" in command line (win)
## or terminal (mac/linux) to install the module
################################################################

import requests ## python -m pip install requests
from time import sleep

string_api_url = "https://version-11-5.string-db.org/api"
output_format = "image"
method = "network"

my_genes = ["G5ECD6", "G5EBQ8"]


##
## Construct URL
##


request_url = "/".join([string_api_url, output_format, method])

## For each gene call STRING

for gene in my_genes:

    ##
    ## Set parameters
    ##

    params = {

        "identifiers" : gene, # your protein
        "species" : 6239, # species NCBI identifier
        "add_white_nodes": 15, # add 15 white nodes to my protein 
        "network_flavor": "confidence", # show confidence links
        "caller_identity" : "www.awesome_app.org" # your app name

    }


    ##
    ## Call STRING
    ##

    response = requests.post(request_url, data=params)

    ##
    ## Save the network to file
    ##

    file_name = "%s_network.png" % gene
    print("Saving interaction network to %s" % file_name)

    with open(file_name, 'wb') as fh:
        fh.write(response.content)

    sleep(1)