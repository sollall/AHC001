#!/usr/bin/env python3
# coding: utf-8
"""
AtCoderのテストケースを自動ダウンロードするスクリプト

使い方:
    python download_testcases.py <contest_id>

例:
    python download_testcases.py ahc001
"""

import argparse
import os
import subprocess
import sys
import re
from pathlib import Path


def download_with_oj(contest_url: str, output_dir: str = "in"):
    """
    online-judge-tools (oj) を使ってテストケースをダウンロード

    Args:
        contest_url: AtCoderのコンテストURL
        output_dir: 出力先ディレクトリ
    """
    print(f"🔍 テストケースをダウンロード中: {contest_url}")

    # ojコマンドでダウンロード
    try:
        # テストケースをダウンロード
        result = subprocess.run(
            ["oj", "download", contest_url, "-d", output_dir],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ エラー: {result.stderr}")
            return False

        print(f"✅ ダウンロード完了!")
        return True

    except FileNotFoundError:
        print("❌ エラー: ojコマンドが見つかりません")
        print("以下のコマンドでインストールしてください:")
        print("  pip install online-judge-tools")
        return False


def rename_testcases(input_dir: str = "in"):
    """
    ダウンロードしたテストケースを0000.txt, 0001.txt形式にリネーム

    Args:
        input_dir: テストケースのディレクトリ
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"❌ ディレクトリが見つかりません: {input_dir}")
        return

    # sample-*.txt や *.in などのファイルを探す
    test_files = sorted(
        [f for f in input_path.iterdir() if f.is_file() and f.suffix in ['.txt', '.in']],
        key=lambda x: x.name
    )

    # README.mdを除外
    test_files = [f for f in test_files if f.name != 'README.md']

    if not test_files:
        print(f"⚠️  テストケースが見つかりません: {input_dir}")
        return

    print(f"\n📝 {len(test_files)}個のテストケースをリネーム中...")

    for idx, old_file in enumerate(test_files):
        new_name = f"{str(idx).zfill(4)}.txt"
        new_path = input_path / new_name

        if old_file.name != new_name:
            old_file.rename(new_path)
            print(f"  {old_file.name} → {new_name}")

    print(f"✅ リネーム完了!")


def create_output_placeholders(num_tests: int, output_dir: str = "out"):
    """
    出力ディレクトリに空のプレースホルダーを作成

    Args:
        num_tests: テストケース数
        output_dir: 出力先ディレクトリ
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    print(f"\n📂 出力ディレクトリを準備中...")

    for idx in range(num_tests):
        placeholder = output_path / f"{str(idx).zfill(4)}.txt"
        placeholder.touch()

    print(f"✅ {num_tests}個の出力ファイルを作成!")


def main():
    parser = argparse.ArgumentParser(
        description="AtCoderのテストケースを自動ダウンロード",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python download_testcases.py ahc001
  python download_testcases.py https://atcoder.jp/contests/ahc001/tasks/ahc001_a
        """
    )

    parser.add_argument(
        'contest',
        help='コンテストIDまたはURL (例: ahc001 または https://atcoder.jp/contests/ahc001/tasks/ahc001_a)'
    )

    parser.add_argument(
        '--input-dir',
        default='in',
        help='入力ファイルの保存先ディレクトリ (デフォルト: in)'
    )

    parser.add_argument(
        '--output-dir',
        default='out',
        help='出力ファイルの保存先ディレクトリ (デフォルト: out)'
    )

    args = parser.parse_args()

    # URLの構築
    if args.contest.startswith('http'):
        contest_url = args.contest
    else:
        # コンテストIDから推測
        contest_id = args.contest.lower()
        # ahc001のような形式ならタスクURLを構築
        if re.match(r'^ahc\d+$', contest_id):
            contest_url = f"https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_a"
        else:
            contest_url = f"https://atcoder.jp/contests/{contest_id}"

    print("="*60)
    print("🚀 AtCoder テストケース自動ダウンロード")
    print("="*60)

    # ディレクトリ作成
    Path(args.input_dir).mkdir(exist_ok=True)
    Path(args.output_dir).mkdir(exist_ok=True)

    # テストケースをダウンロード
    if not download_with_oj(contest_url, args.input_dir):
        sys.exit(1)

    # リネーム
    rename_testcases(args.input_dir)

    # テストケース数をカウント
    num_tests = len([f for f in Path(args.input_dir).iterdir()
                     if f.is_file() and f.suffix == '.txt' and f.name != 'README.md'])

    # 出力プレースホルダー作成
    create_output_placeholders(num_tests, args.output_dir)

    print("\n" + "="*60)
    print(f"🎉 完了! {num_tests}個のテストケースを準備しました")
    print("="*60)
    print(f"\n次のコマンドでソルバーを実行できます:")
    print(f"  python debug.py --module_name scripts.first_answer --test_id 0")
    print(f"  python optimizer.py")


if __name__ == "__main__":
    main()
