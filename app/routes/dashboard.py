from collections import defaultdict
from app import db


@app.route("/dashboard")
def dashboard():
    skills = Skill.query.order_by(Skill.name).all()
    milestones = Milestone.query.order_by(Milestone.timestamp).all()

    insights = []
    for skill in skills:
        last_update = skill.updated_at or skill.created_at
        days_since = (datetime.utcnow() - last_update).days
        if days_since > 14:
            insights.append(f"You haven’t updated '{skill.name}' in {days_since} days.")

    progress_data = defaultdict(list)
    for m in milestones:
        progress_data[m.skill.name].append(
            {
                "date": m.timestamp.strftime("%Y-%m-%d"),
                "progress_level": 1,  # safe fallback value
            }
        )

    for skill_name in progress_data:
        progress_data[skill_name].sort(key=lambda x: x["date"])

    return render_template(
        "dashboard.html", skills=skills, insights=insights, progress_data=progress_data
    )
