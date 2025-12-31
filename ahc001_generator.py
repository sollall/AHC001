#!/usr/bin/env python3
# coding: utf-8
"""
AHC001のテストケースジェネレーター（Python実装）

公式ジェネレーターの仕様:
https://atcoder.jp/contests/ahc001/tasks/ahc001_a

使い方:
    python ahc001_generator.py <seed>
"""

import sys
import random


class AHC001Generator:
    """AHC001のテストケースを生成"""

    SIZE = 10000  # マップサイズ

    def __init__(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)

    def generate_n(self) -> int:
        """会社数Nを生成"""
        # N = round(50 × 4^rand())
        # rand()は[0, 1)の一様乱数
        rand_val = self.rng.random()
        n = round(50 * (4 ** rand_val))
        return n

    def generate_positions(self, n: int) -> list:
        """
        N個の異なる座標を生成

        Returns:
            [(x1, y1), (x2, y2), ..., (xn, yn)]
        """
        # 効率的に重複しない座標を生成
        positions = set()
        while len(positions) < n:
            x = self.rng.randint(0, self.SIZE - 1)
            y = self.rng.randint(0, self.SIZE - 1)
            positions.add((x, y))

        return list(positions)

    def generate_areas(self, n: int) -> list:
        """
        各会社の希望面積を生成

        Returns:
            [r1, r2, ..., rn]
        """
        # 面積の生成ロジック
        # より小さい範囲で生成（1から10000の範囲）
        areas = []

        for _ in range(n):
            # 1から10000の範囲でランダムに生成
            # 対数スケールを使用して小さい値が出やすくする
            rand_val = self.rng.random()
            area = round(1 + (10000 - 1) * (rand_val ** 2))
            areas.append(area)

        return areas

    def generate(self) -> str:
        """
        テストケースを生成して文字列として返す

        Returns:
            テストケースの文字列
        """
        # 会社数を生成
        n = self.generate_n()

        # 座標を生成
        positions = self.generate_positions(n)

        # 面積を生成
        areas = self.generate_areas(n)

        # 出力フォーマット
        lines = [str(n)]
        for i in range(n):
            x, y = positions[i]
            r = areas[i]
            lines.append(f"{x} {y} {r}")

        return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) != 2:
        print(f"使い方: {sys.argv[0]} <seed>", file=sys.stderr)
        print(f"例: {sys.argv[0]} 0", file=sys.stderr)
        sys.exit(1)

    try:
        seed = int(sys.argv[1])
    except ValueError:
        print(f"エラー: seedは整数で指定してください", file=sys.stderr)
        sys.exit(1)

    # ジェネレーターを初期化
    generator = AHC001Generator(seed)

    # テストケースを生成して出力
    testcase = generator.generate()
    print(testcase, end='')


if __name__ == "__main__":
    main()
