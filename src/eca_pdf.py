import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import os
from tqdm import tqdm
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def create_pdf_with_flexible_grid(input_folder, output_pdf, per_page, rows, cols):
    # A4サイズの寸法をインチ単位で指定
    fig_width = 8.27
    fig_height = 11.69

    if rows * cols != per_page:
        raise ValueError("Rows x Columns must equal per_page images.")

    # フォルダ内の画像ファイル名リストを自然順でソート
    image_files = [f for f in os.listdir(input_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
    image_files.sort(key=natural_sort_key)

    # PDFファイルの準備
    with PdfPages(output_pdf) as pdf:
        # 進捗バーを表示
        for i in tqdm(range(0, len(image_files), per_page), desc="Processing Pages"):
            fig, axs = plt.subplots(rows, cols, figsize=(fig_width, fig_height))  # 可変グリッド
            axs = axs.flatten()  # 2D配列を1D配列に変換
            for j, ax in enumerate(axs):
                if i + j < len(image_files):
                    filename = image_files[i + j]
                    path = os.path.join(input_folder, filename)
                    img = mpimg.imread(path)
                    # アスペクト比を保持して画像を表示
                    ax.imshow(img, aspect='equal')
                    ax.axis('off')  # 軸の非表示
                else:
                    ax.axis('off')  # 余分なサブプロットを非表示にする
            # PDFに保存
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
