
class DummyLLM:
    """
    言語モデルを模倣したダミーのクラス

    入力に対してルールベースで応答を返す。
    """

    def __init__(self, config_dict: dict):
        self.config_dict = config_dict
        """
            self.config_dictをinputとしてllmインスタンスの初期化が
            ここに入る
        """

    def generate(self, prompt: str) -> str:
        """
        プロンプトに対してルールベースで応答を生成する。
        実際にはこの部分がllmへの問い合わせ・応答になる。
        """

        # submitデータ生成の際のルールベース
        if "アイドルの説明を生成してください。" in prompt:
            if "ひめっち" in prompt:
                base = "蓮ノ空女学院の2年生。生粋のゲーマーで、ゲームと「みらくらぱーく！」が大好き。対よろ！の精神で誰とでもぶつかり合い、仲良くなろうとする。いつもはゆるっとしているが、ひとたびスイッチが入ると周りが見えなくなってしまうことも。"
            elif "るりちゃん先輩" in prompt:
                base = "蓮ノ空女学院の3年生。1年生の時に留学先のカリフォルニアから編入した帰国子女。周囲を明るくする元気な性格だが、気を遣いすぎるがゆえ、体力を使い切ると充電切れの状態になってしまうことも。ソロ活動が大好きで、釣りやキャンプもひとりで遊びに行く。"
            elif "めぐちゃん先輩" in prompt:
                base = "蓮ノ空女学院の102期生。小さい頃からタレント活動をしており、自分の可愛さを自覚している。世界中を夢中にするため、いつだって努力を惜しまない。一方で興味のないことは一切やらないため、勉強は壊滅的。高校卒業後、夢を叶えるため世界に向かって羽ばたいた。"
            else:
                raise NotImplementedError("Unknown prompt for DummyLLM")
            
            # pronptによる出力変化を出すために、キーワードを加える。
            return base + prompt.split("キーワード:")[1]
        
        # judgeのルールベース応答
        elif "以下の文字列が対象テキストに含まれるか判定してください: " in prompt:
            # dummy出力を作成
            key_word = prompt.split("以下の文字列が対象テキストに含まれるか判定してください: ")[1].split("\n")[0]
            target = prompt.split("【対象テキスト】")[1]
            llm_output_str = f"""
            score: {1.0 if key_word in target else 0.0}  
            reason: not implemented yet    
            """
        
            return llm_output_str

        elif "【対象テキスト】,【比較対象テキスト】内のキーワード数をカウントし、" in prompt:
            keyword = prompt.split("キーワード: ")[1].split("\n")[0]

            submit = prompt.split("【対象テキスト】")[2].split("【比較対象】")[0]
            pair = prompt.split("【比較対象】")[1]

            print("== submit ==")
            print(submit)

            print("== pair ==")
            print(pair)

            submit_keyword_len = len(submit.split(keyword))
            pair_keyword_len = len(pair.split(keyword))

            if submit_keyword_len > pair_keyword_len:
                score = 1.0
            else:
                score = 0.0
            
            return f"""
            score: {score}  
            reason: not implemented yet    
            """


        else:
            raise NotImplementedError("Unknown prompt for DummyLLM")