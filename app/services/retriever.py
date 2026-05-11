import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.embeddings import get_embedding

DATA_PATH = "app/data/data.json"

CACHE_PATH = "app/data/embeddings_cache.json"


class AssessmentRetriever:

    def __init__(self):
        self.assessments = []
        self.embeddings = []

        self.load_data()

    def load_data(self):

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assessments = data

        # Loading Cache
        if os.path.exists(CACHE_PATH):

            print("Loading cached embeddings...")

            with open(CACHE_PATH, "r") as f:
                self.embeddings = np.array(json.load(f))

            return

        print("Generating embeddings...")

        embeddings = []

        for item in self.assessments:

            # text = f"""
            # Name: {item.get("name", "")}
            # Description: {item.get("description", "")}
            # Job Levels: {", ".join(item.get("job_levels", []))}
            # Keys: {", ".join(item.get("keys", []))}
            # """
            text = f"""
            Assessment Name:
            {item.get("name", "")}

            Assessment Description:
            {item.get("description", "")}

            Supported Job Levels:
            {", ".join(item.get("job_levels", []))}

            Assessment Categories:
            {", ".join(item.get("keys", []))}

            Languages:
            {", ".join(item.get("languages", []))}

            Duration:
            {item.get("duration", "")}

            This assessment is useful for hiring, screening, evaluating, selecting, and assessing candidates.

            This assessment may help evaluate:
            software engineering,
            backend engineering,
            frontend engineering,
            cloud engineering,
            technical leadership,
            problem solving,
            programming skills,
            personality traits,
            cognitive ability,
            situational judgement,
            technical knowledge,
            behavioral fit,
            professional skills.
            """

            embedding = get_embedding(text)

            embeddings.append(embedding)

        self.embeddings = np.array(embeddings)
        
        with open(CACHE_PATH, "w") as f:
            json.dump(embeddings, f)

        print("Embeddings ready.")

    def search(self, query: str, top_k: int = 5):

        query_lower = query.lower()

        query_embedding = np.array(
            get_embedding(query)
        ).reshape(1, -1)

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        scored_results = []

        for idx, score in enumerate(similarities):

            item = self.assessments[idx]

            boosted_score = float(score)

            name = item.get("name", "").lower()
            description = item.get("description", "").lower()
            job_levels = " ".join(
                item.get("job_levels", [])
            ).lower()

            combined_text = f"{name} {description}"

            # BOOST IMPORTANT TERMS

            if "java" in query_lower and "java" in combined_text:
                boosted_score += 0.08

            if "aws" in query_lower and "aws" in combined_text:
                boosted_score += 0.10

            if "backend" in query_lower and any(
                word in combined_text
                for word in [
                    "sql",
                    "spring",
                    "web services",
                    "api"
                ]
            ):
                boosted_score += 0.06

            # SENIORITY FILTER

            if "senior" in query_lower:

                if "entry-level" in job_levels:
                    boosted_score -= 0.25

                if "graduate" in job_levels:
                    boosted_score -= 0.25

            scored_results.append({
                "item": item,
                "score": boosted_score
            })

        # SORT
        scored_results = sorted(
            scored_results,
            key=lambda x: x["score"],
            reverse=True
        )

        # DIVERSITY FILTER
        results = []

        seen_names = set()

        for result in scored_results:

            item = result["item"]

            base_name = item.get("name", "").split("(")[0].strip()

            if base_name in seen_names:
                continue

            seen_names.add(base_name)

            results.append({
                "name": item.get("name"),
                "url": item.get("link"),
                "duration": item.get("duration"),
                "description": item.get("description"),
                "score": result["score"]
            })

            if len(results) >= top_k:
                break

        return results


retriever = AssessmentRetriever()