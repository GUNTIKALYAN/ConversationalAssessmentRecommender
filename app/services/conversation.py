class ConversationManager:

    def __init__(self):

        self.sessions = {}

    def get_session(self, session_id):

        if session_id not in self.sessions:

            self.sessions[session_id] = {
                "purpose": None,
                "seniority": None,
                "job_level": None,
                "skills": [],
                "history": [],
                "recommendations_given": False
            }

        return self.sessions[session_id]

    def update_memory(self, session_id, message):

        session = self.get_session(session_id)

        text = message.lower()

        # STORE USER HISTORY
        session["history"].append({
            "role": "user",
            "content": message
        })

        # PURPOSE

        if any(word in text for word in [
            "hiring",
            "selection",
            "screening",
            "recruit"
        ]):
            session["purpose"] = "hiring"

        if any(word in text for word in [
            "development",
            "upskill",
            "reskill",
            "training"
        ]):
            session["purpose"] = "development"

        # SENIORITY

        if any(word in text for word in [
            "senior",
            "lead",
            "principal"
        ]):
            session["seniority"] = "senior"

        if any(word in text for word in [
            "graduate",
            "entry level",
            "fresher",
            "intern",
            "student",
            "campus hire",
            "college"
        ]):
            session["seniority"] = "entry-level"

        # EXECUTIVE

        if any(word in text for word in [
            "executive",
            "director",
            "cxo"
        ]):
            session["job_level"] = "executive"

        # SKILLS / ROLES

        role_patterns = [
            "backend",
            "frontend",
            "full stack",
            "java",
            "python",
            "aws",
            "docker",
            "sql",
            "spring",
            "rust",
            "leadership",
            "sales",
            "customer service",
            "analyst"
        ]

        for role in role_patterns:

            role_words = role.split()
            
            if all(word in text for word in role_words):

                if role not in session["skills"]:
                    session["skills"].append(role)

        return session

    def needs_clarification(self, session):

        if not session["purpose"]:
            return "Is this for hiring, development, or internal mobility?"

        if not session["seniority"] and not session["job_level"]:
            return "What level of candidates are you assessing?"

        if len(session["skills"]) == 0:
            return "What role or functional area is this assessment for?"

        return None

    def build_search_query(self, session):

        query_parts = []

        if session["purpose"]:
            query_parts.append(session["purpose"])

        if session["seniority"]:
            query_parts.append(session["seniority"])

        if session["job_level"]:
            query_parts.append(session["job_level"])

        query_parts.extend(session["skills"])

        return " ".join(query_parts)

    def should_end_conversation(self, message):

        end_phrases = [
            "thanks",
            "thank you",
            "perfect",
            "confirmed",
            "that works",
            "looks good"
        ]

        text = message.lower()

        return any(phrase in text for phrase in end_phrases)


conversation_manager = ConversationManager()