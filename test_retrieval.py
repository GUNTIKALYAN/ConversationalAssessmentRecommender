from app.services.retriever import retriever

query = """Senior backend Java engineer.
Strong Spring framework experience.
SQL heavy role.
Cloud-native systems.
AWS deployment.
Senior IC level.
Microservices architecture."""

results = retriever.search(query)

for r in results:
    print(r["name"], "->", r["score"])