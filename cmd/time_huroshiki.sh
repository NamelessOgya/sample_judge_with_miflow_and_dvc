#!/bin/bash

# mikoto_run_id を自動生成
timestamp=$(date +%Y%m%d%H%M%S)
hash=$(echo -n "$timestamp" | sha1sum | cut -c1-12)
mikoto_run_id="exp_${hash}"

echo "=========================="
echo "mikoto run id: $mikoto_run_id"
echo "=========================="

# Pythonスクリプトを呼び出して復元処理を行う
poetry run python run/time_huroshiki.py "$mikoto_run_id" || exit 1

# ファイル名を復元後に保存したファイルから取得
restored_file=$(cat .restored_file.tmp)
to_mikoto_run_id=$(cat .restored_file2.tmp)

# Gitで add & commit
git add "$restored_file"
git commit -m "Restore $restored_file from mikoto_run_id tag $to_mikoto_run_id"
git tag "$mikoto_run_id"

# 後処理
rm .restored_file.tmp
rm .restored_file2.tmp

echo "✅ 復元とコミットが完了しました。"
