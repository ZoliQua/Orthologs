
filtered_eggnog_file = "data/eggnog/eggnog6/e6.og2seqs_and_species_filtered_7_species_2759_level.tsv"
export_filename = "data/eggnog/eggnog6db_7_species_by_groups.tsv"

# Updated taxon dictionary
taxon_dict = {
    '9606': 'H. sapiens',
    '7955': 'D. rerio',
    '6239': 'C. elegans',
    '3702': 'A. thaliana',
    '7227': 'D. melanogaster',
    '284812': 'S. pombe',
    '4932': 'S. cerevisiae',
}

# Initialize a dictionary to store unique proteins for each taxon
protein_lists = {taxon_id: set() for taxon_id in taxon_dict}

# Function to format each line for the eggnog6db_7_species_by_groups.tsv file
def format_line(columns):
    line = {
        'kog_group_name': columns[1],
        'number_of_species': columns[2],
        '9606': [],
        '7955': [],
        '6239': [],
        '3702': [],
        '7227': [],
        '284812': [],
        '4932': []
    }
    members = columns[5].split(',')
    for member in members:
        taxon_id, protein = member.split('.', 1)
        if taxon_id in line:
            line[taxon_id].append(protein)
            protein_lists[taxon_id].add(protein)  # Add protein to the set for unique protein collection
    return line

# Open the filtered file and create eggnog6db_7_species_by_groups.tsv
with open(filtered_eggnog_file, 'r') as filtered_file, open(export_filename, 'w') as result_file:
    for line in filtered_file:
        columns = line.strip().split('\t')
        formatted_line = format_line(columns)
        for taxon_id in taxon_dict:
            formatted_line[taxon_id] = ','.join(formatted_line[taxon_id])
        result_file.write('\t'.join([formatted_line[key] for key in formatted_line]) + '\n')

# Write the unique protein lists to separate files for each taxon
for taxon_id, proteins in protein_lists.items():
    with open(f'data/eggnog/eggnog6db_{taxon_id}_protein_list.tsv', 'w') as protein_file:
        for protein in proteins:
            protein_file.write(protein + '\n')