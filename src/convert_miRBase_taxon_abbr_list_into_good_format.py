mirBase_list_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/data/miRBase_taxon_abbr_list"
output_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/data/miRBase_taxon_abbr_list_good_format.csv"

with open(mirBase_list_path, "r") as input_file, open(output_path, "w") as output_file:
    output_file.write("species_abbr,species_name\n")
    for line in input_file:
        parts = line.strip().split()
        species_abbr = parts[1]
        #The taxonID column where the cutoff ia made is one before the first column with ";" in it
        taxonomy_start = next(i for i, p in enumerate(parts) if ";" in p)
        species_tokens = parts[3:taxonomy_start - 1]
        species_name = " ".join(species_tokens)

        output_file.write(f"{species_abbr},{species_name}\n")