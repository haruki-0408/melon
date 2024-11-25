
# def generate_equation_image(latex_code, font_prop):
#     """
#     LaTeXコードから数式画像を生成し、BytesIOオブジェクトを返す関数
#     数式の幅を動的に調整してA4サイズに収まるようにする。
#     """
#     try:
#         # LaTeXコードのサニタイズ
#         sanitized_latex = sanitize_latex_code(latex_code)

#         # Matplotlibを使用して数式画像を生成
#         fig = plt.figure()
#         text_obj = fig.text(
#             0.5, 0.5, f'${sanitized_latex}$',
#             fontsize=12, ha='center', va='center',
#             fontproperties=font_prop
#         )
#         fig.patch.set_alpha(0)

#         # 一度描画してサイズを取得
#         fig.canvas.draw()
#         renderer = fig.canvas.get_renderer()
#         bbox = text_obj.get_window_extent(renderer)

#         # A4サイズの横幅（ポイント単位）
#         A4_WIDTH_PT = 595.27  # A4横幅のポイント数
#         dpi = fig.dpi

#         # bbox.width をスケール基準に調整
#         image_width_inch = bbox.width / dpi
#         if image_width_inch > (A4_WIDTH_PT / dpi):  # A4に収まらない場合
#             scale_factor = (A4_WIDTH_PT / dpi) / image_width_inch
#             new_width = bbox.width * scale_factor
#             new_height = bbox.height * scale_factor
#         else:  # サイズ変更不要
#             new_width = bbox.width
#             new_height = bbox.height

#         fig.set_size_inches(new_width / dpi, new_height / dpi)

#         # 画像をバイナリデータとして取得
#         image_buffer = io.BytesIO()
#         plt.savefig(
#             image_buffer,
#             format='png',
#             dpi=dpi,
#             bbox_inches='tight',
#             pad_inches=0.0,
#             transparent=True
#         )
#         plt.close(fig)
#         image_buffer.seek(0)
#         return image_buffer

#     except Exception as e:
#         logger.exception(f"数式画像の生成中にエラーが発生しました: {e}")
#         return None
    
# def generate_parameter_image(symbol, description, font_prop):
#     """
#     パラメータのシンボルと説明から画像を生成し、BytesIOオブジェクトを返す関数。
#     画像サイズを動的に調整してA4サイズに収まるようにする。
#     """
#     try:
#         # LaTeXコードのサニタイズ
#         sanitized_symbol = sanitize_latex_code(symbol)
#         sanitized_description = description

#         # Matplotlibを使用して画像を生成
#         fig = plt.figure()
#         combined_text = f'${sanitized_symbol}$ : {sanitized_description}'
#         text_obj = fig.text(
#             0.5, 0.5, combined_text,
#             fontsize=12, ha='center', va='center',
#             fontproperties=font_prop
#         )
#         fig.patch.set_alpha(0)

#         # 一度描画してサイズを取得
#         fig.canvas.draw()
#         renderer = fig.canvas.get_renderer()
#         bbox = text_obj.get_window_extent(renderer)

#         # A4サイズの横幅（ポイント単位）
#         A4_WIDTH_PT = 595.27  # A4横幅のポイント数
#         dpi = fig.dpi

#         # bbox.width をスケール基準に調整
#         image_width_inch = bbox.width / dpi
#         if image_width_inch > (A4_WIDTH_PT / dpi):  # A4に収まらない場合
#             scale_factor = (A4_WIDTH_PT / dpi) / image_width_inch
#             new_width = bbox.width * scale_factor
#             new_height = bbox.height * scale_factor
#         else:  # サイズ変更不要
#             new_width = bbox.width
#             new_height = bbox.height

#         fig.set_size_inches(new_width / dpi, new_height / dpi)

#         # 画像をバイナリデータとして取得
#         image_buffer = io.BytesIO()
#         plt.savefig(
#             image_buffer,
#             format='png',
#             dpi=dpi,
#             bbox_inches='tight',
#             pad_inches=0.0,
#             transparent=True
#         )
#         plt.close(fig)
#         image_buffer.seek(0)
#         return image_buffer

#     except Exception as e:
#         logger.exception(f"パラメータ画像の生成中にエラーが発生しました: {e}")
#         return None
def generate_equation_image(latex_code, font_prop):
    """
    LaTeXコードから数式画像を生成し、BytesIOオブジェクトを返す関数。
    数式がフォントサイズ12で描画され、画像のサイズが適切になるように調整します。
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_latex = sanitize_latex_code(latex_code)

        # フォントサイズを12に設定
        fontsize = 12

        # Matplotlibを使用して数式画像を生成
        fig = plt.figure(figsize=(0.01, 0.01))  # 初期サイズは小さく
        fig.patch.set_alpha(0)  # 背景を透明に

        # テキストオブジェクトを追加
        text_obj = fig.text(
            0, 0, f"${sanitized_latex}$",
            fontsize=fontsize, fontproperties=font_prop
        )

        # 図のレイアウトを調整
        # fig.tight_layout()

        # 描画してバウンディングボックスを取得
        renderer = fig.canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer)

        # 画像サイズを計算（インチ単位）
        width_inch = (bbox.width + 10) / fig.dpi  # 余白を10ピクセル追加
        height_inch = (bbox.height + 10) / fig.dpi

        # Figureのサイズを再設定
        fig.set_size_inches(width_inch, height_inch)

        # テキストオブジェクトの位置を調整
        text_obj.set_position((5 / bbox.width, 5 / bbox.height))

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        fig.savefig(
            image_buffer,
            format='png',
            dpi=fig.dpi,
            bbox_inches='tight',
            pad_inches=0.0,
            transparent=True
        )
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        logger.exception(f"数式画像の生成中にエラーが発生しました: {e}")
        return None


def generate_parameter_image(symbol, description, font_prop):
    """
    パラメータのシンボルと説明から画像を生成し、BytesIOオブジェクトを返す関数。
    シンボルと説明がフォントサイズ8で描画され、画像のサイズが適切になるように調整します。
    """
    try:
        # LaTeXコードのサニタイズ
        sanitized_symbol = sanitize_latex_code(symbol)
        sanitized_description = description

        # フォントサイズを8に設定
        fontsize = 10.5

        # 表示するテキストを作成
        combined_text = f"${sanitized_symbol}$ : {sanitized_description}"

        # Matplotlibを使用して画像を生成
        fig = plt.figure(figsize=(4, 0.5), dpi=200)  # 幅と高さを小さく設定
        fig.patch.set_alpha(0)  # 背景を透明に

        # テキストオブジェクトを追加
        text_obj = fig.text(
            0.5, 0.5, combined_text,
            fontsize=fontsize, ha='center', va='center', fontproperties=font_prop
        )

        # 不要な軸を非表示
        plt.axis('off')

        # 図のレイアウトを調整
        fig.tight_layout(pad=0)

        # 画像をバイナリデータとして取得
        image_buffer = io.BytesIO()
        fig.savefig(
            image_buffer,
            format='png',
            dpi=200,
            bbox_inches='tight',
            pad_inches=0.0,
            transparent=True
        )
        plt.close(fig)
        image_buffer.seek(0)
        return image_buffer

    except Exception as e:
        logger.exception(f"パラメータ画像の生成中にエラーが発生しました: {e}")
        return None