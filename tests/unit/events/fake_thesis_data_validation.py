# 正常系テスト用のイベントデータ
VALID_EVENT = {
  "workflow_id": "0b2bm093",
  "sections_format": [
    {
      "sub_sections": [
        {
          "title_name": "目的と仮説",
          "text": "本研究は、知的能力と朝食摂取の関係における驚くべき逆説的な仮説を探求する。従来の栄養学的常識に挑戦し、頭が良い人ほど朝食を意図的に避けている可能性を科学的に検証する。\n\n私たちの仮説は、高い知的能力を持つ個人は、朝食を単なる栄養摂取の機会としてではなく、認知的最適化のための戦略的な選択肢として捉えているというものである。これは、伝統的な『朝食は一日の最も重要な食事』という概念に真っ向から挑戦する革新的な視点である。\n\n具体的には、以下の3つの主要な研究仮説を設定した：\n\n1. 高いIQを持つ個人は、朝食を意図的にスキップする傾向がある。\n2. 朝食を摂取しない人は、より創造的で柔軟な思考パターンを示す。\n3. 空腹状態が認知的パフォーマンスを向上させる可能性がある。\n\n[INSERT_FORMULA_HYPOTHESIS_CORE]",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_HYPOTHESIS_CORE",
              "latex_code": "H_{intelligence} = f(breakfast_{skipped})",
              "description": "知性と朝食スキップの関係を表す仮説関数",
              "parameters": [
                {
                  "symbol": "H_{intelligence}",
                  "description": "知性レベル"
                },
                {
                  "symbol": "breakfast_{skipped}",
                  "description": "朝食をスキップした回数または頻度"
                }
              ]
            }
          ]
        },
        {
          "title_name": "仮説や理論の背景",
          "text": "本研究の理論的背景は、認知科学と栄養学の交差点に位置する斬新な領域を開拓するものである。従来の研究は、朝食の重要性を栄養学的観点から単純に評価してきたが、我々は認知的パフォーマンスの複雑な力学に焦点を当てている。\n\n歴史的に、多くの天才や革新的思想家は、伝統的な食事パターンから逸脱してきた。アインシュタイン、ニーチェ、ダ・ヴィンチなどの偉大な知性は、しばしば通常の食事リズムから外れた生活を送っていた。これは単なる偶然ではなく、認知的最適化の戦略的選択である可能性がある。\n\n神経科学的観点から、空腹状態は脳の代謝を変化させ、より集中力が高まり、創造的思考を促進する可能性がある。これは、進化論的な生存戦略と関連している可能性がある。原始的な環境では、食料が不足している状況で最も創造的で柔軟な思考が生存に有利に働いたのではないだろうか。\n\n[INSERT_FORMULA_COGNITIVE_PERFORMANCE]",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_COGNITIVE_PERFORMANCE",
              "latex_code": "CP = \\alpha \\cdot (1 - \\beta \\cdot nutrition_{intake})",
              "description": "認知的パフォーマンスと栄養摂取の関係を示す仮説的関数",
              "parameters": [
                {
                  "symbol": "CP",
                  "description": "認知的パフォーマンス"
                },
                {
                  "symbol": "\\alpha",
                  "description": "基礎認知能力係数"
                },
                {
                  "symbol": "\\beta",
                  "description": "栄養摂取の認知パフォーマンス抑制係数"
                },
                {
                  "symbol": "nutrition_{intake}",
                  "description": "栄養摂取量"
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
          "title_name": "実験の設計と実施方法",
          "text": "本研究における実験設計は、従来の栄養学的研究パラダイムを根本的に覆す革新的なアプローチを採用した。参加者の知的能力と朝食摂取パターンの関係を徹底的に検証するため、多角的で複雑な方法論を開発した。\n\n研究対象は、20〜45歳の高学歴専門家500名（IQ130以上）とし、厳密な選抜基準を設けた。参加者は以下の4つのグループに無作為に分類された：\n\n1. 完全朝食摂取グループ\n2. 部分的朝食摂取グループ\n3. 朝食完全スキップグループ\n4. 間欠的断食グループ\n\n各グループの認知的パフォーマンスを、以下の指標で評価した：\n- 創造性テスト\n- 問題解決能力評価\n- 集中力測定\n- 感情的知性スケール\n\n[INSERT_FORMULA_EXPERIMENTAL_DESIGN]\n\n実験期間は12週間とし、毎週詳細な認知機能評価と生理学的パラメータの測定を実施した。特に注目したのは、朝食摂取パターンが脳の可塑性と認知的柔軟性にどのように影響するかである。",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_EXPERIMENTAL_DESIGN",
              "latex_code": "CP_{total} = \\sum_{i=1}^{n} (w_i \\cdot CP_i)",
              "description": "総合認知パフォーマンスの計算式",
              "parameters": [
                {
                  "symbol": "CP_{total}",
                  "description": "総合認知パフォーマンススコア"
                },
                {
                  "symbol": "w_i",
                  "description": "各認知指標の重み係数"
                },
                {
                  "symbol": "CP_i",
                  "description": "個別認知パフォーマンス指標"
                },
                {
                  "symbol": "n",
                  "description": "評価指標の総数"
                }
              ]
            }
          ]
        },
        {
          "title_name": "使用したツール・技術・データセット",
          "text": "本研究では、最先端のテクノロジーと高度な分析ツールを駆使し、前例のない精密さで実験を遂行した。データ収集と分析には、以下の革新的なツールと技術を採用した：\n\n認知機能評価ツール：\n1. NeuroTracker Pro 3000 - リアルタイム脳機能マッピングシステム\n2. CogniMetrix AI - 機械学習ベースの認知パフォーマンス分析プラットフォーム\n3. EmotionSense ヘッドセット - 感情的反応と生理学的変化の同時計測デバイス\n\nデータ分析技術：\n- 量子機械学習アルゴリズム\n- ベイズ推論モデル\n- 多変量解析手法\n\n[INSERT_TABLE_RESEARCH_TOOLS]\n\n特筆すべきは、我々が開発した独自のアルゴリズム「BreakfastBrain AI」である。このシステムは、朝食摂取パターンと認知機能の複雑な相互作用を高精度で分析可能にした。\n\n[INSERT_FORMULA_DATA_ANALYSIS]",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_RESEARCH_TOOLS",
              "table_type": "basic",
              "title": "研究で使用した主要ツールと技術",
              "columns": ["カテゴリ", "ツール名", "主な機能"],
              "rows": [
                [
                  "認知機能評価",
                  "NeuroTracker Pro 3000",
                  "リアルタイム脳機能マッピング"
                ],
                [
                  "AI分析",
                  "CogniMetrix AI",
                  "機械学習による認知パフォーマンス分析"
                ],
                [
                  "感情センシング",
                  "EmotionSense ヘッドセット",
                  "生理学的・感情的反応計測"
                ],
                ["データ解析", "BreakfastBrain AI", "朝食と認知機能の相関分析"]
              ],
              "style": {
                "header_bg_color": "#4A90E2",
                "header_font_color": "white",
                "cell_bg_color": "#F0F8FF",
                "cell_font_color": "black",
                "border_color": "#B0C4DE",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_DATA_ANALYSIS",
              "latex_code": "R_{cognitive} = \\frac{\\sum_{j=1}^{m} (x_j \\cdot w_j)}{\\sigma_{breakfast}}",
              "description": "認知的相関係数の計算式",
              "parameters": [
                {
                  "symbol": "R_{cognitive}",
                  "description": "認知的相関係数"
                },
                {
                  "symbol": "x_j",
                  "description": "各認知指標の値"
                },
                {
                  "symbol": "w_j",
                  "description": "各指標の重み"
                },
                {
                  "symbol": "\\sigma_{breakfast}",
                  "description": "朝食摂取パターンの標準偏差"
                },
                {
                  "symbol": "m",
                  "description": "認知指標の総数"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "方法論"
    },
    {
      "sub_sections": [
        {
          "title_name": "実験結果の詳細",
          "text": "本研究における実験結果は、従来の栄養学的常識を根本から覆す驚くべき知見をもたらした。500名の高IQ専門家を対象とした12週間の綿密な調査から、朝食と知的能力の間に予想外の相関関係が明らかになった。\n\n主要な発見は以下の通りである：\n\n1. 朝食をスキップするグループは、他のグループと比較して：\n   - 創造性テストのスコアが平均23.7%高い\n   - 問題解決能力が15.4%向上\n   - 集中力持続時間が約20%延長\n\n2. 興味深いことに、完全な朝食摂取グループは最も低い認知的柔軟性を示した。\n\n3. 間欠的断食グループは、最も安定した認知パフォーマンスを記録した。\n\n[INSERT_GRAPH_COGNITIVE_PERFORMANCE]\n\n[INSERT_FORMULA_RESULT_CORRELATION]\n\n驚くべきことに、朝食をスキップする習慣は、単なる食事の選択を超えて、脳の認知的最適化メカニズムと深く関連していることが示唆された。",
          "graphs": [
            {
              "id": "GRAPH_COGNITIVE_PERFORMANCE",
              "title": "朝食摂取パターン別認知パフォーマンス比較",
              "xlabel": "朝食摂取グループ",
              "ylabel": "認知パフォーマンススコア",
              "grid": True,
              "legend": True,
              "charts": [
                {
                  "chart_type": "bar",
                  "categories": [
                    "完全摂取",
                    "部分摂取",
                    "スキップ",
                    "間欠的断食"
                  ],
                  "values": [65, 72, 85, 80],
                  "colors": ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
                }
              ]
            }
          ],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_RESULT_CORRELATION",
              "latex_code": "R_{breakfast,intelligence} = \\frac{\\sum_{i=1}^{n} (x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum_{i=1}^{n} (x_i - \\bar{x})^2 \\sum_{i=1}^{n} (y_i - \\bar{y})^2}}",
              "description": "朝食摂取パターンと知性の相関係数計算式",
              "parameters": [
                {
                  "symbol": "R_{breakfast,intelligence}",
                  "description": "朝食摂取と知性の相関係数"
                },
                {
                  "symbol": "x_i",
                  "description": "朝食摂取パターン"
                },
                {
                  "symbol": "y_i",
                  "description": "認知パフォーマンス指標"
                }
              ]
            }
          ]
        },
        {
          "title_name": "得られたデータの分析",
          "text": "データ分析プロセスは、我々の仮説を驚くほど強力に支持する結果をもたらした。多変量解析とAI駆動の統計モデリングにより、朝食と認知機能の複雑な関係性が明らかになった。\n\n主要な分析結果：\n1. 朝食スキップと創造性の正の相関\n2. 空腹状態における脳の代謝効率の向上\n3. 認知的柔軟性と食事パターンの非線形関係\n\n[INSERT_TABLE_STATISTICAL_SUMMARY]\n\n[INSERT_FORMULA_DATA_INTERPRETATION]\n\n本研究は、単なる栄養学的観察を超えて、人間の認知機能と食事習慣の根本的な再解釈を提案するものである。知的能力の高い個人は、直感的に最適な認知状態を追求しており、朝食は必ずしも『一日の最も重要な食事』ではない可能性を示唆している。\n\n最終的に、この研究は従来の常識に挑戦し、個人の認知的潜在能力を最大化するための新たな視点を提供するものとなった。私たちの発見は、食事と知性の関係における既存のパラダイムを根本から覆す可能性を秘めており、今後の学際的研究への重要な示唆を含んでいる。",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_STATISTICAL_SUMMARY",
              "table_type": "summary",
              "title": "朝食摂取パターン別認知指標統計サマリー",
              "statistics": {
                "創造性スコア": {
                  "mean": 78.5,
                  "median": 77.2,
                  "std": 12.3,
                  "min": 55,
                  "max": 95
                },
                "問題解決能力": {
                  "mean": 82.1,
                  "median": 80.6,
                  "std": 10.7,
                  "min": 60,
                  "max": 98
                },
                "集中力持続時間": {
                  "mean": 45.6,
                  "median": 44.2,
                  "std": 8.9,
                  "min": 30,
                  "max": 60
                }
              },
              "style": {
                "header_bg_color": "#4CAF50",
                "header_font_color": "white",
                "cell_bg_color": "#E8F5E9",
                "cell_font_color": "black",
                "border_color": "#81C784",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_DATA_INTERPRETATION",
              "latex_code": "I_{cognitive} = f(breakfast_{pattern}, t)",
              "description": "時間経過における認知能力と朝食パターンの関係関数",
              "parameters": [
                {
                  "symbol": "I_{cognitive}",
                  "description": "認知能力指標"
                },
                {
                  "symbol": "breakfast_{pattern}",
                  "description": "朝食摂取パターン"
                },
                {
                  "symbol": "t",
                  "description": "時間"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "結果"
    },
    {
      "sub_sections": [
        {
          "title_name": "結果に対する解釈",
          "text": "本研究の結果は、人間の認知機能と食事習慣の関係における従来の常識に根本的な疑問を投げかける。朝食をスキップする行動が、単なる栄養摂取の回避ではなく、高度な認知的最適化戦略である可能性を強く示唆している。\n\n我々の解釈によれば、空腹状態は脳に『生存モード』を起動させ、より効率的で創造的な思考プロセスを誘発する。これは進化論的な観点から説明可能で、食料が限られた環境で生存するために必要とされた認知的柔軟性の名残と考えられる。\n\n[INSERT_FORMULA_COGNITIVE_INTERPRETATION]\n\n特に注目すべき点は、朝食スキップグループの創造性と問題解決能力の顕著な向上である。これは、従来の栄養学的パラダイムでは説明不可能な現象であり、脳の代謝メカニズムの新たな理解を要求するものである。",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_COGNITIVE_INTERPRETATION",
              "latex_code": "C_{creativity} = \\alpha \\cdot (1 - \\beta \\cdot nutrition_{intake})",
              "description": "創造性と栄養摂取の非線形関係を示す解釈関数",
              "parameters": [
                {
                  "symbol": "C_{creativity}",
                  "description": "創造性レベル"
                },
                {
                  "symbol": "\\alpha",
                  "description": "基礎創造性係数"
                },
                {
                  "symbol": "\\beta",
                  "description": "栄養摂取の創造性抑制係数"
                },
                {
                  "symbol": "nutrition_{intake}",
                  "description": "栄養摂取量"
                }
              ]
            }
          ]
        },
        {
          "title_name": "仮説と実験結果の一致/不一致",
          "text": "我々の当初の仮説は、驚くべきことに実験結果によって部分的に支持され、同時に予想外の側面も明らかになった。\n\n一致した仮説：\n1. 高IQを持つ個人の朝食スキップ傾向\n2. 空腹状態における認知的柔軟性の向上\n\n予想外の発見：\n1. 間欠的断食グループの驚くべき安定した認知パフォーマンス\n2. 創造性スコアの予想以上の変動\n\n[INSERT_GRAPH_HYPOTHESIS_COMPARISON]\n\n特に興味深いのは、我々の仮説が完全に正確であったわけではなく、むしろ複雑な生理学的メカニズムの存在を示唆したことである。単純な『朝食をスキップすれば頭が良くなる』という単純な結論は避けるべきであり、個人の生理学的特性と認知的メカニズムの複雑さを強調する必要がある。",
          "graphs": [
            {
              "id": "GRAPH_HYPOTHESIS_COMPARISON",
              "title": "仮説と実験結果の比較",
              "xlabel": "仮説要素",
              "ylabel": "支持レベル",
              "grid": True,
              "legend": True,
              "charts": [
                {
                  "chart_type": "bar",
                  "categories": [
                    "IQ相関",
                    "創造性向上",
                    "認知的柔軟性",
                    "間欠的断食効果"
                  ],
                  "values": [85, 75, 70, 90],
                  "colors": ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
                }
              ]
            }
          ],
          "tables": [],
          "formulas": []
        },
        {
          "title_name": "実験の限界・誤差・改善点",
          "text": "科学的誠実性を保つため、本研究の限界と潜在的な改善点を率直に認識することが重要である。\n\n実験の主な限界：\n1. サンプルサイズの制限（500名）\n2. 地理的・文化的バイアスの可能性\n3. 長期的影響の未検証\n4. 個人の代謝差異の考慮不足\n\n[INSERT_TABLE_EXPERIMENTAL_LIMITATIONS]\n\n将来の研究に向けた具体的な改善提案：\n- より大規模で多様なサンプル集団の採用\n- 遺伝的背景と代謝メカニズムのさらなる分析\n- 長期追跡調査の実施\n- 個別化された栄養・認知パフォーマンスモデルの開発\n\n[INSERT_FORMULA_ERROR_ANALYSIS]\n\n最終的に、この研究は完璧な結論ではなく、人間の認知機能と食事習慣の複雑な関係を探求するための重要な一歩である。科学は常に進化し、新たな疑問を生み出すものであり、我々の研究もその精神に忠実であることを目指している。",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_EXPERIMENTAL_LIMITATIONS",
              "table_type": "basic",
              "title": "実験の主要な限界と潜在的バイアス",
              "columns": ["カテゴリ", "具体的制限", "影響度"],
              "rows": [
                ["サンプルサイズ", "500名の限定的な参加者", "中"],
                ["地理的バイアス", "特定地域への集中", "高"],
                ["長期影響", "12週間の短期研究", "高"],
                ["個人差", "代謝メカニズムの個人差未考慮", "中"]
              ],
              "style": {
                "header_bg_color": "#FF6B6B",
                "header_font_color": "white",
                "cell_bg_color": "#FFF5F5",
                "cell_font_color": "black",
                "border_color": "#FF9999",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_ERROR_ANALYSIS",
              "latex_code": "\\epsilon_{total} = \\sqrt{\\sum_{i=1}^{n} (\\sigma_i^2 \\cdot w_i)}",
              "description": "実験全体の潜在的誤差を計算する関数",
              "parameters": [
                {
                  "symbol": "\\epsilon_{total}",
                  "description": "総合誤差"
                },
                {
                  "symbol": "\\sigma_i",
                  "description": "各要因の標準偏差"
                },
                {
                  "symbol": "w_i",
                  "description": "各要因の重み係数"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "考察"
    },
    {
      "sub_sections": [
        {
          "title_name": "仮説の検証結果",
          "text": "本研究は、「頭いい人ほど朝食を食べない」という挑戦的な仮説を科学的に検証し、驚くべき知見をもたらした。我々の主要な仮説は、以下のように部分的に支持され、同時に新たな科学的疑問を提起した。\n\n仮説検証の詳細：\n1. 高IQ個人の朝食スキップ傾向：強く支持\n   - 朝食をスキップするグループは、認知的柔軟性で有意に高いスコアを示した\n\n2. 空腹状態と創造的思考の関係：部分的に支持\n   - 空腹時の脳は、より効率的で創造的な思考モードに移行する可能性が示唆された\n\n3. 認知的パフォーマンスと食事パターンの非線形関係：完全に支持\n   - 単純な栄養摂取モデルでは説明できない複雑な相互作用が明らかになった\n\n[INSERT_FORMULA_HYPOTHESIS_VERIFICATION]\n\n[INSERT_GRAPH_HYPOTHESIS_SUPPORT]\n\n重要な点は、我々の研究が従来の栄養学的パラダイムに根本的な疑問を投げかけ、知性と食事習慣の関係における新たな理解の扉を開いたことである。",
          "graphs": [
            {
              "id": "GRAPH_HYPOTHESIS_SUPPORT",
              "title": "仮説検証の支持レベル",
              "xlabel": "仮説要素",
              "ylabel": "支持度(%)",
              "grid": True,
              "legend": True,
              "charts": [
                {
                  "chart_type": "bar",
                  "categories": [
                    "IQ・朝食スキップ",
                    "空腹と創造性",
                    "認知パフォーマンス"
                  ],
                  "values": [85, 72, 90],
                  "colors": ["#3498db", "#2ecc71", "#e74c3c"]
                }
              ]
            }
          ],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_HYPOTHESIS_VERIFICATION",
              "latex_code": "H_{verification} = \\frac{\\sum_{i=1}^{n} (x_i \\cdot w_i)}{\\sigma_{total}}",
              "description": "仮説検証の総合的支持度を計算する関数",
              "parameters": [
                {
                  "symbol": "H_{verification}",
                  "description": "仮説検証の総合支持度"
                },
                {
                  "symbol": "x_i",
                  "description": "各仮説要素の支持レベル"
                },
                {
                  "symbol": "w_i",
                  "description": "各要素の重み係数"
                },
                {
                  "symbol": "\\sigma_{total}",
                  "description": "総合変動"
                }
              ]
            }
          ]
        },
        {
          "title_name": "今後の研究方向性",
          "text": "本研究は、人間の認知機能と食事習慣の関係における新たな研究フロンティアを開拓した。今後の研究は、以下の重要な方向性に焦点を当てるべきである。\n\n将来の研究アジェンダ：\n1. 遺伝的背景と認知パフォーマンスの相互作用\n   - 個人の遺伝子型と食事パターンの関係性の詳細な解析\n\n2. 長期的認知影響の追跡研究\n   - 10年以上の縦断的研究による持続的影響の評価\n\n3. 神経科学的メカニズムの解明\n   - 空腹状態が脳の代謝と神経可塑性に与える詳細な影響\n\n[INSERT_TABLE_FUTURE_RESEARCH_DIRECTIONS]\n\n[INSERT_FORMULA_RESEARCH_POTENTIAL]\n\n特に注目すべき研究領域：\n- 個別化された認知最適化戦略の開発\n- 食事パターンと脳の可塑性の関係\n- 認知的パフォーマンスの新たな測定法の確立\n\n最終的に、この研究は単なる終着点ではなく、人間の認知機能に対する理解を深める旅の重要な通過点である。私たちの発見は、知性、栄養、そして人間の潜在能力の複雑な相互作用に対する新たな視点を提供し、未来の学際的研究への重要な基盤を築いたと言えるだろう。",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_FUTURE_RESEARCH_DIRECTIONS",
              "table_type": "basic",
              "title": "今後の研究における主要な方向性",
              "columns": ["研究領域", "主要な焦点", "予想される課題"],
              "rows": [
                [
                  "遺伝的解析",
                  "認知能力と食事パターンの遺伝的基盤",
                  "複雑な遺伝的相互作用"
                ],
                ["長期追跡", "10年以上の認知影響評価", "継続的なデータ収集"],
                [
                  "神経科学",
                  "空腹状態の脳メカニズム",
                  "複雑な神経生理学的測定"
                ],
                ["個別化戦略", "個人最適化された認知強化", "高度な個人差の考慮"]
              ],
              "style": {
                "header_bg_color": "#4A90E2",
                "header_font_color": "white",
                "cell_bg_color": "#E6F2FF",
                "cell_font_color": "black",
                "border_color": "#7BC9FF",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_RESEARCH_POTENTIAL",
              "latex_code": "P_{research} = f(\\vec{x}, t, \\sigma_{individual})",
              "description": "研究の将来的可能性を表す多変数関数",
              "parameters": [
                {
                  "symbol": "P_{research}",
                  "description": "研究の潜在的可能性"
                },
                {
                  "symbol": "\\vec{x}",
                  "description": "研究変数ベクトル"
                },
                {
                  "symbol": "t",
                  "description": "時間パラメータ"
                },
                {
                  "symbol": "\\sigma_{individual}",
                  "description": "個人差の変動"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "結論"
    }
  ],
  "abstract": "本研究は、知的能力と朝食摂取パターンの関係における革新的な探求を行った。500名の高IQ専門家を対象とした12週間の実験により、従来の栄養学的常識に挑戦する驚くべき知見が得られた。\n\n朝食をスキップするグループは、創造性テストで23.7%高いスコアを示し、問題解決能力も15.4%向上した。特に興味深いのは、空腹状態が脳の認知的柔軟性を高める可能性を示唆したことである。間欠的断食グループは最も安定した認知パフォーマンスを記録し、単なる食事習慣を超えた脳の最適化メカニズムの存在を示唆した。\n\n研究は、高い知性を持つ個人が直感的に最適な認知状態を追求していることを明らかにし、「朝食は一日の最も重要な食事」という従来の概念に根本的な疑問を投げかけた。今後は、遺伝的背景や長期的影響の解明に向けた更なる研究が期待される。",
  "title": "頭いい人ほど朝食を食べない"
}


# LaTeXバリデーション異常系テスト用のイベントデータ
INVALID_DATA_EVENT = {
  "workflow_id": "0b2bm093",
  "sections_format": [
    {
      "sub_sections": [
        {
          "title_name": "目的と仮説",
          "text": "本研究は、知的能力と朝食摂取の関係における驚くべき逆説的な仮説を探求する。従来の栄養学的常識に挑戦し、頭が良い人ほど朝食を意図的に避けている可能性を科学的に検証する。\n\n私たちの仮説は、高い知的能力を持つ個人は、朝食を単なる栄養摂取の機会としてではなく、認知的最適化のための戦略的な選択肢として捉えているというものである。これは、伝統的な『朝食は一日の最も重要な食事』という概念に真っ向から挑戦する革新的な視点である。\n\n具体的には、以下の3つの主要な研究仮説を設定した：\n\n1. 高いIQを持つ個人は、朝食を意図的にスキップする傾向がある。\n2. 朝食を摂取しない人は、より創造的で柔軟な思考パターンを示す。\n3. 空腹状態が認知的パフォーマンスを向上させる可能性がある。\n\n[INSERT_FORMULA_HYPOTHESIS_CORE]",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_HYPOTHESIS_CORE",
              "latex_code": "H_{intelligence} = f(breakfast_{skipped})",
              "description": "知性と朝食スキップの関係を表す仮説関数",
              "parameters": [
                {
                  "symbol": "H_{intelligence}",
                  "description": "知性レベル"
                },
                {
                  "symbol": "breakfast_{skipped}",
                  "description": "朝食をスキップした回数または頻度"
                }
              ]
            }
          ]
        },
        {
          "title_name": "仮説や理論の背景",
          "text": "本研究の理論的背景は、認知科学と栄養学の交差点に位置する斬新な領域を開拓するものである。従来の研究は、朝食の重要性を栄養学的観点から単純に評価してきたが、我々は認知的パフォーマンスの複雑な力学に焦点を当てている。\n\n歴史的に、多くの天才や革新的思想家は、伝統的な食事パターンから逸脱してきた。アインシュタイン、ニーチェ、ダ・ヴィンチなどの偉大な知性は、しばしば通常の食事リズムから外れた生活を送っていた。これは単なる偶然ではなく、認知的最適化の戦略的選択である可能性がある。\n\n神経科学的観点から、空腹状態は脳の代謝を変化させ、より集中力が高まり、創造的思考を促進する可能性がある。これは、進化論的な生存戦略と関連している可能性がある。原始的な環境では、食料が不足している状況で最も創造的で柔軟な思考が生存に有利に働いたのではないだろうか。\n\n[INSERT_FORMULA_COGNITIVE_PERFORMANCE]",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_COGNITIVE_PERFORMANCE",
              "latex_code": "CP = %^&$%^$^tetete\\cdot (1 - \\beta \\cdot nutrition_{intake})",
              "description": "認知的パフォーマンスと栄養摂取の関係を示す仮説的関数",
              "parameters": [
                {
                  "symbol": "CP",
                  "description": "認知的パフォーマンス"
                },
                {
                  "symbol": "\\alpha",
                  "description": "基礎認知能力係数"
                },
                {
                  "symbol": "\\beta",
                  "description": "栄養摂取の認知パフォーマンス抑制係数"
                },
                {
                  "symbol": "nutrition_{intake}",
                  "description": "栄養摂取量"
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
          "title_name": "実験の設計と実施方法",
          "text": "本研究における実験設計は、従来の栄養学的研究パラダイムを根本的に覆す革新的なアプローチを採用した。参加者の知的能力と朝食摂取パターンの関係を徹底的に検証するため、多角的で複雑な方法論を開発した。\n\n研究対象は、20〜45歳の高学歴専門家500名（IQ130以上）とし、厳密な選抜基準を設けた。参加者は以下の4つのグループに無作為に分類された：\n\n1. 完全朝食摂取グループ\n2. 部分的朝食摂取グループ\n3. 朝食完全スキップグループ\n4. 間欠的断食グループ\n\n各グループの認知的パフォーマンスを、以下の指標で評価した：\n- 創造性テスト\n- 問題解決能力評価\n- 集中力測定\n- 感情的知性スケール\n\n[INSERT_FORMULA_EXPERIMENTAL_DESIGN]\n\n実験期間は12週間とし、毎週詳細な認知機能評価と生理学的パラメータの測定を実施した。特に注目したのは、朝食摂取パターンが脳の可塑性と認知的柔軟性にどのように影響するかである。",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_EXPERIMENTAL_DESIGN",
              "latex_code": "CP_{total} = \\sum_{i=1}^{n} (w_i \\cdot CP_i)",
              "description": "総合認知パフォーマンスの計算式",
              "parameters": [
                {
                  "symbol": "CP_{total}",
                  "description": "総合認知パフォーマンススコア"
                },
                {
                  "symbol": "w_i",
                  "description": "各認知指標の重み係数"
                },
                {
                  "symbol": "CP_i",
                  "description": "個別認知パフォーマンス指標"
                },
                {
                  "symbol": "n",
                  "description": "評価指標の総数"
                }
              ]
            }
          ]
        },
        {
          "title_name": "使用したツール・技術・データセット",
          "text": "本研究では、最先端のテクノロジーと高度な分析ツールを駆使し、前例のない精密さで実験を遂行した。データ収集と分析には、以下の革新的なツールと技術を採用した：\n\n認知機能評価ツール：\n1. NeuroTracker Pro 3000 - リアルタイム脳機能マッピングシステム\n2. CogniMetrix AI - 機械学習ベースの認知パフォーマンス分析プラットフォーム\n3. EmotionSense ヘッドセット - 感情的反応と生理学的変化の同時計測デバイス\n\nデータ分析技術：\n- 量子機械学習アルゴリズム\n- ベイズ推論モデル\n- 多変量解析手法\n\n[INSERT_TABLE_RESEARCH_TOOLS]\n\n特筆すべきは、我々が開発した独自のアルゴリズム「BreakfastBrain AI」である。このシステムは、朝食摂取パターンと認知機能の複雑な相互作用を高精度で分析可能にした。\n\n[INSERT_FORMULA_DATA_ANALYSIS]",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_RESEARCH_TOOLS",
              "table_type": "basic",
              "title": "研究で使用した主要ツールと技術",
              "columns": ["カテゴリ", "ツール名", "主な機能"],
              "rows": [
                [
                  "認知機能評価",
                  "NeuroTracker Pro 3000",
                  "リアルタイム脳機能マッピング"
                ],
                [
                  "AI分析",
                  "CogniMetrix AI",
                  "機械学習による認知パフォーマンス分析"
                ],
                [
                  "感情センシング",
                  "EmotionSense ヘッドセット",
                  "生理学的・感情的反応計測"
                ],
                ["データ解析", "BreakfastBrain AI", "朝食と認知機能の相関分析"]
              ],
              "style": {
                "header_bg_color": "#4A90E2",
                "header_font_color": "white",
                "cell_bg_color": "#F0F8FF",
                "cell_font_color": "black",
                "border_color": "#B0C4DE",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_DATA_ANALYSIS",
              "latex_code": "R_{cognitive} = \\frac{\\sum_{j=1}^{m} (x_j \\cdot w_j)}{\\sigma_{breakfast}}",
              "description": "認知的相関係数の計算式",
              "parameters": [
                {
                  "symbol": "R_{cognitive}",
                  "description": "認知的相関係数"
                },
                {
                  "symbol": "x_j",
                  "description": "各認知指標の値"
                },
                {
                  "symbol": "w_j",
                  "description": "各指標の重み"
                },
                {
                  "symbol": "\\sigma_{breakfast}",
                  "description": "朝食摂取パターンの標準偏差"
                },
                {
                  "symbol": "m",
                  "description": "認知指標の総数"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "方法論"
    },
    {
      "sub_sections": [
        {
          "title_name": "実験結果の詳細",
          "text": "本研究における実験結果は、従来の栄養学的常識を根本から覆す驚くべき知見をもたらした。500名の高IQ専門家を対象とした12週間の綿密な調査から、朝食と知的能力の間に予想外の相関関係が明らかになった。\n\n主要な発見は以下の通りである：\n\n1. 朝食をスキップするグループは、他のグループと比較して：\n   - 創造性テストのスコアが平均23.7%高い\n   - 問題解決能力が15.4%向上\n   - 集中力持続時間が約20%延長\n\n2. 興味深いことに、完全な朝食摂取グループは最も低い認知的柔軟性を示した。\n\n3. 間欠的断食グループは、最も安定した認知パフォーマンスを記録した。\n\n[INSERT_GRAPH_COGNITIVE_PERFORMANCE]\n\n[INSERT_FORMULA_RESULT_CORRELATION]\n\n驚くべきことに、朝食をスキップする習慣は、単なる食事の選択を超えて、脳の認知的最適化メカニズムと深く関連していることが示唆された。",
          "graphs": [
            {
              "id": "GRAPH_COGNITIVE_PERFORMANCE",
              "title": "朝食摂取パターン別認知パフォーマンス比較",
              "xlabel": "朝食摂取グループ",
              "ylabel": "認知パフォーマンススコア",
              "grid": True,
              "legend": True,
              "charts": [
                {
                  "chart_type": "bar",
                  "categories": [
                    "完全摂取",
                    "部分摂取",
                    "スキップ",
                    "間欠的断食"
                  ],
                  "values": [65, 72, 85, 80],
                  "colors": ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
                }
              ]
            }
          ],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_RESULT_CORRELATION",
              "latex_code": "R_{breakfast,intelligence} = \\frac{\\sum_{i=1}^{n} (x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum_{i=1}^{n} (x_i - \\bar{x})^2 \\sum_{i=1}^{n} (y_i - \\bar{y})^2}}",
              "description": "朝食摂取パターンと知性の相関係数計算式",
              "parameters": [
                {
                  "symbol": "R_{breakfast,intelligence}",
                  "description": "朝食摂取と知性の相関係数"
                },
                {
                  "symbol": "x_i",
                  "description": "朝食摂取パターン"
                },
                {
                  "symbol": "y_i",
                  "description": "認知パフォーマンス指標"
                }
              ]
            }
          ]
        },
        {
          "title_name": "得られたデータの分析",
          "text": "データ分析プロセスは、我々の仮説を驚くほど強力に支持する結果をもたらした。多変量解析とAI駆動の統計モデリングにより、朝食と認知機能の複雑な関係性が明らかになった。\n\n主要な分析結果：\n1. 朝食スキップと創造性の正の相関\n2. 空腹状態における脳の代謝効率の向上\n3. 認知的柔軟性と食事パターンの非線形関係\n\n[INSERT_TABLE_STATISTICAL_SUMMARY]\n\n[INSERT_FORMULA_DATA_INTERPRETATION]\n\n本研究は、単なる栄養学的観察を超えて、人間の認知機能と食事習慣の根本的な再解釈を提案するものである。知的能力の高い個人は、直感的に最適な認知状態を追求しており、朝食は必ずしも『一日の最も重要な食事』ではない可能性を示唆している。\n\n最終的に、この研究は従来の常識に挑戦し、個人の認知的潜在能力を最大化するための新たな視点を提供するものとなった。私たちの発見は、食事と知性の関係における既存のパラダイムを根本から覆す可能性を秘めており、今後の学際的研究への重要な示唆を含んでいる。",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_STATISTICAL_SUMMARY",
              "table_type": "summary",
              "title": "朝食摂取パターン別認知指標統計サマリー",
              "statistics": {
                "創造性スコア": {
                  "mean": 78.5,
                  "median": 77.2,
                  "std": 12.3,
                  "min": 55,
                  "max": 95
                },
                "問題解決能力": {
                  "mean": 82.1,
                  "median": 80.6,
                  "std": 10.7,
                  "min": 60,
                  "max": 98
                },
                "集中力持続時間": {
                  "mean": 45.6,
                  "median": 44.2,
                  "std": 8.9,
                  "min": 30,
                  "max": 60
                }
              },
              "style": {
                "header_bg_color": "#4CAF50",
                "header_font_color": "white",
                "cell_bg_color": "#E8F5E9",
                "cell_font_color": "black",
                "border_color": "#81C784",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_DATA_INTERPRETATION",
              "latex_code": "I_{cognitive} = f(breakfast_{pattern}, t)",
              "description": "時間経過における認知能力と朝食パターンの関係関数",
              "parameters": [
                {
                  "symbol": "I_{cognitive}",
                  "description": "認知能力指標"
                },
                {
                  "symbol": "breakfast_{pattern}",
                  "description": "朝食摂取パターン"
                },
                {
                  "symbol": "t",
                  "description": "時間"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "結果"
    },
    {
      "sub_sections": [
        {
          "title_name": "結果に対する解釈",
          "text": "本研究の結果は、人間の認知機能と食事習慣の関係における従来の常識に根本的な疑問を投げかける。朝食をスキップする行動が、単なる栄養摂取の回避ではなく、高度な認知的最適化戦略である可能性を強く示唆している。\n\n我々の解釈によれば、空腹状態は脳に『生存モード』を起動させ、より効率的で創造的な思考プロセスを誘発する。これは進化論的な観点から説明可能で、食料が限られた環境で生存するために必要とされた認知的柔軟性の名残と考えられる。\n\n[INSERT_FORMULA_COGNITIVE_INTERPRETATION]\n\n特に注目すべき点は、朝食スキップグループの創造性と問題解決能力の顕著な向上である。これは、従来の栄養学的パラダイムでは説明不可能な現象であり、脳の代謝メカニズムの新たな理解を要求するものである。",
          "graphs": [],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_COGNITIVE_INTERPRETATION",
              "latex_code": "C_{creativity} = \\alpha \\cdot (1 - \\beta \\cdot nutrition_{intake})",
              "description": "創造性と栄養摂取の非線形関係を示す解釈関数",
              "parameters": [
                {
                  "symbol": "C_{creativity}",
                  "description": "創造性レベル"
                },
                {
                  "symbol": "\\alpha",
                  "description": "基礎創造性係数"
                },
                {
                  "symbol": "\\beta",
                  "description": "栄養摂取の創造性抑制係数"
                },
                {
                  "symbol": "nutrition_{intake}",
                  "description": "栄養摂取量"
                }
              ]
            }
          ]
        },
        {
          "title_name": "仮説と実験結果の一致/不一致",
          "text": "我々の当初の仮説は、驚くべきことに実験結果によって部分的に支持され、同時に予想外の側面も明らかになった。\n\n一致した仮説：\n1. 高IQを持つ個人の朝食スキップ傾向\n2. 空腹状態における認知的柔軟性の向上\n\n予想外の発見：\n1. 間欠的断食グループの驚くべき安定した認知パフォーマンス\n2. 創造性スコアの予想以上の変動\n\n[INSERT_GRAPH_HYPOTHESIS_COMPARISON]\n\n特に興味深いのは、我々の仮説が完全に正確であったわけではなく、むしろ複雑な生理学的メカニズムの存在を示唆したことである。単純な『朝食をスキップすれば頭が良くなる』という単純な結論は避けるべきであり、個人の生理学的特性と認知的メカニズムの複雑さを強調する必要がある。",
          "graphs": [
            {
              "id": "GRAPH_HYPOTHESIS_COMPARISON",
              "title": "仮説と実験結果の比較",
              "xlabel": "仮説要素",
              "ylabel": "支持レベル",
              "grid": True,
              "legend": True,
              "charts": [
                {
                  "chart_type": "bar",
                  "categories": [
                    "IQ相関",
                    "創造性向上",
                    "認知的柔軟性",
                    "間欠的断食効果"
                  ],
                  "values": [85, 75, 70, 90],
                  "colors": ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
                }
              ]
            }
          ],
          "tables": [],
          "formulas": []
        },
        {
          "title_name": "実験の限界・誤差・改善点",
          "text": "科学的誠実性を保つため、本研究の限界と潜在的な改善点を率直に認識することが重要である。\n\n実験の主な限界：\n1. サンプルサイズの制限（500名）\n2. 地理的・文化的バイアスの可能性\n3. 長期的影響の未検証\n4. 個人の代謝差異の考慮不足\n\n[INSERT_TABLE_EXPERIMENTAL_LIMITATIONS]\n\n将来の研究に向けた具体的な改善提案：\n- より大規模で多様なサンプル集団の採用\n- 遺伝的背景と代謝メカニズムのさらなる分析\n- 長期追跡調査の実施\n- 個別化された栄養・認知パフォーマンスモデルの開発\n\n[INSERT_FORMULA_ERROR_ANALYSIS]\n\n最終的に、この研究は完璧な結論ではなく、人間の認知機能と食事習慣の複雑な関係を探求するための重要な一歩である。科学は常に進化し、新たな疑問を生み出すものであり、我々の研究もその精神に忠実であることを目指している。",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_EXPERIMENTAL_LIMITATIONS",
              "table_type": "basic",
              "title": "実験の主要な限界と潜在的バイアス",
              "columns": ["カテゴリ", "具体的制限", "影響度"],
              "rows": [
                ["サンプルサイズ", "500名の限定的な参加者", "中"],
                ["地理的バイアス", "特定地域への集中", "高"],
                ["長期影響", "12週間の短期研究", "高"],
                ["個人差", "代謝メカニズムの個人差未考慮", "中"]
              ],
              "style": {
                "header_bg_color": "#FF6B6B",
                "header_font_color": "white",
                "cell_bg_color": "#FFF5F5",
                "cell_font_color": "black",
                "border_color": "#FF9999",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_ERROR_ANALYSIS",
              "latex_code": "\\epsilon_{total} = \\sqrt{\\sum_{i=1}^{n} (\\sigma_i^2 \\cdot w_i))",
              "description": "実験全体の潜在的誤差を計算する関数",
              "parameters": [
                {
                  "symbol": "\\epsilon_{total}",
                  "description": "総合誤差"
                },
                {
                  "symbol": "\\sigma_i",
                  "description": "各要因の標準偏差"
                },
                {
                  "symbol": "w_i",
                  "description": "各要因の重み係数"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "考察"
    },
    {
      "sub_sections": [
        {
          "title_name": "仮説の検証結果",
          "text": "本研究は、「頭いい人ほど朝食を食べない」という挑戦的な仮説を科学的に検証し、驚くべき知見をもたらした。我々の主要な仮説は、以下のように部分的に支持され、同時に新たな科学的疑問を提起した。\n\n仮説検証の詳細：\n1. 高IQ個人の朝食スキップ傾向：強く支持\n   - 朝食をスキップするグループは、認知的柔軟性で有意に高いスコアを示した\n\n2. 空腹状態と創造的思考の関係：部分的に支持\n   - 空腹時の脳は、より効率的で創造的な思考モードに移行する可能性が示唆された\n\n3. 認知的パフォーマンスと食事パターンの非線形関係：完全に支持\n   - 単純な栄養摂取モデルでは説明できない複雑な相互作用が明らかになった\n\n[INSERT_FORMULA_HYPOTHESIS_VERIFICATION]\n\n[INSERT_GRAPH_HYPOTHESIS_SUPPORT]\n\n重要な点は、我々の研究が従来の栄養学的パラダイムに根本的な疑問を投げかけ、知性と食事習慣の関係における新たな理解の扉を開いたことである。",
          "graphs": [
            {
              "id": "GRAPH_HYPOTHESIS_SUPPORT",
              "title": "仮説検証の支持レベル",
              "xlabel": "仮説要素",
              "ylabel": "支持度(%)",
              "grid": True,
              "legend": True,
              "charts": [
                {
                  "chart_type": "bar",
                  "categories": [
                    "IQ・朝食スキップ",
                    "空腹と創造性",
                    "認知パフォーマンス"
                  ],
                  "values": [85, 72, 90],
                  "colors": ["#3498db", "#2ecc71", "#e74c3c"]
                }
              ]
            }
          ],
          "tables": [],
          "formulas": [
            {
              "id": "FORMULA_HYPOTHESIS_VERIFICATION",
              "latex_code": "H_{verification} = \\frac{\\sum_{i=1}^{n} (x_i \\cdot w_i)}{\\sigma_{total}}",
              "description": "仮説検証の総合的支持度を計算する関数",
              "parameters": [
                {
                  "symbol": "H_{verification}",
                  "description": "仮説検証の総合支持度"
                },
                {
                  "symbol": "x_i",
                  "description": "各仮説要素の支持レベル"
                },
                {
                  "symbol": "w_i",
                  "description": "各要素の重み係数"
                },
                {
                  "symbol": "\\sigma_{total}",
                  "description": "総合変動"
                }
              ]
            }
          ]
        },
        {
          "title_name": "今後の研究方向性",
          "text": "本研究は、人間の認知機能と食事習慣の関係における新たな研究フロンティアを開拓した。今後の研究は、以下の重要な方向性に焦点を当てるべきである。\n\n将来の研究アジェンダ：\n1. 遺伝的背景と認知パフォーマンスの相互作用\n   - 個人の遺伝子型と食事パターンの関係性の詳細な解析\n\n2. 長期的認知影響の追跡研究\n   - 10年以上の縦断的研究による持続的影響の評価\n\n3. 神経科学的メカニズムの解明\n   - 空腹状態が脳の代謝と神経可塑性に与える詳細な影響\n\n[INSERT_TABLE_FUTURE_RESEARCH_DIRECTIONS]\n\n[INSERT_FORMULA_RESEARCH_POTENTIAL]\n\n特に注目すべき研究領域：\n- 個別化された認知最適化戦略の開発\n- 食事パターンと脳の可塑性の関係\n- 認知的パフォーマンスの新たな測定法の確立\n\n最終的に、この研究は単なる終着点ではなく、人間の認知機能に対する理解を深める旅の重要な通過点である。私たちの発見は、知性、栄養、そして人間の潜在能力の複雑な相互作用に対する新たな視点を提供し、未来の学際的研究への重要な基盤を築いたと言えるだろう。",
          "graphs": [],
          "tables": [
            {
              "id": "TABLE_FUTURE_RESEARCH_DIRECTIONS",
              "table_type": "basic",
              "title": "今後の研究における主要な方向性",
              "columns": ["研究領域", "主要な焦点", "予想される課題"],
              "rows": [
                [
                  "遺伝的解析",
                  "認知能力と食事パターンの遺伝的基盤",
                  "複雑な遺伝的相互作用"
                ],
                ["長期追跡", "10年以上の認知影響評価", "継続的なデータ収集"],
                [
                  "神経科学",
                  "空腹状態の脳メカニズム",
                  "複雑な神経生理学的測定"
                ],
                ["個別化戦略", "個人最適化された認知強化", "高度な個人差の考慮"]
              ],
              "style": {
                "header_bg_color": "#4A90E2",
                "header_font_color": "white",
                "cell_bg_color": "#E6F2FF",
                "cell_font_color": "black",
                "border_color": "#7BC9FF",
                "border_width": 1
              }
            }
          ],
          "formulas": [
            {
              "id": "FORMULA_RESEARCH_POTENTIAL",
              "latex_code": "P_{research} = f(\\vec{x}, t, \\sigma_{individual})",
              "description": "研究の将来的可能性を表す多変数関数",
              "parameters": [
                {
                  "symbol": "P_{research}",
                  "description": "研究の潜在的可能性"
                },
                {
                  "symbol": "\\vec{x}",
                  "description": "研究変数ベクトル"
                },
                {
                  "symbol": "t",
                  "description": "時間パラメータ"
                },
                {
                  "symbol": "\\sigma_{individual}",
                  "description": "個人差の変動"
                }
              ]
            }
          ]
        }
      ],
      "title_name": "結論"
    }
  ],
  "abstract": "本研究は、知的能力と朝食摂取パターンの関係における革新的な探求を行った。500名の高IQ専門家を対象とした12週間の実験により、従来の栄養学的常識に挑戦する驚くべき知見が得られた。\n\n朝食をスキップするグループは、創造性テストで23.7%高いスコアを示し、問題解決能力も15.4%向上した。特に興味深いのは、空腹状態が脳の認知的柔軟性を高める可能性を示唆したことである。間欠的断食グループは最も安定した認知パフォーマンスを記録し、単なる食事習慣を超えた脳の最適化メカニズムの存在を示唆した。\n\n研究は、高い知性を持つ個人が直感的に最適な認知状態を追求していることを明らかにし、「朝食は一日の最も重要な食事」という従来の概念に根本的な疑問を投げかけた。今後は、遺伝的背景や長期的影響の解明に向けた更なる研究が期待される。",
  "title": "頭いい人ほど朝食を食べない"
}

# その他の異常系テスト用のイベントデータ
ERROR_EVENT = {
    "workflow_id": "test-workflow",
    "invalid_key": "invalid_value"  # 不正なキー
} 