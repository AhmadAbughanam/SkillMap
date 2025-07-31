from flask import Blueprint, request, redirect, url_for, render_template, flash
from datetime import datetime
from app import db
from app.models import Skill, Milestone
from app.utils.llm_client import generate_llm_insight
from app.models import LLMInsight
from flask import current_app as app

skills_bp = Blueprint("skills", __name__, url_prefix="/skills")


# List all skills
@skills_bp.route("/")
def skills_list():
    skills_data = Skill.query.order_by(Skill.updated_at.desc()).all()
    return render_template("skills.html", skills=skills_data)


# View skill details and milestones
@skills_bp.route("/<int:skill_id>")
def skill_detail(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    milestones = (
        Milestone.query.filter_by(skill_id=skill.id)
        .order_by(Milestone.timestamp.desc())
        .all()
    )
    return render_template("skill_detail.html", skill=skill, milestones=milestones)


# Create a new skill - GET shows form, POST processes submission
@skills_bp.route("/new", methods=["GET", "POST"])
def skill_create():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")

        if not name:
            flash("Skill name is required.", "danger")
            return redirect(url_for("skills.skill_create"))

        existing = Skill.query.filter_by(name=name).first()
        if existing:
            flash("Skill with that name already exists.", "warning")
            return redirect(url_for("skills.skill_create"))

        skill = Skill(name=name, description=description, category=category)
        db.session.add(skill)
        db.session.commit()

        try:
            ai_text = generate_llm_insight(skill, section="initial")
            insight = LLMInsight(
                skill_id=skill.id,
                section="initial",
                content=ai_text,
                generated_at=datetime.utcnow(),
            )
            db.session.add(insight)
            db.session.commit()
        except Exception as e:
            app.logger.error(
                f"LLM insight generation failed for skill {skill.name}: {e}"
            )

        flash(f'Skill "{name}" created successfully.', "success")
        return redirect(url_for("skills.skills_list"))

    return render_template("skill_form.html", action="Create", skill=None)


# Edit existing skill
@skills_bp.route("/<int:skill_id>/edit", methods=["GET", "POST"])
def skill_edit(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")

        if not name:
            flash("Skill name is required.", "danger")
            return redirect(url_for("skills.skill_edit", skill_id=skill_id))

        existing = Skill.query.filter(Skill.name == name, Skill.id != skill_id).first()
        if existing:
            flash("Another skill with that name already exists.", "warning")
            return redirect(url_for("skills.skill_edit", skill_id=skill_id))

        skill.name = name
        skill.description = description
        skill.category = category
        db.session.commit()

        flash(f'Skill "{name}" updated successfully.', "success")
        return redirect(url_for("skills.skill_detail", skill_id=skill_id))

    return render_template("skill_form.html", action="Edit", skill=skill)


# Delete skill
@skills_bp.route("/<int:skill_id>/delete", methods=["POST"])
def skill_delete(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash(f'Skill "{skill.name}" deleted.', "info")
    return redirect(url_for("skills.skills_list"))


# Add a milestone to a skill
@skills_bp.route("/<int:skill_id>/milestones/new", methods=["GET", "POST"])
def milestone_create(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    if request.method == "POST":
        note = request.form.get("note")
        progress_level = request.form.get("progress_level")
        timestamp_str = request.form.get("timestamp")

        if not note:
            flash("Milestone note is required.", "danger")
            return redirect(url_for("skills.milestone_create", skill_id=skill_id))

        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except ValueError:
                flash("Invalid timestamp format.", "warning")
                return redirect(url_for("skills.milestone_create", skill_id=skill_id))
        else:
            timestamp = datetime.utcnow()

        milestone = Milestone(
            skill_id=skill.id,
            note=note,
            progress_level=progress_level,
            timestamp=timestamp,
        )
        db.session.add(milestone)
        db.session.commit()

        try:
            ai_text = generate_llm_insight(skill, section="progress update")
            insight = LLMInsight(
                skill_id=skill.id,
                section="progress update",
                content=ai_text,
                generated_at=datetime.utcnow(),
            )
            db.session.add(insight)
            db.session.commit()
        except Exception as e:
            app.logger.error(f"LLM insight generation failed after milestone: {e}")

        flash("Milestone added.", "success")
        return redirect(url_for("skills.skill_detail", skill_id=skill_id))

    return render_template("milestone_form.html", skill=skill)


# Edit milestone
@skills_bp.route("/milestones/<int:milestone_id>/edit", methods=["GET", "POST"])
def milestone_edit(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    skill = milestone.skill

    if request.method == "POST":
        note = request.form.get("note")
        progress_level = request.form.get("progress_level")
        timestamp_str = request.form.get("timestamp")

        if not note:
            flash("Milestone note is required.", "danger")
            return redirect(url_for("skills.milestone_edit", milestone_id=milestone_id))

        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except ValueError:
                flash("Invalid timestamp format.", "warning")
                return redirect(
                    url_for("skills.milestone_edit", milestone_id=milestone_id)
                )
        else:
            timestamp = milestone.timestamp

        milestone.note = note
        milestone.progress_level = progress_level
        milestone.timestamp = timestamp
        db.session.commit()
        flash("Milestone updated.", "success")
        return redirect(url_for("skills.skill_detail", skill_id=skill.id))

    return render_template("milestone_form.html", skill=skill, milestone=milestone)


# Delete milestone
@skills_bp.route("/milestones/<int:milestone_id>/delete", methods=["POST"])
def milestone_delete(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    skill_id = milestone.skill_id
    db.session.delete(milestone)
    db.session.commit()
    flash("Milestone deleted.", "info")
    return redirect(url_for("skills.skill_detail", skill_id=skill_id))
