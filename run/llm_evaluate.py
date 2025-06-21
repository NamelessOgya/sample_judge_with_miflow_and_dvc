"""
    poetry run python -m run.llm_evaluate --prompt_name check_if_category_in_text
"""

import argparse
import mlflow
import pandas as pd
import hashlib

from src.judge.judge_common import evaluate_submit_df
from src.judge.llm_judge import LLMJudge
from src.utils.dvc_util import get_current_run_id
from src.utils.hash_util import get_file_hash



def main():
    parser = argparse.ArgumentParser(description="evaluate時の引数")
    parser.add_argument('--prompt_name', type=str, required=True, help="名前を指定")
    parser.add_argument('--submit_file_name', type=str, required=True, help="名前を指定")

    args = parser.parse_args()

    submit = pd.read_csv("./data/submit/{submit_file_name}.csv")  # todo: config指定できるように    
    judge  = LLMJudge(prompt_path = f"./src/judge/prompt/{args.prompt_name}.txt") 

    result = evaluate_submit_df(submit_df = submit, judge = judge)

    result.to_json(f"./data/result/llm_{args.submit_file_name}_{args.prompt_name}.json", orient="records", lines=True, force_ascii=False)

    
    mlflow.set_experiment("text_generation")
    
    mlflow.log_param("mikoto_run_id", get_current_run_id())
    mlflow.log_param("category", "llm")

    mlflow.log_param("prompt_name", args.prompt_name)

    mlflow.log_param("judge_prompt_base", judge.prompt_base)
    mlflow.log_param("judge_prompt_version", get_file_hash(f"./src/judge/prompt/{args.prompt_name}.txt"))

    mlflow.log_param("submit_file_name", args.submit_file_name)
    mlflow.log_param("submit_file_version", get_file_hash(f"./data/submit/{args.submit_file_name}.csv"))

    mlflow.log_metric("score", result["score"].mean())

if __name__ == '__main__':
    main()