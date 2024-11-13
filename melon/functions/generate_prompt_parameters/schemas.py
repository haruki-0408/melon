INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "format": {
            "type": "object",
            "properties": {
                "category_type_en": {
                    "type": "string",
                    "enum": [
                        "development",
                        "issue"
                    ],
                    "description": "カテゴリータイプ（英語）"
                },
                "category_type_jp": {
                    "type": "string",
                    "enum": [
                        "新技術開発",
                        "問題提起"
                    ],
                    "description": "カテゴリータイプ（日本語）",
                    "const": {
                        "development": "新技術開発",
                        "issue": "問題提起"
                    }
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
        },
        "title": {
            "type": "string",
            "maxLength": 100,
            "description": "タイトル"
        }
    },
    "required": ["format", "title"]
}
