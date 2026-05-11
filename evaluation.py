from app.services.retriever import retriever

test_cases = [
    {
        "query": "Hiring senior backend Java engineers with AWS",
        "expected": [
            "Java",
            "Spring",
            "SQL",
            "AWS"
        ]
    },
    {
        "query": "Graduate financial analyst assessment",
        "expected": [
            "Numerical",
            "Financial",
            "Graduate"
        ]
    },
    {
        "query": "Executive leadership hiring",
        "expected": [
            "OPQ",
            "Leadership"
        ]
    }
]


def precision_at_k(retrieved, expected):

    relevant = 0

    for item in retrieved:

        name = item["name"].lower()

        if any(
            keyword.lower() in name
            for keyword in expected
        ):
            relevant += 1

    return relevant / len(retrieved)


for case in test_cases:

    results = retriever.search(case["query"])

    precision = precision_at_k(
        results,
        case["expected"]
    )

    print("\nQUERY:", case["query"])
    print("Precision@5:", round(precision, 2))

    for r in results:
        print("-", r["name"])