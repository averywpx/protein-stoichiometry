#!/bin/bash

JOB_ID=$1

echo "#!/bin/bash" > /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
echo "#SBATCH -o job.protenix.$JOB_ID.out" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
echo "#SBATCH -e job.protenix.$JOB_ID.err" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
echo "#SBATCH --gres=gpu:1" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
echo "#SBATCH -p gpu31" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
echo "#SBATCH --qos=normal" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
echo "#SBATCH -J $JOB_ID.protenix" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
echo "#SBATCH --nodes=1" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh


## train data
# echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_homomeric_complex_json/protenix_homomeric_complex_$JOB_ID.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_$JOB_ID.sh

# valid data
# echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/valid_dataset_protenix_homomeric_complex.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output_valid_data --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_$JOB_ID.sh

# # valid data AAB
# echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/valid_dataset_protenix_AAB_complex.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output_valid_AAB --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh

# train data AAB
echo "~/anaconda3/envs/protenix2/bin/protenix predict --input /lustre/grp/gyqlab/wangpx/data/StoPred_data/protenix_training_AAB_json/protenix_training_AAB_$JOB_ID.json --out_dir /lustre/grp/gyqlab/wangpx/protenix2/base_1_output_training_AAB_2 --seeds 101 --model_name "protenix_base_default_v0.5.0"" >> /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh

#submit the job
sbatch /lustre/grp/gyqlab/wangpx/protenix2/script/protenix_job_AAB_$JOB_ID.sh
