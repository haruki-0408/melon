INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "examples": [
        {"title": "日本語のタイトル例", "category": "development"}
    ],
    "required": ["title", "category"],
    "properties": {
        "title": {
            "type": "string",
            "maxLength": 100
        },
        "category": {
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
            ]
        }
    }
}
