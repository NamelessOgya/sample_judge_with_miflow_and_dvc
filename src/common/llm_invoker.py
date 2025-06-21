
import pandas as pd
import yaml

from src.common.dummy_llm import DummyLLM

class LLMInvoker:
    """
    Base class for LLM invokers.
    This class should be extended by specific LLM invoker implementations.
    """

    def __init__(self, model_config, prompt_path: str):
        # 必要項目(f-stringを含む文字列)
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_base = f.read()
        
        self.model_config = model_config

        self.llm = DummyLLM(model_config)
    
    def prompt_filling(self, prompt_filling_dict: dict) -> str:
        """
            プロンプトの穴埋め部分に辞書の内容を適用

            prompt_filling_dict: 
                promptにinsertする情報をkey_value形式で格納した辞書。
                judgeされるべきテキストが"text"keyに格納されている必要がある。
                ほかのkey_valueは任意であり、プロンプトの内容に応じて変化する。
            例: {"idol_name": "るり", "gakunen": "2年生", "text": "対象テキストの内容"}
        """
        
        return self.prompt_base.format(**prompt_filling_dict)
    
    def invoke(self, prompt: str) -> str:
        """
            llmにプロンプトを渡して評価をtext形式で受け取る。

            prompt: llmにinsertするpromptの文字列
        """

        # llmが出力をはyaml形式で返すことを想定
        return self.llm.generate(prompt)
    
    def parse_llm_output(self, llm_output_str: str) -> dict:
        """
            LLMの出力(string)を辞書形式に変換する。

            llm_output_str: LLMが返した文字列形式の出力。yaml形式の出力を文字列化したものを想定。
        """
        
        return yaml.safe_load(llm_output_str)

    def judge_row(self, prompt_filling_dict: dict) -> dict:
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

        result = self.generate_row(prompt_filling_dict)

        result = self.parse_llm_output(result)
        
        return result # {}"score":float, "reason": str}

    def generate_row(self, prompt_filling_dict: dict) -> str:
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

        result = self.invoke(
            self.prompt_filling(prompt_filling_dict)
        )
        
        return result # {}"score":float, "reason": str}
