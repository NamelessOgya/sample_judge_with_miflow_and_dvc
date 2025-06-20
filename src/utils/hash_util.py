"""
    poetry run python -m src.utils.hash_util
"""

import hashlib

# ファイルを文字列として読み込み

def get_file_hash(filename: str) -> str:
    """
        ファイルを丸ごと文字列として読み込んでハッシュを得る。
        奇跡的に衝突しない限りは、同じファイルは同じハッシュ値になるので、
        バージョン管理のような用途に使える。
        :param filename: ハッシュを取得したいファイルのパス
        :return: ハッシュ値（SHA-256）
    """
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # ハッシュ化（SHA-256）
    hash_value = hashlib.sha256(content.encode("utf-8")).hexdigest()

    return hash_value

if __name__ == "__main__":
    print(get_file_hash("./src/judge/prompt/check_if_category_in_text.txt"))