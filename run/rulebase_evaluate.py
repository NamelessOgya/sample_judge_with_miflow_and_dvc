"""
    poetry run python -m run.rulebase_evaluate --rulebase_func_name count_text_length
"""

import argparse
import mlflow
import pandas as pd


from src.judge.judge_submit_df import evaluate_submit_df
from src.judge.rulebase_judge import RulebaseJudge
from src.utils.dvc_util import get_current_run_id
from src.utils.hash_util import get_file_hash


def main():
    parser = argparse.ArgumentParser(description="evaluate時の引数")
    parser.add_argument('--rulebase_func_name', type=str, required=True, help="名前を指定")
    parser.add_argument('--submit_file_name', type=str, required=True, help="名前を指定")
    

    args = parser.parse_args()

    submit = pd.read_csv("./data/submit/submit.csv") # todo: config指定できるように
    judge  = RulebaseJudge(args.rulebase_func_name) 

    

    result = evaluate_submit_df(submit_df = submit, judge = judge)
    
    result.to_json(f"./data/result/rulebase_{args.submit_file_name}_{args.rulebase_func_name}.json", orient="records", lines=True, force_ascii=False)

    mlflow.log_param("mikoto_run_id", get_current_run_id())
    mlflow.log_param("category", "rulebase")
    mlflow.log_param("rulebase_func_name", judge.rulebase_func_name)
    mlflow.log_param("rulebase_func_version", get_file_hash(f"./src/judge/rulebase_funcs/{args.rulebase_func_name}.py"))


    mlflow.log_param("submit_file_name", args.submit_file_name)
    mlflow.log_param("submit_file_version", get_file_hash(f"./data/submit/{args.submit_file_name}.csv"))

    
    mlflow.log_metric("score", result["score"].mean())

if __name__ == '__main__':
    main()