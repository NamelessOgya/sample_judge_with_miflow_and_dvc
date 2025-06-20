
"""
    rulebase judgeで使用する関数群をここに書いていく。 
    IFはかならず以下の値とする。 

    input: 
        string: str llmの出力

    config_dict: 
        config_dict: dict 検証用csv一行を辞書化したもの。
"""

def check_megu_in_text(
    row_dict: dict
):
    return {"score": 1.0 if "めぐ" in row_dict["text"] else 0.0}