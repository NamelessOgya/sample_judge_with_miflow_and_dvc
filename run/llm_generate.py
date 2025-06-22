"""
    poetry run python -m run.llm_generate --generate_target_name data --prompt_name set_idol_discription
"""

import yaml
import argparse
import mlflow
import pandas as pd

from src.common.llm_invoker import LLMInvoker
from src.generate.generate_test_df import generate_test_df
from src.utils.dvc_util import get_current_run_id
from src.utils.hash_util import get_file_hash


def main():
    parser = argparse.ArgumentParser(description="generate時の引数")
    parser.add_argument('--generate_target_name', type=str, required=True, help="名前を指定")
    parser.add_argument('--prompt_name', type=str, required=True, help="名前を指定")

    args = parser.parse_args()

    generate_target = pd.read_csv(f"./data/generate_target/{args.generate_target_name}.csv")  
    

    # inference時はconfigを直接読み込む
    # llm componentに渡す情報を可変にするため
    with open("params.yaml", "r") as f:
        param = yaml.safe_load(f)

    invoker = LLMInvoker(
        model_config = param["generate"]["model_config"],  # 実際のモデル設定を指定する
        prompt_path = f"./src/generate/prompt/{args.prompt_name}.txt"
    )

    result = generate_test_df(
        generate_target = generate_target, 
        invoker = invoker
    )

    mlflow.set_experiment("text_generation")

    mlflow.log_param("mikoto_run_id", get_current_run_id())
    
    mlflow.log_param("prompt_name", args.prompt_name)
    mlflow.log_param("generate_prompt_base", invoker.prompt_base)
    mlflow.log_param("generate_prompt_version", get_file_hash(f"./src/generate/prompt/{args.prompt_name}.txt"))

    for key, value in param["generate"]["model_config"].items():
        mlflow.log_param(f"model_config_{key}", value)

    
    result.to_csv(f"./data/submit/{args.generate_target_name}_{args.prompt_name}.csv", index = False)

    



if __name__ == '__main__':
    main()