from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
import threading

from app import cache, db
from app.models import Skill, LLMInsight
from app.utils.llm_client import generate_llm_insight

llm_bp = Blueprint("llm", __name__, url_prefix="/llm")
LOCK = threading.Lock()


@llm_bp.route("/")
def index():
    return render_template("index.html")


@llm_bp.route("/insight/<int:skill_id>", methods=["GET", "POST"])
def llm_insight(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    section = (
        request.form.get("section", "general").strip()
        if request.method == "POST"
        else None
    )

    if request.method == "POST":
        cache_key = f"llm_insight:{skill_id}:{section}"
        cached = cache.get(cache_key)

        if cached:
            flash("Loaded cached insight.", "info")
            insight_text = cached
        else:
            with LOCK:
                insight_text = generate_llm_insight(skill, section)
                cache.set(cache_key, insight_text, timeout=3600 * 24 * 7)

            new_insight = LLMInsight(
                skill_id=skill.id, section=section, content=insight_text
            )
            db.session.add(new_insight)
            db.session.commit()
            flash("Generated new LLM insight.", "success")

        return render_template(
            "llm_insights.html", skill=skill, section=section, insight=insight_text
        )

    return render_template("llm_insights.html", skill=skill, section=None, insight=None)


@llm_bp.route("/insights")
def llm_all_insights():
    insights = LLMInsight.query.order_by(LLMInsight.generated_at.desc()).all()
    return render_template("llm_all_insights.html", insights=insights)


@llm_bp.route("/clear_cache", methods=["POST"])
def llm_clear_cache():
    before_date_str = request.form.get("before_date")
    skill_id = request.form.get("skill_id")
    section = request.form.get("section")

    if not before_date_str:
        flash("Please provide a date to clear cache before.", "danger")
        return redirect(url_for("llm.llm_all_insights"))

    try:
        before_date = datetime.strptime(before_date_str, "%Y-%m-%d")
    except ValueError:
        flash("Invalid date format. Use YYYY-MM-DD.", "danger")
        return redirect(url_for("llm.llm_all_insights"))

    query = LLMInsight.query.filter(LLMInsight.generated_at < before_date)

    if skill_id:
        query = query.filter(LLMInsight.skill_id == int(skill_id))

    if section:
        query = query.filter(LLMInsight.section == section)

    count = query.delete(synchronize_session=False)
    db.session.commit()
    flash(f"Deleted {count} cached insight(s).", "success")

    if skill_id and section:
        cache_key = f"llm_insight:{skill_id}:{section}"
        cache.delete(cache_key)

    return redirect(url_for("llm.llm_all_insights"))
