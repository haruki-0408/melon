INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "workflow_id": {
            "type": "string",
            "description": "実行ID"
        },
        "title": {
            "type": "string",
            "maxLength": 100,
            "description": "タイトル"
        },
        "format": {
            "type": "object",
            "properties": {
                "category_type_en": {
                    "type": "string",
                    "enum": [
                        "development",
                        "issue",
                        "verification",
                        "case_study",
                        "theory",
                        "historical_analysis",
                        "prediction",
                        "comparison",
                        "survay",
                        "criticism"
                    ],
                    "description": "カテゴリータイプ（英語）"
                },
                "category_type_jp": {
                    "type": "string",
                    "enum": [
                        "新技術開発",
                        "問題提起",
                        "検証",
                        "ケーススタディ",
                        "理論提案",
                        "歴史的解析",
                        "予測",
                        "対比・比較",
                        "調査・アンケート",
                        "反論・批判"
                    ],
                    "description": "カテゴリータイプ（日本語）",
                },
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title_name": {
                                "type": "string",
                                "maxLength": 100
                            },
                            "sub_sections": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title_name": {
                                            "type": "string",
                                            "maxLength": 100
                                        }
                                    },
                                    "required": ["title_name"]
                                }
                            }
                        },
                        "required": ["title_name", "sub_sections"]
                    }
                }
            },
            "required": ["category_type_en", "category_type_jp", "sections"]
        }
    },
    "required": ["workflow_id","title","format"]
}
