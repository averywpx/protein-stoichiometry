import pandas as pd

input_file_path = "/storage/gaoyiqinLab/wangpeixin/data/data_1/intermediate_data/entity_df/train_data_entity_count_tax_df.csv"
iptm_file_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_training_A.csv"
# iptm_file_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_valid_A_2.csv"

ref_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/train_data_entity_count_tax_df_after_20210930.csv"

# find the top1 of max_iptm
def calc_top1_success_rate(df):
    top1_max_iptm_df = df[df["group_max_iptm"]==df["max_iptm"]]
    correct_prediction = len(top1_max_iptm_df[top1_max_iptm_df["count"]==top1_max_iptm_df["correct_count"]])
    # correct_prediction = len(top1_max_iptm_df[top1_max_iptm_df["pred_stoi"]==top1_max_iptm_df["stoichiometry"]])
    # print(correct_prediction)
    # print(len(top1_max_iptm_df))
    max_top1_success_rate = correct_prediction/len(top1_max_iptm_df)
    return max_top1_success_rate

def calc_top123_success_rate(df, order, metric=["max","avg"]):
    top23_df = df.groupby("name", group_keys=False).apply(pd.DataFrame.nlargest, n=order, columns=f"{metric}_iptm")
    top23_df = top23_df.reset_index().drop(["index", "uid","max_iptm","avg_iptm","group_max_iptm"], axis=1)
    top23_df = top23_df.groupby("name").agg({
        "pred_stoi": lambda x: x.tolist(),
        "stoichiometry": "first"
    })
    top23_df["Exist"] = [val in lst for val, lst in zip(top23_df["stoichiometry"], top23_df["pred_stoi"])]

    # print(len(top23_df[top23_df["Exist"]==True]))
    # print(len(top23_df))
    top3_success_rate = len(top23_df[top23_df["Exist"]==True])/len(top23_df)
    return top3_success_rate

df = pd.read_csv(input_file_path)


# count number of Arath appear
df["ARATH_counts"] = df["db_codes"].apply(lambda x: x.count("ARATH"))
arath_df = df[(df["ARATH_counts"]!=0)&(df["ARATH_counts"]==df["counts"])]

# ref_df = pd.read_csv(ref_path)
# after_20210930_date_lst = ref_df["name"].tolist()
# arath_df = arath_df[arath_df["name"].isin(after_20210930_date_lst)]


# # df["db_codes"] is a pure list
# arath_df = df[df["db_codes"].str.contains("ARATH")]

# # try human fist
# # Create a boolean mask indicating if the substring is in any item of the list
# arath_mask = df["joined_db_codes"].apply(lambda x: any("HUMAN" in s for s in x))

# # # Filter the DataFrame using the mask
# arath_df = df[arath_mask]

# print(df.dtypes)
# print(df[["name", "joined_db_codes"]])

# print(arath_df)
print(arath_df["counts"].value_counts())
print(arath_df["stoichiometry"].value_counts())
# print(arath_df[["name", "db_codes"]])

# idea 1: count numner of strings have substring
# idea 2: join strings in db_codes column and use str.contains

# retrieve name field in arath_df
arath_lst = arath_df["name"].tolist()

# read iptm file and see how many Arabidopsis protein left
iptm_A_df = pd.read_csv(iptm_file_path)

iptm_arath_df = iptm_A_df[iptm_A_df["name"].isin(arath_lst)]
print(f"Length of Arabidopsis df: {len(iptm_arath_df)}")

iptm_arath_df["pred_stoi"] = "A"+ iptm_arath_df["count"].astype(str)
iptm_arath_df["stoichiometry"] = "A"+ iptm_arath_df["correct_count"].astype(str)
iptm_arath_df["possible_combination_counts"]=iptm_arath_df.groupby("name")["name"].transform("count")

print(iptm_arath_df["stoichiometry"].value_counts())

# calculate success rate based on number of A chains in homo-oligomer
for i in range(2,51):
    df = iptm_arath_df[iptm_arath_df["correct_count"]==i]
    success_rate = calc_top1_success_rate(df)
    print(f"For protein with {i} possible combinations, the success rate is: {success_rate}")

# top1_max_iptm_success_rate = calc_top1_success_rate(iptm_arath_df)
# print(f"Arabidopsis: Top 1 max_iptm success rate: {top1_max_iptm_success_rate}")

# # get top2 iptm success rate based on max_iptm
# top2_max_iptm_success_rate = calc_top123_success_rate(iptm_arath_df, 2, "max")
# print(f"Arabidopsis: Top 2 max_iptm success rate: {top2_max_iptm_success_rate}")

# # get top3 iptm success rate based on max_iptm
# top3_max_iptm_success_rate = calc_top123_success_rate(iptm_arath_df, 3, "max")
# print(f"Arabidopsis: Top 3 max_iptm success rate: {top3_max_iptm_success_rate}")
