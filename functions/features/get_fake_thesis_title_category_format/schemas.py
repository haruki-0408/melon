INPUT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "examples": [
        {"category": "development"}
    ],
    "required": ["category"],
    "properties": {
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
