
source_eggnog_file = "data/eggnog/eggnog6/e6.og2seqs_and_species.tsv"
export_eggnog_file = "data/eggnog/eggnog6/e6.og2seqs_and_species_filtered_7_species_2759_level.tsv"

# Dictionary of taxons we are interested in
taxon_dict = {
    '9606': 'H. sapiens',
    '7955': 'D. rerio',
    '6239': 'C. elegans',
    '3702': 'A. thaliana',
    '7227': 'D. melanogaster',
    '4896': 'S. pombe',
    '284812': 'S. pombe',
    '4932': 'S. cerevisiae',
    '559292': 'S. cerevisiae'
}

new_line = {'9606': [], '7955': [], '6239': [], '3702': [], '7227': [], '284812': [], '4932': []}

# Open the original file in read mode and a new file in write mode
with open(source_eggnog_file, 'r') as original_file, open(export_eggnog_file, 'w') as filtered_file:
    for line in original_file:
        columns = line.strip().split('\t')

        if columns[0].strip() != "2759":
            continue

        # Process members (column 6) and species (column 5)
        members = columns[5].split(',')
        species = columns[4].split(',')

        # Filter members and species based on the taxon_dict
        filtered_members = [member for member in members if member.split('.')[0] in taxon_dict]
        filtered_species = set([member.split('.')[0] for member in filtered_members])  # Unique species IDs from filtered members

        # If there are any members left after filtering, write the line to the new file
        if filtered_members:
            # Update the number of species and members based on the filtering
            columns[2] = str(len(filtered_species))
            columns[3] = str(len(filtered_members))
            columns[4] = ','.join(filtered_species)
            columns[5] = ','.join(filtered_members)

            # Write the updated line to the new file
            filtered_file.write('\t'.join(columns) + '\n')