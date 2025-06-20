"""
    poetry run python -m src.judge.llm_judge
"""

"""
    プロンプトを読み込み、内容を評価するクラス。
"""

import pandas as pd
import yaml

class LLMJudge:
    def __init__(self, prompt_path: str):
        # 必要項目(f-stringを含む文字列)
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.judge_prompt_base = f.read()
    
    def prompt_filling(self, prompt_filling_dict: dict) -> str:
        """
            プロンプトの穴埋め部分に辞書の内容を適用

            prompt_filling_dict: 
                promptにinsertする情報をkey_value形式で格納した辞書。
                judgeされるべきテキストが"text"keyに格納されている必要がある。
                ほかのkey_valueは任意であり、プロンプトの内容に応じて変化する。
            例: {"idol_name": "るり", "gakunen": "2年生", "text": "対象テキストの内容"}
        """
        
        return self.judge_prompt_base.format(**prompt_filling_dict)
    
    def llm_inference(self, prompt: str) -> str:
        """
            llmにプロンプトを渡して評価をtext形式で受け取る。
            本当はこの部分にLLMに問い合わせを行い評価を得る部分が入るが、
            検証のために手作業でyamlを作る。

            prompt: llmにinsertするpromptの文字列
        """

        # dummy出力を作成
        key_word = prompt.split("以下の文字列が対象テキストに含まれるか判定してください: ")[1].split("\n")[0]
        target = prompt.split("【対象テキスト】")[1]
        llm_output_str = f"""
        score: {1.0 if key_word in target else 0.0}  
        reason: not implemented yet    
        """


        # llmが出力をはyaml形式で返すことを想定
        return llm_output_str
    
    def parse_llm_output(self, llm_output_str: str) -> dict:
        """
            LLMの出力(string)を辞書形式に変換する。

            llm_output_str: LLMが返した文字列形式の出力。yaml形式の出力を文字列化したものを想定。
        """
        
        return yaml.safe_load(llm_output_str)

    def judge(self, prompt_filling_dict: dict) -> dict:
        """
            llmにプロンプトを渡して評価を得る。
            テキスト形式で受け取った評価を辞書形式にパースして返す。

            評価値がkey "score"に格納されている必要があるが、
            そのほかのkey_valueは任意である。

            すべてのkey_valueがresultのjsonファイルに保存される。

            prompt_filling_dict: 
                promptにinsertする情報をkey_value形式で格納した辞書。
                judgeされるべきテキストが"text"keyに格納されている必要がある。
                ほかのkey_valueは任意であり、プロンプトの内容に応じて変化する。
            例: {"idol_name": "るり", "gakunen": "2年生", "text": "対象テキストの内容"}
        """

        result = self.llm_inference(
            self.prompt_filling(prompt_filling_dict)
        )

        result = self.parse_llm_output(result)
        
        return result # {}"score":float, "reason": str}


if __name__ == '__main__':
    prompt_path = "./src/judge/prompt/check_if_category_in_text.txt"
    j = LLMJudge(prompt_path)

    sample_input = {}
    sample_input["idol_name"] = "ひめっち"
    sample_input["gakunen"] = "2年生"
    sample_input["text"] = """
    蓮ノ空女学院の2年生。生粋のゲーマーで、ゲームと「みらくらぱーく！」が大好き。“対よろ！”の精神で誰とでもぶつかり合い、仲良くなろうとする。いつもはゆるっとしているが、ひとたびスイッチが入ると周りが見えなくなってしまうことも。
    """

    print(f"test1...score: {j.judge(sample_input)}")
    
    sample_input["text"] += "\nるりちゃんはとてもかわいいです。"

    print(f"test2...score: {j.judge(sample_input)}")