from agents.job_agent import JobAgent
from agents.resume_improvement_agent import ResumeImprovementAgent
from agents.resume_agent import ResumeAgent
from agents.skill_gap_agent import SkillGapAgent
from agents.roadmap_agent import RoadmapAgent
from agents.project_agent import ProjectAgent
from agents.interview_agent import InterviewAgent


class CoordinatorAgent:

    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.skill_agent = SkillGapAgent()
        self.roadmap_agent = RoadmapAgent()
        self.project_agent = ProjectAgent()
        self.interview_agent = InterviewAgent()
        self.improvement_agent = ResumeImprovementAgent()
        self.job_agent = JobAgent()

    def run(self, resume_text, target_role, job_description=""):

        print("Coordinator started")

        return {
            "resume": self.resume_agent.analyze_resume(
                resume_text,
                target_role
            ),
            "skills": self.skill_agent.analyze_skill_gap(
                resume_text,
                target_role
            ),
            "roadmap": self.roadmap_agent.generate_roadmap(
                resume_text,
                target_role
            ),
            "projects": self.project_agent.recommend_projects(
                resume_text,
                target_role
            ),
            "interview": self.interview_agent.generate_interview_questions(
                resume_text,
                target_role
            ),
            "improvements": self.improvement_agent.improve_resume(
             resume_text,
             target_role
            ),
            "jobs": self.job_agent.recommend_jobs(
             resume_text,
             target_role
            )
        }