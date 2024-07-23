import os
from eca_simulation import Rule, CellularAutomaton, ECAPlotter
from eca_pdf import create_pdf_with_flexible_grid
from tqdm import tqdm

def simulate_and_save_images(is_rand, max_t, output_folder):
    for rule_no in tqdm(range(256), desc="Processing rules"):
        rule = Rule(rule_no)
        automaton = CellularAutomaton(size=50, is_rand=is_rand)
        automaton.run(rule, max_t)
        current_state = automaton.get_current_state()
        ECAPlotter.plot_and_save(current_state, rule_no, output_folder)

def main():
    is_rand = False  # 初期状態のフラグ
    max_t = 50  # 最大ステップ数
    base_folder = 'eca_results'

    # フォルダとPDFの名前を設定
    if is_rand:
        output_folder = f"{base_folder}_rand"
        output_pdf = f"{base_folder}_rand.pdf"
    else:
        output_folder = base_folder
        output_pdf = f"{base_folder}.pdf"

    # シミュレーションと画像保存
    simulate_and_save_images(is_rand, max_t, output_folder)

    # 画像をPDFにまとめる
    per_page = 8  # 1ページに配置する画像の数
    rows = 4      # グリッドの行数
    cols = 2      # グリッドの列数
    create_pdf_with_flexible_grid(output_folder, output_pdf, per_page, rows, cols)

if __name__ == "__main__":
    main()
