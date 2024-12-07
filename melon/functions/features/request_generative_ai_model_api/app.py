import json
from aws_lambda_powertools import Logger
from anthropic_client import AnthropicClient
from utilities import upload_to_s3

logger = Logger(service_name="request_generative_ai_model_api")

# 生成AI リクエストインスタンス生成
client = AnthropicClient()  

@logger.inject_lambda_context(log_event=False)
def lambda_handler(event, context):
    workflow_id = event.get("workflow_id")
    title = event.get("title")  
    sections_format = [
        {
        "sub_sections": [
            {
            "title_name": "歴史的背景の紹介",
            "text": "古代ローマ帝国の通信技術は、これまで歴史学者によって完全に見逃されてきた驚くべき先進性を秘めていた。本研究は、彼らが実際には原始的なWi-Fiネットワークシステムを開発していたという、これまで誰も想像できなかった革新的な事実を明らかにする。\n\n紀元前1世紀から紀元後3世紀にかけて、ローマ帝国の工学者たちは、現代のワイヤレス通信技術の驚くべき先駆けとなるシステムを密かに開発していたのである。彼らは、光学的信号伝達、音響波通信、そして驚くべきことに電磁波の初期的な理解を組み合わせて、広大な帝国全体をカバーする通信網を構築していた。\n\n[INSERT_GRAPH_ROMAN_WIFI_COVERAGE]",
            "graphs": [
                {
                "id": "GRAPH_ROMAN_WIFI_COVERAGE",
                "figure_width": 6.5,
                "figure_height": 4.5,
                "title": "ローマ帝国のWi-Fiネットワーク推定カバレッジ",
                "xlabel": "地理的範囲（km）",
                "ylabel": "通信強度（仮想単位）",
                "grid": True,
                "legend": True,
                "charts": [
                    {
                    "chart_type": "area",
                    "x": [
                        0,
                        500,
                        1000,
                        1500,
                        2000,
                        2500,
                        3000
                    ],
                    "y1": [
                        0.1,
                        0.3,
                        0.6,
                        0.8,
                        0.9,
                        0.7,
                        0.5
                    ],
                    "y2": [
                        0,
                        0.1,
                        0.2,
                        0.3,
                        0.4,
                        0.3,
                        0.2
                    ],
                    "colors": [
                        "rgba(100, 149, 237, 0.5)",
                        "rgba(255, 182, 193, 0.3)"
                    ],
                    "alphas": [
                        0.5,
                        0.3
                    ]
                    }
                ]
                }
            ],
            "tables": [],
            "formulas": []
            },
            {
            "title_name": "現代とのつながりや影響",
            "text": "驚くべきことに、ローマ帝国の通信技術は、現代のワイヤレスネットワークの基本的な概念に驚くほど近いものだった。彼らは、光学的信号塔、音響反射板、そして原始的な電磁波変調技術を巧みに組み合わせて、広大な帝国全体をカバーする通信網を構築していたのである。\n\n[INSERT_TABLE_TECH_COMPARISON]\n\n特に注目すべきは、彼らが開発した「光学Wi-Fi」システムである。山頂に設置された特殊な鏡と反射装置を使用し、数百キロメートルにわたって情報を伝達することができた。これは、現代のLi-Fi技術の驚くべき先駆けと言えるだろう。\n\n[INSERT_FORMULA_SIGNAL_TRANSMISSION]",
            "graphs": [],
            "tables": [
                {
                "id": "TABLE_TECH_COMPARISON",
                "table_type": "comparison",
                "title": "古代ローマのWi-Fi技術と現代技術の比較",
                "comparison_data": {
                    "信号伝達距離": {
                    "mean": 250,
                    "std": 50,
                    "min": 100,
                    "max": 400
                    },
                    "通信速度": {
                    "mean": 0.5,
                    "std": 0.2,
                    "min": 0.1,
                    "max": 1
                    },
                    "エネルギー効率": {
                    "mean": 0.3,
                    "std": 0.1,
                    "min": 0.1,
                    "max": 0.5
                    }
                },
                "style": {
                    "header_bg_color": "#4682B4",
                    "header_font_color": "white",
                    "cell_bg_color": "#F0F8FF",
                    "cell_font_color": "black",
                    "border_color": "#87CEEB",
                    "border_width": 1
                }
                }
            ],
            "formulas": [
                {
                "id": "FORMULA_SIGNAL_TRANSMISSION",
                "latex_code": "S_{t} = \\frac{P_{r} \\cdot G_{t} \\cdot G_{r} \\cdot \\lambda^{2}}{(4\\pi d)^{2}}",
                "description": "古代ローマの光学Wi-Fi信号伝達モデル",
                "parameters": [
                    {
                    "symbol": "S_{t}",
                    "description": "信号伝達強度"
                    },
                    {
                    "symbol": "P_{r}",
                    "description": "送信電力"
                    },
                    {
                    "symbol": "G_{t}",
                    "description": "送信アンテナ利得"
                    },
                    {
                    "symbol": "G_{r}",
                    "description": "受信アンテナ利得"
                    },
                    {
                    "symbol": "\\lambda",
                    "description": "波長"
                    },
                    {
                    "symbol": "d",
                    "description": "送受信間距離"
                    }
                ]
                }
            ]
            }
        ],
        "title_name": "はじめに"
        },
        {
        "sub_sections": [
            {
            "title_name": "具体的な出来事や現象の説明",
            "text": "ローマ帝国の通信技術は、驚くべき洗練された「光学Wi-Fiネットワーク」として機能していた。特に、帝国の軍事通信と行政システムにおいて、この革新的な技術は驚くべき効率性を発揮していた。\n\n主要な通信手法は、山頂に設置された特殊な反射鏡と光学信号塔のネットワークであった。これらの装置は、太陽光や火を利用して、複雑な二進法コードを数百キロメートルにわたって伝達することができた。\n\n[INSERT_GRAPH_SIGNAL_TRANSMISSION]\n\n興味深いことに、彼らは光の反射角度、太陽の位置、そして特殊な鏡の形状を巧みに操作することで、現代のデジタル通信に匹敵するほど複雑な情報伝達を実現していたのである。\n\n[INSERT_TABLE_COMMUNICATION_METHODS]",
            "graphs": [
                {
                "id": "GRAPH_SIGNAL_TRANSMISSION",
                "figure_width": 6.5,
                "figure_height": 4.5,
                "title": "古代ローマの光学Wi-Fi信号伝達効率",
                "xlabel": "距離（km）",
                "ylabel": "信号強度",
                "grid": True,
                "legend": True,
                "charts": [
                    {
                    "chart_type": "line",
                    "lines": [
                        {
                        "x": [
                            0,
                            100,
                            200,
                            300,
                            400,
                            500
                        ],
                        "y": [
                            1,
                            0.8,
                            0.6,
                            0.4,
                            0.3,
                            0.2
                        ],
                        "label": "信号強度",
                        "color": "blue",
                        "linestyle": "-",
                        "marker": "o"
                        }
                    ]
                    }
                ]
                }
            ],
            "tables": [
                {
                "id": "TABLE_COMMUNICATION_METHODS",
                "table_type": "basic",
                "title": "ローマ帝国の通信方法",
                "columns": [
                    "通信方法",
                    "最大距離",
                    "情報伝達速度",
                    "使用頻度"
                ],
                "rows": [
                    [
                    "光学信号塔",
                    "500 km",
                    "高",
                    "軍事通信"
                    ],
                    [
                    "音響反射板",
                    "200 km",
                    "中",
                    "地域間連絡"
                    ],
                    [
                    "火災信号",
                    "100 km",
                    "低",
                    "緊急警報"
                    ]
                ],
                "style": {
                    "header_bg_color": "#4682B4",
                    "header_font_color": "white",
                    "cell_bg_color": "#F0F8FF",
                    "cell_font_color": "black",
                    "border_color": "#87CEEB",
                    "border_width": 1
                }
                }
            ],
            "formulas": []
            },
            {
            "title_name": "その影響と結果",
            "text": "ローマ帝国の通信技術は、単なる技術的な好奇心以上の重大な歴史的影響を持っていた。この驚くべき通信システムは、帝国の行政、軍事戦略、そして文化的統合に革命的な変化をもたらしたのである。\n\n[INSERT_FORMULA_COMMUNICATION_EFFICIENCY]\n\n特に注目すべきは、この通信技術が帝国の拡大と維持に果たした決定的な役割である。遠く離れた地域間での迅速な情報伝達は、中央政府の統制力を劇的に強化し、帝国の驚異的な安定性と持続性を可能にした。\n\n[INSERT_GRAPH_EMPIRE_EXPANSION]",
            "graphs": [
                {
                "id": "GRAPH_EMPIRE_EXPANSION",
                "figure_width": 6.5,
                "figure_height": 4.5,
                "title": "通信技術と帝国の拡大",
                "xlabel": "年代",
                "ylabel": "帝国領土面積",
                "grid": True,
                "legend": True,
                "charts": [
                    {
                    "chart_type": "area",
                    "x": [
                        0,
                        50,
                        100,
                        150,
                        200,
                        250,
                        300
                    ],
                    "y1": [
                        100000,
                        250000,
                        500000,
                        750000,
                        1000000,
                        1200000,
                        1500000
                    ],
                    "y2": [
                        0,
                        50000,
                        100000,
                        200000,
                        300000,
                        400000,
                        500000
                    ],
                    "colors": [
                        "rgba(70,130,180,0.5)",
                        "rgba(255,160,122,0.3)"
                    ],
                    "alphas": [
                        0.5,
                        0.3
                    ]
                    }
                ]
                }
            ],
            "tables": [],
            "formulas": [
                {
                "id": "FORMULA_COMMUNICATION_EFFICIENCY",
                "latex_code": "E_{c} = \\frac{I_{t} \\cdot D_{r}}{T_{p} \\cdot \\sqrt{D_{d}}}",
                "description": "ローマ帝国の通信効率モデル",
                "parameters": [
                    {
                    "symbol": "E_{c}",
                    "description": "通信効率"
                    },
                    {
                    "symbol": "I_{t}",
                    "description": "情報伝達強度"
                    },
                    {
                    "symbol": "D_{r}",
                    "description": "通信距離"
                    },
                    {
                    "symbol": "T_{p}",
                    "description": "伝達時間"
                    },
                    {
                    "symbol": "D_{d}",
                    "description": "情報の複雑さ"
                    }
                ]
                }
            ]
            }
        ],
        "title_name": "歴史的解析"
        },
        {
        "sub_sections": [
            {
            "title_name": "歴史的出来事が現代にどのように影響しているか",
            "text": "古代ローマのWi-Fi技術は、現代の通信技術に驚くべき影響を与えている。彼らの革新的なアプローチは、現代のワイヤレス通信の基本的な概念に驚くほど近いものだった。特に、光学的信号伝達と電磁波の初期的な理解は、今日のLi-Fi技術や無線通信システムの原型と言えるだろう。\n\n[INSERT_GRAPH_TECH_EVOLUTION]\n\n興味深いことに、ローマ帝国の通信技術は、現代のIoT（モノのインターネット）の概念にも驚くほど近い。彼らは、広範囲にわたる通信ネットワークを通じて、情報を迅速かつ効率的に伝達する方法を既に理解していたのである。\n\n[INSERT_TABLE_TECH_COMPARISON]",
            "graphs": [
                {
                "id": "GRAPH_TECH_EVOLUTION",
                "figure_width": 6.5,
                "figure_height": 4.5,
                "title": "通信技術の進化：古代ローマから現代へ",
                "xlabel": "技術世代",
                "ylabel": "通信効率",
                "grid": True,
                "legend": True,
                "charts": [
                    {
                    "chart_type": "line",
                    "lines": [
                        {
                        "x": [
                            "古代ローマ",
                            "中世",
                            "産業革命",
                            "20世紀",
                            "現代"
                        ],
                        "y": [
                            0.2,
                            0.1,
                            0.3,
                            0.7,
                            1
                        ],
                        "label": "通信効率",
                        "color": "red",
                        "linestyle": "-.",
                        "marker": "x"
                        }
                    ]
                    }
                ]
                }
            ],
            "tables": [
                {
                "id": "TABLE_TECH_COMPARISON",
                "table_type": "basic",
                "title": "通信技術の比較：古代vs現代",
                "columns": [
                    "技術",
                    "伝達速度",
                    "カバレッジ",
                    "エネルギー効率"
                ],
                "rows": [
                    [
                    "古代ローマWi-Fi",
                    "低速",
                    "限定的",
                    "非効率"
                    ],
                    [
                    "現代Wi-Fi",
                    "高速",
                    "広範囲",
                    "高効率"
                    ]
                ],
                "style": {
                    "header_bg_color": "#4682B4",
                    "header_font_color": "white",
                    "cell_bg_color": "#F0F8FF",
                    "cell_font_color": "black",
                    "border_color": "#87CEEB",
                    "border_width": 1
                }
                }
            ],
            "formulas": []
            },
            {
            "title_name": "現代の問題とその関連性の分析",
            "text": "現代の通信技術が直面している課題は、驚くべきことに、古代ローマの通信システムが既に解決していた問題と驚くほど類似している。セキュリティ、効率性、そして広範囲にわたる情報伝達の課題は、2000年前から人類が取り組んできた普遍的な挑戦なのである。\n\n[INSERT_GRAPH_PROBLEM_ANALYSIS]\n\n[INSERT_FORMULA_COMMUNICATION_CHALLENGE]\n\n本研究の最終的な結論として、古代ローマの通信技術は単なる歴史的な興味深い話題ではない。それは、人類の技術的進歩における連続性と創造性を示す驚くべき証拠なのである。私たちは過去から学び、未来へと続く技術的な知恵の連鎖を理解することができる。この研究は、技術の進化が直線的ではなく、むしろ螺旋状に発展することを明確に示している。",
            "graphs": [
                {
                "id": "GRAPH_PROBLEM_ANALYSIS",
                "figure_width": 6.5,
                "figure_height": 4.5,
                "title": "通信技術の課題分析",
                "xlabel": "課題の種類",
                "ylabel": "重要度",
                "grid": True,
                "legend": True,
                "charts": [
                    {
                    "chart_type": "bar",
                    "categories": [
                        "セキュリティ",
                        "速度",
                        "カバレッジ",
                        "エネルギー効率"
                    ],
                    "values": [
                        85,
                        75,
                        60,
                        50
                    ],
                    "colors": [
                        "red",
                        "blue",
                        "green",
                        "purple"
                    ]
                    }
                ]
                }
            ],
            "tables": [],
            "formulas": [
                {
                "id": "FORMULA_COMMUNICATION_CHALLENGE",
                "latex_code": "C_{t} = \\frac{S_{p} \\cdot E_{f}}{T_{l} \\cdot \\sqrt{D_{c}}}",
                "description": "通信技術の課題モデル",
                "parameters": [
                    {
                    "symbol": "C_{t}",
                    "description": "通信技術の複雑さ"
                    },
                    {
                    "symbol": "S_{p}",
                    "description": "システムの性能"
                    },
                    {
                    "symbol": "E_{f}",
                    "description": "エネルギー効率"
                    },
                    {
                    "symbol": "T_{l}",
                    "description": "技術的制限"
                    },
                    {
                    "symbol": "D_{c}",
                    "description": "データの複雑さ"
                    }
                ]
                }
            ]
            }
        ],
        "title_name": "現代への影響"
        },
        {
        "sub_sections": [
            {
            "title_name": "歴史から学んだ教訓",
            "text": "古代ローマのWi-Fi技術の研究から、私たちは驚くべき教訓を学ぶことができる。技術の進歩は直線的ではなく、むしろ螺旋状に発展し、過去の知恵が未来の革新を導く可能性があることを示している。\n\n[INSERT_GRAPH_LESSON_LEARNED]\n\n特に注目すべきは、限られたリソースと技術的制約の中で、いかに創造的な解決策を生み出すことができるかという点である。ローマ帝国の工学者たちは、利用可能な最小限の技術を用いて、驚くべき通信システムを構築したのである。\n\n[INSERT_TABLE_TECHNOLOGICAL_LESSONS]",
            "graphs": [
                {
                "id": "GRAPH_LESSON_LEARNED",
                "figure_width": 6.5,
                "figure_height": 4.5,
                "title": "技術革新の教訓",
                "xlabel": "イノベーションの段階",
                "ylabel": "創造性の程度",
                "grid": True,
                "legend": True,
                "charts": [
                    {
                    "chart_type": "line",
                    "lines": [
                        {
                        "x": [
                            1,
                            2,
                            3,
                            4,
                            5
                        ],
                        "y": [
                            0.2,
                            0.5,
                            0.8,
                            0.6,
                            0.9
                        ],
                        "label": "創造性",
                        "color": "green",
                        "linestyle": "-",
                        "marker": "o"
                        }
                    ]
                    }
                ]
                }
            ],
            "tables": [
                {
                "id": "TABLE_TECHNOLOGICAL_LESSONS",
                "table_type": "basic",
                "title": "技術革新から学ぶ教訓",
                "columns": [
                    "教訓",
                    "重要性",
                    "適用可能性"
                ],
                "rows": [
                    [
                    "創造的思考",
                    "高",
                    "普遍的"
                    ],
                    [
                    "リソースの最適活用",
                    "中",
                    "状況依存"
                    ],
                    [
                    "学際的アプローチ",
                    "高",
                    "広範囲"
                    ]
                ],
                "style": {
                    "header_bg_color": "#4682B4",
                    "header_font_color": "white",
                    "cell_bg_color": "#F0F8FF",
                    "cell_font_color": "black",
                    "border_color": "#87CEEB",
                    "border_width": 1
                }
                }
            ],
            "formulas": []
            },
            {
            "title_name": "現代社会への応用",
            "text": "ローマ帝国の通信技術から得られた洞察は、現代社会の様々な分野に直接応用可能である。特に、持続可能な技術開発、効率的な情報伝達、そして限られたリソースを最大限に活用する方法において、重要な示唆を提供している。\n\n[INSERT_FORMULA_TECHNOLOGICAL_APPLICATION]\n\n[INSERT_GRAPH_MODERN_APPLICATION]\n\n本研究の最終的な結論として、技術の進歩は単なる直線的な発展ではなく、過去の知恵と創造性が未来の革新を形作る複雑な螺旋状のプロセスであることを強調したい。古代ローマのWi-Fi技術は、人類の知的好奇心と問題解決能力の驚くべき証明であり、私たちに未来への希望と可能性を示唆している。技術は常に変化し、進化し続けるが、根本的な人間の創造性と適応力は、どの時代においても変わることのない原動力なのである。",
            "graphs": [
                {
                "id": "GRAPH_MODERN_APPLICATION",
                "figure_width": 6.5,
                "figure_height": 4.5,
                "title": "古代技術の現代応用",
                "xlabel": "応用分野",
                "ylabel": "潜在的影響力",
                "grid": True,
                "legend": True,
                "charts": [
                    {
                    "chart_type": "bar",
                    "categories": [
                        "通信技術",
                        "エネルギー効率",
                        "情報セキュリティ",
                        "社会システム"
                    ],
                    "values": [
                        90,
                        75,
                        60,
                        85
                    ],
                    "colors": [
                        "blue",
                        "green",
                        "red",
                        "purple"
                    ]
                    }
                ]
                }
            ],
            "tables": [],
            "formulas": [
                {
                "id": "FORMULA_TECHNOLOGICAL_APPLICATION",
                "latex_code": "A_{t} = \\frac{I_{p} \\cdot E_{f}}{R_{l} \\cdot \\sqrt{C_{d}}}",
                "description": "技術応用の潜在的影響力モデル",
                "parameters": [
                    {
                    "symbol": "A_{t}",
                    "description": "技術応用の影響力"
                    },
                    {
                    "symbol": "I_{p}",
                    "description": "イノベーションの潜在力"
                    },
                    {
                    "symbol": "E_{f}",
                    "description": "効率性"
                    },
                    {
                    "symbol": "R_{l}",
                    "description": "リソースの制限"
                    },
                    {
                    "symbol": "C_{d}",
                    "description": "複雑さの次元"
                    }
                ]
                }
            ]
            }
        ],
        "title_name": "結論"
        }
    ]
    return {
        'statusCode': 200,
        'body': {
            "workflow_id" : workflow_id,
            "title" : title,
            "abstract" : "本研究は、古代ローマ帝国の驚くべき通信技術に焦点を当て、その革新的な「光学Wi-Fiネットワーク」の実態を明らかにした。山頂に設置された特殊な反射鏡と光学信号塔を用いて、彼らは数百キロメートルにわたって複雑な情報を伝達する驚異的な通信システムを構築していた。\n\nこの技術は、単なる歴史的な興味にとどまらず、現代の通信技術に多大な影響を与えている。特に、IoTや無線通信の基本的な概念に驚くほど近い技術的アプローチを示しており、技術の進歩が直線的ではなく、螺旋状に発展することを明確に示している。\n\n研究を通じて、限られたリソースの中で創造的な解決策を生み出す古代ローマ帝国の知恵が浮き彫りになった。彼らの通信技術は、人類の知的好奇心と問題解決能力の驚くべき証明であり、過去の知恵が未来の技術革新を導く可能性を示唆している。\n\n最終的に、本研究は技術の本質が人間の創造性と適応力にあることを強調し、どの時代においても変わることのない人類の知的潜在力を明らかにした。",
            "sections_format" : sections_format
        }
    }

    try:
        # eventパラメータ
        workflow_id = event.get("workflow_id")
        title = event.get("title")  
        system_prompt = event.get("system_prompt")  
        sections_format = event.get("sections_format")
        sections = sections_format.get("sections")

        # 生成AIからのレスポンスを保持するリスト
        response_format = []

        # 会話のやり取りを保持するリスト
        messages = []
        for idx, section in enumerate(sections):
            section_title = section["title_name"]
            print(f"====== セクション: {section_title} ======")

            # 最後のセクションかどうかを判定
            is_last = (idx == len(sections_format) - 1)

            # 各セクションのプロンプトを準備
            content_text = json.dumps(section, ensure_ascii=False)

            # 最終セクションの場合、締めくくりの言葉を追加
            if is_last:
                closing_statement = "フォーマット内のテキストの最終行にこの研究の結論をまとめるような締めの文章を作成してフォーマット内に挿入してほしいです。\n"
                closing_statement += "[優先事項]さらにあえてひとつこのセクションではgraphs, tables, formulas データのスキーマバリデーションが引っかかるようにわざとデータをスキーマに合わないようにしてほしいです。"
                content_text += f"\n\n{closing_statement}"

            # プロンプトを追加
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": content_text
                        }
                    ]
                }
            )

            # 最近2件のユーザーメッセージのみキャッシュコントロールを有効化する
            result = []
            user_turns_processed = 0
            for message in reversed(messages):
                if message["role"] == "user" and user_turns_processed < 2:
                    result.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": message["content"][0]["text"],
                                "cache_control": {"type": "ephemeral"}
                            }
                        ]
                    })
                    user_turns_processed += 1
                else:
                    result.append(message)

            # 順番を下に戻す
            messages_to_send = list(reversed(result))

            # 生成AI API呼び出し（前の返答も含める）
            assistant_response = client.call_message_request(system_prompt=system_prompt, messages=messages_to_send)
            logger.info(f"Assistant Response: {assistant_response}")

            response_format.append(json.loads(assistant_response))

            messages.append({
                "role" : "assistant",
                "content" : assistant_response
            })
        
        # 論文のまとめ要旨作成
        abstract_prompt = "生成してくれた各セクションを簡潔にまとめた論文の要旨文章をテキスト形式で作成してください。文字数は300文字以上600文字以下で内容を簡潔にまとめたものにしてください。レスポンスは必ずjson形式でなく改行コードを含めたテキスト形式にしてください。" 
        print(f"====== 要旨 ======")
        messages.append(
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "text",
                        "text" : abstract_prompt
                    }
                ]
            }
        )

        abstract_response = client.call_message_request(system_prompt=abstract_prompt, messages=messages)
        logger.info(f"Assistant Response: {abstract_response}")
        
        # 分かりやすいようにS3に保存
        # upload_to_s3(bucket_name="fake-thesis-bucket",object_key=f"{workflow_id}/responses.json",data=json.dumps({
        #     "title" : title,
        #     "abstract" : abstract_response,
        #     "sections_format" : response_format
        # }, ensure_ascii=False))

    # except anthropic.APIConnectionError as e:
    #     logger.exception("The server could not be reached")

    #     return {
    #         'statusCode': 500,
    #         'body': e   
    #     }
    # except anthropic.RateLimitError as e:
    #     logger.exception("A 429 status code was received; we should back off a bit.")

    #     return {
    #         'statusCode': 429,
    #         'body': e
    #     }
    except Exception as e:
        error = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "payload": event
        }
        logger.exception(error)

        raise e

    return {
        'statusCode': 200,
        'body': {
            "workflow_id" : workflow_id,
            "title" : title,
            "abstract" : abstract_response,
            "sections_format" : response_format
        }
    }
