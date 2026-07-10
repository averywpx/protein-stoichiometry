import requests
import pandas as pd
from io import StringIO
import time

pdb_athan_entity_df_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/train_data_entity_count_tax_arath_df.csv"
pdb_athan_uniprot_df_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/train_data_pdb_uniprot_arath_df.csv"
tair_athan_df_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/tair_arath_df.csv"
athan_uniprot_df_path_1200 = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/uniprot_arath_df_1200.csv"


# Search uniprot using single locus from TAIR
def transcript_to_uniprot(transcript_id):
    locus_id = transcript_id.rsplit(".", 1)[0]

    url = "https://rest.uniprot.org/uniprotkb/search"

    params = {
        "query": f"(xref:tair-{locus_id}) AND (organism_id:3702)",
        "format": "tsv",
        "fields": "accession,id,xref_tair,cc_subunit"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    if not response.text.strip():
        return None

    return pd.read_csv(StringIO(response.text), sep="\t")


# Search uniprot using list of locus id from TAIR
def loci_to_uniprot_dict_df(locus_ids, reviewed_only=False):
    url = "https://rest.uniprot.org/uniprotkb/search"
    rows = []

    for locus_id in locus_ids:
        print(locus_id)
        query = f"(xref:tair-{locus_id}) AND (organism_id:3702)"
        if reviewed_only:
            query += " AND (reviewed:true)"

        params = {
            "query": query,
            "format": "tsv",
            "fields": "accession,id,reviewed,xref_tair,cc_subunit,length,sequence"
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            lines = response.text.strip().splitlines()

            # Only header returned = no match
            if len(lines) <= 1:
                rows.append({"locus_id": locus_id})
                continue

            header = lines[0].split("\t")

            for line in lines[1:]:
                values = line.split("\t")
                row = dict(zip(header, values))
                row["locus_id"] = locus_id
                rows.append(row)

        except requests.RequestException as e:
            print(f"Failed to retrieve {locus_id}: {e}")
            rows.append({
                "locus_id": locus_id,
                "error": str(e)
            })

        # time.sleep(0.1)

    return pd.DataFrame(rows)

# def get_uniprot_sequence(accession):
#     url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"

#     response = requests.get(url)
#     response.raise_for_status()

#     # Remove FASTA header and join sequence lines
#     lines = response.text.strip().split("\n")
#     sequence = "".join(lines[1:])

#     return sequence


# Get uniprot info using accession id in pdb
def get_uniprot_sequence(accession):
    # WARNING: Only for A2
    accession = accession[2:-2]
    print(accession)
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        lines = response.text.strip().split("\n")
        sequence = "".join(lines[1:])

        return sequence

    except requests.RequestException as e:
        print(f"Failed to retrieve {accession}: {e}")
        return None



# # def download_athan_from_uniprot():
uniprot_url = "https://rest.uniprot.org/uniprotkb/stream"

params = {
    "query": "organism_id:3702",
    "format": "tsv",
    "fields": "accession,id,reviewed,xref_tair,cc_subunit,length, sequence"
}

response = requests.get(uniprot_url, params=params)
response.raise_for_status()

print(f"Response: {response.text}")

uniprot_df = pd.read_csv(
    StringIO(response.text),
    sep="\t"
)
    # return uniprot_df

# uniprot_df = download_athan_from_uniprot()

# print(uniprot_df.head())
# print(uniprot_df["Reviewed"].value_counts())

# uniprot_df.to_csv(
#     athan_uniprot_df_path,
#     sep="\t",
#     index=False
# )




# seq = get_uniprot_sequence("['Q9LVM1']")
# print(seq)

# # Use db_accessions in pdb to add uniprot sequence field
# pdb_athan_entity_df = pd.read_csv(pdb_athan_entity_df_path)
# pdb_athan_entity_dimer_df = pdb_athan_entity_df[pdb_athan_entity_df["stoichiometry"]=="A2"]
# pdb_athan_entity_dimer_df["uniprot_sequence"] = pdb_athan_entity_dimer_df["pdbx_db_accessions"].apply(
#     get_uniprot_sequence
# )

# # WARNING: Q9LVM1 did download uniprot_sequence
# pdb_athan_entity_dimer_df = pd.read_csv(pdb_athan_uniprot_df_path)

# test_df = pdb_athan_entity_dimer_df[pdb_athan_entity_dimer_df["pdbx_db_accessions"].str.contains("Q9FN03")]
# old_df = pdb_athan_entity_df[pdb_athan_entity_df["pdbx_db_accessions"].str.contains("Q9LVM1")]
# print(test_df[["sequences", "db_codes", "pdbx_db_accessions", "name", "uniprot_sequence"]])
# print(old_df)
# print("Q9LVM1" in pdb_athan_entity_dimer_df["pdbx_db_accessions"].tolist())


# pdb_athan_entity_dimer_df.to_csv(pdb_athan_uniprot_df_path, index=False)


# # Get uniprot id and subunit info using tair locus id
# result = transcript_to_uniprot("AT2G40940.1")
# print(result)

# # Save uniprot info to df
# tair_athan_df = pd.read_csv(tair_athan_df_path)
# locus_ids = tair_athan_df["locus"].tolist()
# # locus_ids_1200 = ["ATCG00500", "ATCG00510", "AT2G40940"]
# locus_ids_1200 = locus_ids[:1200]

# uniprot_df_1200 = loci_to_uniprot_dict_df(locus_ids_1200, reviewed_only=False)
# uniprot_df_1200.to_csv(athan_uniprot_df_path_1200, index=False)