from agents.career_master_agent import CareerMasterAgent


class CoordinatorAgent:
    """
    Coordinates the complete resume analysis workflow.
    """

    def __init__(self):
        self.master_agent = CareerMasterAgent()

    def run(self, resume_text, target_role):
        """
        Returns a Python dictionary with all analysis results.
        """

        results = self.master_agent.analyze(
            resume_text=resume_text,
            target_role=target_role
        )

        if not isinstance(results, dict):
            raise Exception("CareerMasterAgent did not return a valid dictionary.")

        required_keys = [
            "resume",
            "skills",
            "roadmap",
            "projects",
            "interview",
            "improvements",
            "jobs"
        ]

        missing = [
            key for key in required_keys
            if key not in results
        ]

        if missing:
            raise Exception(
                f"Missing keys in Gemini response: {', '.join(missing)}"
            )

        return results