import pickle
from glob import glob
import json
import numpy as np
import pandas as pd

AMINO_ACID_LEN_LIMIT = 1000

# # training data
# input_path = "/lustre/grp/gyqlab/wangpx/protenix2/base_1_output/*"

# input_path = "/lustre/grp/gyqlab/wangpx/protenix2/base_1_output_training_AAB/*"

# input_path = "/lustre/grp/gyqlab/wangpx/protenix2/base_1_output_valid_data/*"

# input_path = "/lustre/grp/gyqlab/wangpx/protenix2/base_1_output_valid_AAB/*"

# Athan mix
# input_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/protenix_output/base_1_output_athan_900/*"
input_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/protenix_output/base_1_output_homodimer_athan_900_v1/*"

# train entity df
# entity_df_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/train_data_entity_count_df.csv"
# # valid entity df
# entity_df_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/valid_data_entity_count_df.csv"
# tair 34 entity df
entity_df_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/homodimer_uniprot_tair_arath_df.csv"






# training A
# iptm_csv_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_training_A.csv"
# training AAB
# iptm_csv_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_training_AAB.csv"
# iptm_csv_intermediate_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_training_AAB_intermediate.csv"

# # valid A
# iptm_csv_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_valid_A_2.csv"
# # valid AAB
# iptm_csv_intermediate_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_valid_AAB_intermediate.csv"
# iptm_csv_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_valid_AAB.csv"


# athan mixed
# iptm_csv_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/results/StoPred_result_analysis/result_df_filterd_by_iptm_athan_mixed_900.csv"
# iptm_csv_intermediate_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/results/StoPred_result_analysis/result_df_filterd_by_iptm_athan_mixed_900_intermediate.csv"
iptm_csv_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/results/StoPred_result_analysis/result_df_filterd_by_iptm_athan_mixed_homodimer_900_v1.csv"
iptm_csv_intermediate_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/results/StoPred_result_analysis/result_df_filterd_by_iptm_athan_mixed_homodimer_900_intermediate_v1.csv"






unsorted_paths = glob(input_path)
paths=sorted(unsorted_paths)
paths = paths[:-1]
print(f"Length of possible protein combinations: {len(paths)}")

# fetch iptm (max and average amonge 5 sample)
result_dict={}
result_dict["uid"]=[]
result_dict["name"]=[]
result_dict["count"]=[]
# result_dict["pro_stoi"]=[]
result_dict["max_iptm"]=[]
result_dict["avg_iptm"]=[]
result_dict["pred_stoi"]=[]
result_dict["subunit_count"]=[]
count = 0
for p in paths:
    # if count <= 50:
    uid = p.split("/")[-1]
    split_name = uid.split("_")
    name=split_name[0]
    # name = "_".join(split_name[:2])
    # print(split_name)
    if len(split_name) == 2:
        pred_stoi = f"A{split_name[1]}"
        subunit_count=1
    elif len(split_name[2:]) == 1:
        pred_stoi = f"A{split_name[2]}"
        subunit_count=1
    elif len(split_name[2:]) == 2:
        pred_stoi = f"A{split_name[2]}B{split_name[3]}"
        subunit_count=2
    protein_number=int(split_name[-1])
    # pro_stoi=f"A{protein_number}"
    prediction_path = f"{p}/seed_101/predictions/*.json"
    sample_paths = glob(prediction_path)
    iptms=[]
    for sp in sample_paths:
        with open(sp, "r") as file:
            metric_dict = json.load(file)
            iptm = metric_dict["iptm"]
            iptms+=[iptm]
    avg_iptm = np.mean(iptms)
    max_iptm = max(iptms)
    result_dict["uid"]+=[uid]
    result_dict["name"]+=[name]
    result_dict["count"]+=[protein_number]
    # result_dict["pro_stoi"]+=[pro_stoi]
    result_dict["max_iptm"]+=[max_iptm]
    result_dict["avg_iptm"]+=[avg_iptm]
    result_dict["pred_stoi"]+=[pred_stoi]
    result_dict["subunit_count"]+=[subunit_count]
        # count+=1
result_df = pd.DataFrame.from_dict(result_dict)

protein_counts = result_df["name"].nunique()
print(f"Initial number of proteins: {protein_counts}")

# remove low confidence results
result_df["group_max_iptm"]=result_df.groupby("name")["max_iptm"].transform("max")
result_df = result_df[result_df["group_max_iptm"]>=0.5]
print(f"Number of possible complex after remove top1 iptm <=0.5: {len(result_df)}")
protein_counts_2 = result_df["name"].nunique()
print(f"Number of proteins after remove top1 iptm <=0.5: {protein_counts_2}")

result_df.to_csv(iptm_csv_intermediate_path, index=False)

# add correct stoi
# with open("/lustre/grp/gyqlab/wangpx/data/StoPred_data/StoPred_raw_data/train_data.pkl", "rb") as f:
#         input_dict=pickle.load(f)
entity_df = pd.read_csv(entity_df_path)
entity_df = entity_df.rename(columns={'protein_id':'name'})
entity_df_lst = entity_df["name"].tolist()
entity_df = entity_df.set_index(["name"])
### WARNING: find a way to annotate stoichiometry in uniprot

entity_df["stoichiometry"] = "A2"

# result_df = result_df[result_df["name"].isin(entity_df_lst)]
print(len(result_df))
print(result_df["name"].nunique())

correct_counts=[]
stoichiometries=[]
amino_acid_lengths=[]
for index, row in result_df.iterrows():
    ### Append amino acid length and filter out those larger than 1000
    name = row["name"]
    correct_row = entity_df.loc[name]
    correct_stoi = correct_row["stoichiometry"]
    amino_acid_length = correct_row["Length"]
    # amino_acid_length = correct_row["amino acid length"]
    stoichiometries+=[correct_stoi]
    amino_acid_lengths+=[amino_acid_length]
    correct_count= int(correct_stoi[1:])
    correct_counts+=[correct_count]

result_df["correct_count"]=correct_counts
result_df["stoichiometry"]=stoichiometries
result_df["amino acid length"]=amino_acid_lengths

# remove those doesn't have correct answer in the existing combination
# result_df["max_count"]=result_df.groupby("name")["count"].transform("max")
# result_df=result_df[result_df["max_count"]>=result_df["correct_count"]]
result_df = result_df[result_df["amino acid length"]<=AMINO_ACID_LEN_LIMIT]
print(f"Number of possible complex after remove those without correct answer: {len(result_df)}")
protein_counts_3 = result_df["name"].nunique()
print(f"Number of proteins after remove those without correct answer: {protein_counts_3}")

print(result_df)

result_df.to_csv(iptm_csv_path, index=False)

