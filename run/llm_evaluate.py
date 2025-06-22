"""
    poetry run python -m run.llm_evaluate --prompt_name check_if_category_in_text
"""

import argparse
import mlflow
import pandas as pd
import yaml
import json

from src.judge.judge_submit_df import evaluate_submit_df
from src.common.llm_invoker import LLMInvoker
from src.utils.dvc_util import get_current_run_id
from src.utils.hash_util import get_file_hash



def main():
    parser = argparse.ArgumentParser(description="evaluate時の引数")
    parser.add_argument('--judge_name', type=str, required=True, help="名前を指定")
    parser.add_argument('--submit_file_name', type=str, required=True, help="名前を指定")
    args = parser.parse_args()

    with open("params.yaml", "r") as f:
        judge_config = yaml.safe_load(f)["judge"]


    judge_menu = None
    for m in judge_config["judge_menus"]:
        if args.judge_name == m["name"]:
            judge_menu = m

    if judge_menu is None:
        raise NotImplemented

    print(judge_menu)

    # nameがかぶっていないか確認する
    

    submit = pd.read_csv(f"./data/submit/{args.submit_file_name}.csv")  # todo: config指定できるように  
    
    
    if "filter" not in judge_menu.keys():
        for condition in judge_menu["filter"]:
            submit = submit[submit[condition["filter_col_name"]].astype(str) == condition["filter_value"].astype(str)].copy()

    judge  = LLMInvoker(
        model_config = judge_config["model_config"],
        prompt_path = f"./src/judge/prompt/{judge_menu['prompt_name']}.txt"
    ) 

    result = evaluate_submit_df(
        submit_df = submit, 
        judge = judge, 
        additional_filling_dict = judge_menu['prompt_insert']
    )

    result["filter"] = json.dumps(judge_menu["filter"], ensure_ascii=False) 
    result["prompt_insert"] = json.dumps(judge_menu['prompt_insert'], ensure_ascii=False) 

    result.to_json(f"./data/result/llm_{args.submit_file_name}_{args.name}.json", orient="records", lines=True, force_ascii=False)

    
    mlflow.set_experiment("evaluate")
    
    mlflow.log_param("mikoto_run_id", get_current_run_id())
    mlflow.log_param("category", "llm")

    
    mlflow.log_param("judge_name", args.judge_name)
    mlflow.log_param("prompt_name", judge_menu["prompt"])

    mlflow.log_param("judge_prompt_base", judge.prompt_base)
    mlflow.log_param("judge_prompt_version", get_file_hash(f"./src/judge/prompt/{args.prompt_name}.txt"))

    mlflow.log_param("submit_file_name", args.submit_file_name)
    mlflow.log_param("submit_file_version", get_file_hash(f"./data/submit/{args.submit_file_name}.csv"))


    mlflow.log_metric("score", result["score"].mean())

    # model configの記録
    for key, value in judge_config["model_config"].items():
        mlflow.log_param(f"model_config_{key}", value)

    # filter / additional_fillingの記録  
    mlflow.log_param("filter", json.dumps(judge_menu["filter"], ensure_ascii=False) )
    mlflow.log_param("prompt_insert", json.dumps(judge_menu['prompt_insert'], ensure_ascii=False) )
    mlflow.log_param("len_submit", len(submit))

if __name__ == '__main__':
    main()