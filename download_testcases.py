#!/usr/bin/env python3
# coding: utf-8
"""
AtCoderのテストケースを自動生成するスクリプト

使い方:
    python download_testcases.py --generator tools/gen.exe --num-tests 100
    python download_testcases.py --seeds 0-99

例:
    # ジェネレーターを使って100個生成
    python download_testcases.py --generator tools/gen.exe --num-tests 100

    # シード範囲を指定
    python download_testcases.py --generator ./gen --seeds 0-49
"""

import argparse
import os
import subprocess
import sys
import re
from pathlib import Path


def generate_testcases(generator_path: str, num_tests: int, input_dir: str = "in", seed_start: int = 0):
    """
    ジェネレーターを使ってテストケースを生成

    Args:
        generator_path: ジェネレーターの実行ファイルパス
        num_tests: 生成するテストケース数
        input_dir: 出力先ディレクトリ
        seed_start: 開始シード値
    """
    print(f"🔧 ジェネレーター: {generator_path}")
    print(f"📊 生成数: {num_tests}個 (シード {seed_start} から {seed_start + num_tests - 1})")

    input_path = Path(input_dir)
    input_path.mkdir(exist_ok=True)

    gen_path = Path(generator_path)
    if not gen_path.exists():
        print(f"❌ エラー: ジェネレーターが見つかりません: {generator_path}")
        return False

    print(f"\n🚀 テストケースを生成中...")

    # Pythonスクリプトかどうかを判定
    is_python = generator_path.endswith('.py')

    success_count = 0
    for i in range(num_tests):
        seed = seed_start + i
        output_file = input_path / f"{str(i).zfill(4)}.txt"

        try:
            # コマンドを構築
            if is_python:
                cmd = ["python", str(gen_path), str(seed)]
            else:
                cmd = [str(gen_path), str(seed)]

            # ジェネレーターを実行してファイルに書き込み
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True
                )

            if result.returncode == 0:
                success_count += 1
                if (i + 1) % 10 == 0 or i == num_tests - 1:
                    print(f"  ✓ {i + 1}/{num_tests} 生成完了")
            else:
                print(f"  ✗ シード {seed} の生成に失敗: {result.stderr}")

        except Exception as e:
            print(f"  ✗ シード {seed} の生成中にエラー: {e}")

    print(f"\n✅ 生成完了: {success_count}/{num_tests} ファイル")
    return success_count > 0


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
            print(f"⚠️  警告: {result.stderr}")
            return False

        print(f"✅ ダウンロード完了!")
        return True

    except FileNotFoundError:
        print("⚠️  ojコマンドが見つかりません（スキップ）")
        return False


def rename_testcases(input_dir: str = "in", start_index: int = 0):
    """
    ダウンロードしたテストケースを0000.txt, 0001.txt形式にリネーム

    Args:
        input_dir: テストケースのディレクトリ
        start_index: 開始インデックス

    Returns:
        リネームしたファイル数
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"❌ ディレクトリが見つかりません: {input_dir}")
        return 0

    # sample-*.txt や *.in などのファイルを探す
    test_files = sorted(
        [f for f in input_path.iterdir() if f.is_file() and f.suffix in ['.txt', '.in']],
        key=lambda x: x.name
    )

    # README.mdと既に正しい形式のファイルを除外
    test_files = [f for f in test_files if f.name != 'README.md' and not re.match(r'^\d{4}\.txt$', f.name)]

    if not test_files:
        return 0

    print(f"\n📝 {len(test_files)}個のテストケースをリネーム中...")

    for idx, old_file in enumerate(test_files):
        new_name = f"{str(start_index + idx).zfill(4)}.txt"
        new_path = input_path / new_name

        if old_file.name != new_name:
            old_file.rename(new_path)
            print(f"  {old_file.name} → {new_name}")

    print(f"✅ リネーム完了!")
    return len(test_files)


def main():
    parser = argparse.ArgumentParser(
        description="AtCoderのテストケースを自動生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # ジェネレーターで100個生成
  python download_testcases.py --generator tools/gen.exe --num-tests 100

  # シード範囲を指定
  python download_testcases.py --generator ./gen --seeds 0-99

  # サンプルをダウンロードしてから追加生成
  python download_testcases.py ahc001 --generator tools/gen.exe --num-tests 100
        """
    )

    parser.add_argument(
        'contest',
        nargs='?',
        help='コンテストIDまたはURL (例: ahc001) - 省略可'
    )

    parser.add_argument(
        '--generator', '-g',
        default='ahc001_generator.py',
        help='テストケースジェネレーターのパス (デフォルト: ahc001_generator.py)'
    )

    parser.add_argument(
        '--num-tests', '-n',
        type=int,
        default=100,
        help='生成するテストケース数 (デフォルト: 100)'
    )

    parser.add_argument(
        '--seeds', '-s',
        help='シード範囲 (例: 0-99, 100-199)'
    )

    parser.add_argument(
        '--input-dir',
        default='in',
        help='入力ファイルの保存先ディレクトリ (デフォルト: in)'
    )

    args = parser.parse_args()

    # シード範囲の解析
    seed_start = 0
    num_tests = args.num_tests

    if args.seeds:
        match = re.match(r'^(\d+)-(\d+)$', args.seeds)
        if match:
            seed_start = int(match.group(1))
            seed_end = int(match.group(2))
            num_tests = seed_end - seed_start + 1
        else:
            print(f"❌ エラー: シード範囲の形式が不正です: {args.seeds}")
            print("   正しい形式: 0-99")
            sys.exit(1)

    print("="*60)
    print("🚀 AtCoder テストケース自動生成")
    print("="*60)

    # ディレクトリ作成
    Path(args.input_dir).mkdir(exist_ok=True)

    # オプション: 公式サンプルをダウンロード
    downloaded_count = 0
    if args.contest:
        # URLの構築
        if args.contest.startswith('http'):
            contest_url = args.contest
        else:
            contest_id = args.contest.lower()
            if re.match(r'^ahc\d+$', contest_id):
                contest_url = f"https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_a"
            else:
                contest_url = f"https://atcoder.jp/contests/{contest_id}"

        if download_with_oj(contest_url, args.input_dir):
            downloaded_count = rename_testcases(args.input_dir, 0)

    # ジェネレーターで生成
    if args.generator:
        # サンプルケースをダウンロードした場合は、その分をスキップ
        actual_start = seed_start + downloaded_count
        actual_count = num_tests - downloaded_count

        if actual_count > 0:
            if not generate_testcases(args.generator, actual_count, args.input_dir, actual_start):
                sys.exit(1)
    elif not args.contest:
        print("❌ エラー: コンテストIDまたはジェネレーターを指定してください")
        parser.print_help()
        sys.exit(1)

    # 最終的なテストケース数をカウント
    final_count = len([f for f in Path(args.input_dir).iterdir()
                      if f.is_file() and f.suffix == '.txt' and f.name != 'README.md'])

    print("\n" + "="*60)
    print(f"🎉 完了! {final_count}個のテストケースを準備しました")
    print("="*60)
    print(f"\n📂 保存先: {args.input_dir}/")
    print(f"\n次のコマンドでソルバーを実行できます:")
    print(f"  python debug.py --module_name scripts.first_answer --test_id 0")
    print(f"  python optimizer.py")


if __name__ == "__main__":
    main()
