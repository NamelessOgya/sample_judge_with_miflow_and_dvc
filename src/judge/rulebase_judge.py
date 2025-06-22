"""
    poetry run python -m src.judge.rulebase_judge
"""

"""
    プロンプトを読み込み、内容を評価するクラス。
"""

import importlib

class RulebaseJudge:
    def __init__(self, rulebase_func_name: str):
        self.rulebase_func_name = rulebase_func_name
        module = importlib.import_module(f"src.judge.rulebase_funcs.{rulebase_func_name}")
        
        # 関数オブジェクトを取得して実行
        self.func = getattr(module, rulebase_func_name)
    
    def judge_row(self, row_dict: dict) -> dict:
        
        result = self.func(row_dict)
        
        return result 


if __name__ == '__main__':
    j = RulebaseJudge("count_text_length")

    sample_input = {}
    sample_input["card_name"] = "ひめっち"
    sample_input["zokusei"] = "2年生"
    sample_input["text"] = """
    蓮ノ空女学院の2年生。生粋のゲーマーで、ゲームと「みらくらぱーく！」が大好き。“対よろ！”の精神で誰とでもぶつかり合い、仲良くなろうとする。いつもはゆるっとしているが、ひとたびスイッチが入ると周りが見えなくなってしまうことも。
    """

    print(f"test1...score: {j.judge(sample_input)}")
    
    sample_input["text"] += "海皇"

    print(f"test2...score: {j.judge(sample_input)}")