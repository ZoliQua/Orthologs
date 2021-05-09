
# QuickGO GO Slim Parser
#
# What this file do?
# Retrieve GO SLIM data from GeneOntology website
#
# Code written by Zoltan Dul, PhD (2021)
# Contact me at zoltan dul [at] gmail.com
#

import urllib.request as rqs
import json


url_goslim = "http://current.geneontology.org/ontology/subsets/goslim_generic.json"
hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': "Magic Browser"}

page = rqs.Request(url_goslim, headers=hdr)
content = rqs.urlopen(page).read()
my_slim = json.loads(content)

GOslim_list = []
GOslim_dict = {}

for this_goID in my_slim['graphs'][0]['nodes']:
	go_slim = this_goID['id'].split("/")[-1]

	if go_slim[0:3] == "GO_":
		GOslim_list.append(go_slim)
		GOslim_dict[this_goID['lbl']] = go_slim

print(f"GO Slim parser read {len(GOslim_dict)} GO IDs.")