import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships
from collections import Counter

mirna_sequence_records_path = "/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/mirna_sequence_records.csv"

data_df = pd.read_csv(mirna_sequence_records_path, dtype={"source_db_version": str})

def plot_upset_miRNA_databases(data_df):
    db_sets = {
        db: set(data_df.loc[data_df["source_db"]==db, "miRNA_id"])
        for db in data_df["source_db"].unique()
    }
    memberships = []
    for miRNA_id in set.union(*db_sets.values()):
        present_in = tuple(db for db, ids in db_sets.items() if miRNA_id in ids)
        memberships.append(present_in)
    
    membership_counts = Counter(memberships)
    db_combinations = []
    db_counts = []
    for key, value in membership_counts.items():
        db_combinations.append(list(key))
        db_counts.append(value)
    upset_data = from_memberships(db_combinations, data=db_counts)
    UpSet(upset_data, sort_by="cardinality", show_counts=True).plot()
    plt.title("miRNA Databases Overlap")
    plt.savefig("/home/l/leitzb/miRNA/Harmonization-of-miRNA-databases/output/plots/upset_miRNA_databases.png", dpi=300)
    plt.close()

plot_upset_miRNA_databases(data_df)