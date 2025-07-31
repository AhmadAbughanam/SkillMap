from datetime import datetime
from app import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    milestones = db.relationship(
        "Milestone", backref="skill", lazy=True, cascade="all, delete-orphan"
    )
    insights = db.relationship(
        "LLMInsight", backref="skill", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Skill {self.name}>"


class Milestone(db.Model):
    __tablename__ = "milestones"

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)
    note = db.Column(db.Text, nullable=False)
    progress_level = db.Column(db.String(50))  # e.g. Beginner, Intermediate, Advanced
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Milestone {self.id} - Skill {self.skill_id}>"


class LLMInsight(db.Model):
    __tablename__ = "llm_insights"

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)
    section = db.Column(db.String(100))  # e.g., "motivation", "next steps"
    content = db.Column(db.Text, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LLMInsight {self.section} for Skill {self.skill_id}>"
