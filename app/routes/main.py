from flask import current_app as app, render_template, Blueprint
from app.models import Skill, Milestone
from app.utils.helpers import generate_rule_based_insights
from collections import defaultdict
from app import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    skills = Skill.query.all()
    milestones = Milestone.query.all()
    insights = generate_rule_based_insights(
        skills, milestones
    )  # or however you generate insights

    progress_data = defaultdict(list)
    for m in milestones:
        if m.skill and m.timestamp:
            progress_data[m.skill.name].append(
                {
                    "date": m.timestamp.strftime("%Y-%m-%d"),
                    "progress_level": int(m.progress_level or 0),
                }
            )

    return render_template(
        "dashboard.html",
        milestones=milestones,
        insights=insights,
        skills=skills,
        progress_data=progress_data,  # now contains actual data
    )
