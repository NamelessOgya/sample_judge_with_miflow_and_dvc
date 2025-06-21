import sys
import yaml
import subprocess
from pathlib import Path

def main():

    print("==========================")
    target_file = input("復元したいファイルパスを入力してください（例: data/submit/foo.csv）: ").strip()
    print("==========================")
    mikoto_run_id = input("mikoto_run_idを入力してください。（例: exp_XXXX）: ").strip()
    print("==========================")
    print(f"🔁 タグ {mikoto_run_id} から dvc.lock を取得...")

    tmp_lock = Path(f".tmp_dvc_lock_{mikoto_run_id}.yaml")

    try:
        subprocess.run(
            ["git", "show", f"{mikoto_run_id}:dvc.lock"],
            check=True,
            stdout=tmp_lock.open("w")
        )
    except subprocess.CalledProcessError:
        print(f"❌ {mikoto_run_id} に対応する dvc.lock を取得できませんでした。")
        sys.exit(1)

    with tmp_lock.open("r") as f:
        lock_data = yaml.safe_load(f)

    found = False
    for stage in lock_data.get("stages", {}).values():
        for output in stage.get("outs", []):
            if output.get("path") == target_file:
                md5_value = output.get("md5")
                found = True
                break
        if found:
            break

    if not found:
        print(f"❌ {mikoto_run_id} 時点の {target_file} に対応する md5 が見つかりません。")
        sys.exit(1)

    with open("dvc.lock", "r") as f:
        current_lock = yaml.safe_load(f)

    modified = False
    for stage in current_lock.get("stages", {}).values():
        for output in stage.get("outs", []):
            if output.get("path") == target_file:
                output["md5"] = md5_value
                modified = True

    if not modified:
        print(f"⚠️ 現在の dvc.lock に {target_file} の定義が見つかりません。")
        sys.exit(1)

    with open("dvc.lock", "w") as f:
        yaml.dump(current_lock, f, sort_keys=False)

    subprocess.run(["poetry", "run", "dvc", "pull", target_file], check=True)

    # 復元対象ファイル名を一時ファイルに書き出し（shell側で git add に使う）
    Path(".restored_file.tmp").write_text(target_file)
    Path(".restored_file2.tmp").write_text(mikoto_run_id)

if __name__ == "__main__":
    main()
