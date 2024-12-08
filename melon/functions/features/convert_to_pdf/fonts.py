from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.rl_config import canvas_basefontname as _canvas_basefontname

# フォントファイルのパスを設定
FONT_PATH_JP = '/opt/python/fonts/ipaexm.ttf'
FONT_PATH_EN = '/opt/python/fonts/times new roman bold italic.ttf'

def register_fonts():
    """
    日本語と英語のフォントを登録する関数。
    """
    # 日本語フォントの登録
    pdfmetrics.registerFont(TTFont("IPAexMincho", FONT_PATH_JP))
    # 英語フォントの登録
    pdfmetrics.registerFont(TTFont("TimesNewRoman", FONT_PATH_EN))
    # デフォルトフォントを日本語フォント（明朝体）に設定
    _canvas_basefontname = 'IPAexMincho'
