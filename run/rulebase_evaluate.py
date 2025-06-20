"""
    poetry run python -m run.rulebase_evaluate --rulebase_func_name count_text_length
"""

import argparse
import mlflow
import pandas as pd


from src.evaluate_common import evaluate_submit_df
from src.judge.rulebase_judge import RulebaseJudge


def main():
    parser = argparse.ArgumentParser(description="evaluate時の引数")
    parser.add_argument('--rulebase_func_name', type=str, required=True, help="名前を指定")
    parser.add_argument('--submit_file_name', type=str, required=True, help="名前を指定")
    

    args = parser.parse_args()

    submit = pd.read_csv("./data/submit/submit.csv") # todo: config指定できるように
    judge  = RulebaseJudge(args.rulebase_func_name) 

    mlflow.log_param("rulebase_func_name", judge.rulebase_func_name)
    mlflow.log_param("submit_file_name", "./data/submit/submit.csv")
    mlflow.log_param("submit_data_version", "hoge")

    result = evaluate_submit_df(submit_df = submit, judge = judge)
    
    mlflow.log_metric("score", result["score"].mean())
    result.to_json(f"./data/result/rulebase_{args.submit_file_name}_{args.rulebase_func_name}.json", orient="records", lines=True, force_ascii=False)

if __name__ == '__main__':
    main()