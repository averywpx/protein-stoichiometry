import re
import pandas as pd

log_file = "/storage/gaoyiqinLab/wangpeixin/data/data_1/test_msa/msa_search_output_360.txt"

task_pat = re.compile(r"task\s+(\d+):\s+(\S+)")
elapsed_pat = re.compile(r"elapsed:\s+([0-9:]+)")

rows = []
current_task = None
last_elapsed = None


def elapsed_to_minutes(elapsed):
    parts = list(map(int, elapsed.split(":")))

    if len(parts) == 2:       # MM:SS
        m, s = parts
        return m + s / 60

    if len(parts) == 3:       # HH:MM:SS
        h, m, s = parts
        return h * 60 + m + s / 60


with open(log_file, "r", errors="ignore") as f:
    for line in f:
        task_match = task_pat.search(line)

        # When a new task starts, save the previous task
        if task_match:
            if current_task is not None and last_elapsed is not None:
                current_task["elapsed"] = last_elapsed
                current_task["elapsed_minutes"] = elapsed_to_minutes(last_elapsed)
                rows.append(current_task)

            current_task = {
                "task_index": int(task_match.group(1)),
                "transcript_id": task_match.group(2),
            }
            last_elapsed = None

        # Always update elapsed; the last one before next task is kept
        elapsed_matches = elapsed_pat.findall(line)
        if elapsed_matches and current_task is not None:
            last_elapsed = elapsed_matches[-1]

# Save the final task
if current_task is not None and last_elapsed is not None:
    current_task["elapsed"] = last_elapsed
    current_task["elapsed_minutes"] = elapsed_to_minutes(last_elapsed)
    rows.append(current_task)

df = pd.DataFrame(rows)
df["elapsed_minutes"] = df["elapsed_minutes"].round(2)
df.to_csv("/storage/gaoyiqinLab/wangpeixin/data/data_1/test_msa/msa_search_time_summary.csv", index=False)

lst_1 = df[df["elapsed_minutes"]<= 1]["transcript_id"].tolist()
lst_5 = df[(df["elapsed_minutes"]> 1) & (df["elapsed_minutes"]<= 5)]["transcript_id"].tolist()
lst_10 = df[(df["elapsed_minutes"]> 5) & (df["elapsed_minutes"]<= 10)]["transcript_id"].tolist()
lst_30 = df[(df["elapsed_minutes"]> 10) & (df["elapsed_minutes"]<= 30)]["transcript_id"].tolist()

print(f"Proteins that takes less than 1 min: {lst_1}\n")
print(f"Proteins that takes more than 1 min and less than 5 min: {lst_5}\n")
print(f"Proteins that takes more than 5 min and less than 10 min: {lst_10}\n")
print(f"Proteins that takes more than 10 min and less than30 min: {lst_30}\n")


