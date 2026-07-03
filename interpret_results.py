import numpy as np
import pandas as pd


# training A
input_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_training_A.csv"
# training AAB
# input_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_training_AAB.csv"

# # valid A
# input_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_valid_A_2.csv"
# # valid AAB
# input_path = "/lustre/grp/gyqlab/wangpx/protenix2/StoPred_result_analysis/result_df_filterd_by_iptm_valid_AAB.csv"

ref_path = "/lustre/grp/gyqlab/wangpx/data/StoPred_data/train_data_entity_count_tax_df_after_20210930.csv"


dataset_type = "Training Dataset"
# dataset_type = "Validation Dataset"

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


ref_df = pd.read_csv(ref_path)
after_20210930_date_lst = ref_df["name"].tolist()


result_df = pd.read_csv(input_path)
result_df["possible_combination_counts"]=result_df.groupby("name")["name"].transform("count")
# result_df["pred_stoi"] = "A"+ result_df["count"].astype(str)
# result_df["stoichiometry"] = "A"+ result_df["correct_count"].astype(str)


# result_df = result_df[result_df["name"].isin(after_20210930_date_lst)]

print(f"{dataset_type}")

# calculate success rate based on number of A chains in homo-oligomer
for i in range(2,51):
    df = result_df[result_df["correct_count"]==i]
    success_rate = calc_top1_success_rate(df)
    print(f"For protein with {i} possible combinations, the success rate is: {success_rate}")

# # calc top1 sucess rate based on max_iptm
# max_top1_success_rate = calc_top123_success_rate(result_df, 1, "max")
# print(f"Top 1 max_iptm success rate: {max_top1_success_rate}")

# # # get top1 iptm success rate based on max_iptm
# # top1_max_iptm_success_rate = calc_top1_success_rate(result_df)
# # print(f"AAB: Top 1 max_iptm success rate: {top1_max_iptm_success_rate}")

# # get top1 iptm success rate based on avg_iptm
# top1_avg_iptm_success_rate = calc_top123_success_rate(result_df, 1, "avg")
# print(f"AAB: Top 1 avg_iptm success rate: {top1_avg_iptm_success_rate}")

# # use possible_combination_counts filtered out those with possible complex less than 2
# more_complex_df = result_df[result_df["possible_combination_counts"]>2]
# max_top1_success_rate_2 = calc_top123_success_rate(more_complex_df, 1, "max")
# print(f"AAB: Top 1 max_iptm success rate (>2 possible complex): {max_top1_success_rate_2}")

# # random_1000_df = result_df.sample(n=1000)
# # max_top1_success_rate_3 = calc_top1_success_rate(random_1000_df)
# # print(f"AAB: Top 1 max_iptm success rate (1000 randomly selected samples): {max_top1_success_rate_3}")

# # # sample 1000 from top1_max_iptm_df
# # random_50_df = result_df.sample(frac=0.5)
# # # random_1000_df = result_df.sample(n=1000)
# # max_top1_success_rate_4 = calc_top1_success_rate(random_50_df)
# # print(f"AAB: Top 1 max_iptm success rate (randomly selecte 50% of the samples): {max_top1_success_rate_4}")

# # random_10_df = result_df.sample(frac=0.1)
# # max_top1_success_rate_4 = calc_top1_success_rate(random_10_df)
# # print(f"AAB: Top 1 max_iptm success rate (randomly selecte 10% of samples): {max_top1_success_rate_4}")

# # get top2 iptm success rate based on max_iptm
# top2_max_iptm_success_rate = calc_top123_success_rate(result_df, 2, "max")
# print(f"AAB: Top 2 max_iptm success rate: {top2_max_iptm_success_rate}")

# # get top2 iptm success rate based on avg_iptm
# top2_avg_iptm_success_rate = calc_top123_success_rate(result_df, 2, "avg")
# print(f"AAB: Top 2 avg_iptm success rate: {top2_avg_iptm_success_rate}")

# # get top3 iptm success rate based on max_iptm
# top3_max_iptm_success_rate = calc_top123_success_rate(result_df, 3, "max")
# print(f"AAB: Top 3 max_iptm success rate: {top3_max_iptm_success_rate}")

# # get top3 iptm success rate based on avg_iptm
# top3_avg_iptm_success_rate = calc_top123_success_rate(result_df, 3, "avg")
# print(f"AAB: Top 3 avg_iptm success rate: {top3_avg_iptm_success_rate}")



# # analyze results of proteins with only two subunits
# result_AB_df = result_df[result_df["subunit_count"]==2]
# print(f"Length of possible combination of proteins with 2 subunits: {len(result_AB_df)}")
# AB_set = set(result_AB_df["name"].tolist())
# print(f"Number of protein with AB structure: {len(AB_set)}")

# # # get top1 iptm success rate based on max_iptm
# # top1_max_iptm_success_rate = calc_top1_success_rate(result_AB_df)
# # print(f"AB: Top 1 max_iptm success rate: {top1_max_iptm_success_rate}")
# # calc top1 sucess rate based on max_iptm
# max_top1_success_rate = calc_top123_success_rate(result_AB_df, 1, "max")
# print(f"AB: Top 1 max_iptm success rate: {max_top1_success_rate}")

# # calc top1 sucess rate based on max_iptm
# max_top1_success_rate = calc_top123_success_rate(result_AB_df, 1, "avg")
# print(f"AB: Top 1 max_iptm success rate: {max_top1_success_rate}")

# # # get top1 iptm success rate based on avg_iptm
# # top1_avg_iptm_success_rate = calc_top1_success_rate(result_AB_df)
# # print(f"AB: Top 1 avg_iptm success rate: {top1_avg_iptm_success_rate}")

# # use possible_combination_counts filtered out those with possible complex less than 2
# more_complex_df = result_AB_df[result_AB_df["possible_combination_counts"]>2]
# max_top1_success_rate_2 = calc_top123_success_rate(more_complex_df, 1, "max")
# print(f"AB: Top 1 max_iptm success rate (>2 possible complex): {max_top1_success_rate_2}")

# # random_1000_df = result_df.sample(n=1000)
# # max_top1_success_rate_3 = calc_top1_success_rate(random_1000_df)
# # print(f"AAB: Top 1 max_iptm success rate (1000 randomly selected samples): {max_top1_success_rate_3}")

# # # sample 1000 from top1_max_iptm_df
# # random_50_df = result_AB_df.sample(frac=0.5)
# # max_top1_success_rate_4 = calc_top1_success_rate(random_50_df)
# # print(f"AAB: Top 1 max_iptm success rate (randomly selecte 50% of the samples): {max_top1_success_rate_4}")

# # random_10_df = result_AB_df.sample(frac=0.1)
# # max_top1_success_rate_4 = calc_top1_success_rate(random_10_df)
# # print(f"AAB: Top 1 max_iptm success rate (randomly selecte 10% of samples): {max_top1_success_rate_4}")

# # get top2 iptm success rate based on max_iptm
# top2_max_iptm_success_rate = calc_top123_success_rate(result_AB_df, 2, "max")
# print(f"AB: Top 2 max_iptm success rate: {top2_max_iptm_success_rate}")

# # get top2 iptm success rate based on avg_iptm
# top2_avg_iptm_success_rate = calc_top123_success_rate(result_AB_df, 2, "avg")
# print(f"AB: Top 2 avg_iptm success rate: {top2_avg_iptm_success_rate}")

# # get top3 iptm success rate based on max_iptm
# top3_max_iptm_success_rate = calc_top123_success_rate(result_AB_df, 3, "max")
# print(f"AB: Top 3 max_iptm success rate: {top3_max_iptm_success_rate}")

# # get top3 iptm success rate based on avg_iptm
# top3_avg_iptm_success_rate = calc_top123_success_rate(result_AB_df, 3, "avg")
# print(f"AB: Top 3 avg_iptm success rate: {top3_avg_iptm_success_rate}")

