"""
    poetry run python -m src.sample_judge.llm_judge
"""


import pandas as pd

class LLMJudge:
    def __init__(self, prompt_path: str):
        # 必要項目(f-stringを含む文字列)
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.judge_prompt_base = f.read()
    
    def prompt_filling(self, prompt_filling_dict: dict) -> str:
        """
        プロンプトの穴埋め部分に辞書の内容を適用
        """
        
        return self.judge_prompt_base.format(**prompt_filling_dict)
    
    def llm_inference(self, prompt: str) -> float:
        """
        本当はこの部分にLLMに問い合わせを行い評価を得る部分が入るが、
        検証のために簡易的な実装を行う。
        """

        key_word = prompt.split("以下の文字列が対象テキストに含まれるか判定してください: ")[1].split("\n")[0]
        target = prompt.split("【対象テキスト】")[1]

        return {
            "score": 1.0 if key_word in target else 0.0 ,
            "reason": "not implemented yet"
        } # {"score":float, "reason": str}
    
    def judge(self, prompt_filling_dict: dict) -> dict:
        
        result = self.llm_inference(
            self.prompt_filling(prompt_filling_dict)
        )
        
        return result # {}"score":float, "reason": str}


if __name__ == '__main__':
    prompt_path = "./src/sample_judge/prompt/check_if_category_in_text.txt"
    j = LLMJudge(prompt_path)

    sample_input = {}
    sample_input["card_name"] = "ひめっち"
    sample_input["zokusei"] = "2年生"
    sample_input["text"] = """
    蓮ノ空女学院の2年生。生粋のゲーマーで、ゲームと「みらくらぱーく！」が大好き。“対よろ！”の精神で誰とでもぶつかり合い、仲良くなろうとする。いつもはゆるっとしているが、ひとたびスイッチが入ると周りが見えなくなってしまうことも。
    """

    print(f"test1...score: {j.judge(sample_input)}")
    
    sample_input["text"] += "海皇"

    print(f"test2...score: {j.judge(sample_input)}")