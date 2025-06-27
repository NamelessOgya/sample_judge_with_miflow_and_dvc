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

    submit = pd.read_csv(f"./data/submit/{args.submit_file_name}.csv")  # todo: config指定できるように  

    # pairwise evaluateのために、pair側の出力をカラムに追加する。  
    if 'pair_csv_name' == "None":
        pair_df = pd.read_csv(f"./data/submit/{judge_menu['pair_csv_name']}.csv")
        join_keys = [col for col in pair_df.columns if col != "text"]
        pair_df = pair_df.rename(columns = {"text": "pair_text"})

        submit = pd.merge(submit, pair_df, on = join_keys, how = "left")
        submit["pair_submit_name"] = judge_menu['pair_csv_name']

        if submit["pair_text"].isna().sum() > 0:
            raise Exception("submitファイルにpairwiseファイルのjoinを試みましたが、紐づかないレコードがありました。")
    
    
    if "filter" in judge_menu.keys():
        for condition in judge_menu["filter"]:
            
            submit = submit[submit[condition["filter_col_name"]].astype(str) == str(condition["filter_value"])].copy()
    else:
        judge_menu["filter"] = {}

    if "prompt_insert" not in judge_menu.keys():
        judge_menu["prompt_insert"] = {}

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

    result.to_json(f"./data/result/llm_{args.submit_file_name}_{args.judge_name}_{judge_menu['pair_csv_name']}.json", orient="records", lines=True, force_ascii=False)
    
    mlflow.set_experiment("evaluate")
    
    mlflow.log_param("mikoto_run_id", get_current_run_id())
    mlflow.log_param("category", "llm")
    
    if 'pair_csv_name' == "None":
        mlflow.log_param("judge_name", args.judge_name + "_vs_" + judge_menu['pair_csv_name'])
    else:
        mlflow.log_param("judge_name", args.judge_name)

    mlflow.log_param("prompt_name", judge_menu["prompt_name"])

    mlflow.log_param("judge_prompt_base", judge.prompt_base)
    mlflow.log_param("judge_prompt_version", get_file_hash(f"./src/judge/prompt/{judge_menu['prompt_name']}.txt"))

    mlflow.log_param("submit_file_name", args.submit_file_name)
    mlflow.log_param("submit_file_version", get_file_hash(f"./data/submit/{args.submit_file_name}.csv"))


    mlflow.log_metric("score", result["score"].mean())

    # model configの記録
    for key, value in judge_config["model_config"].items():
        mlflow.log_param(f"model_config_{key}", value)

    # filter / additional_fillingの記録  
    mlflow.log_param("filter", json.dumps(judge_menu["filter"], ensure_ascii=False))
    mlflow.log_param("prompt_insert", json.dumps(judge_menu['prompt_insert'], ensure_ascii=False) )
    mlflow.log_param("len_submit", len(submit))

if __name__ == '__main__':
    main()