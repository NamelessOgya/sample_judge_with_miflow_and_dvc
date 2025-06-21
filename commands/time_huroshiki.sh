# ① タイムスタンプ取得
timestamp=$(date +%Y%m%d%H%M%S)

# ② ハッシュ生成し、一時ファイルとして吐き出す。
hash=$(echo -n "$timestamp" | sha1sum | cut -c1-12)
mikoto_run_id="exp_${hash}"
echo "mikoto_run_id: \"$mikoto_run_id\"" > current_run.yaml


echo "=========================="
echo "mikoto run id: $mikoto_run_id"
echo "=========================="

# === 入力受付 ===
echo "=========================="
read -p "復元したいファイルパスを入力してください（例: data/fileA.csv）: " FILE_PATH
echo "=========================="
read -p "復元元のmikoto_run_idを入力してください（例: exp_XXXXXX）: " COMMIT_ID
echo "=========================="

# .dvcファイルのパスを生成
DVC_FILE="${FILE_PATH}.dvc"

# === 入力チェック ===
if [ ! -f "$DVC_FILE" ]; then
  echo "❌ エラー: DVCファイルが存在しません: $DVC_FILE"
  exit 1
fi

if ! git cat-file -e "${COMMIT_ID}^{commit}" 2>/dev/null; then
  echo "❌ エラー: 指定されたコミットIDは存在しません: $COMMIT_ID"
  exit 1
fi

# === 復元処理 ===
echo "📦 $DVC_FILE をコミット $COMMIT_ID の状態に復元します..."

# 指定されたコミットの.dvcファイルを一時的にcheckout
git checkout "$COMMIT_ID" -- "$DVC_FILE"

# DVCキャッシュからファイルを復元
dvc checkout "$DVC_FILE"

# Gitに追加して新しいコミットを作成
git add "$FILE_PATH" "$DVC_FILE"
git commit -m "AUto: Restore $FILE_PATH from mikoto_run_id $COMMIT_ID"
git tag "$mikoto_run_id"