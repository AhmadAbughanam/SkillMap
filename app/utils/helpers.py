from datetime import datetime, timedelta


def generate_rule_based_insights(skills, milestones):
    """
    Generate simple rule-based insights based on skill and milestone data.

    Args:
        skills (list): List of Skill model instances.
        milestones (list): List of Milestone model instances.

    Returns:
        list of strings: insight messages.
    """
    insights = []

    now = datetime.utcnow()
    two_weeks_ago = now - timedelta(days=14)

    # 1. Check skills not updated recently
    for skill in skills:
        # last updated is skill.updated_at
        if skill.updated_at < two_weeks_ago:
            insights.append(
                f'You haven’t updated skill "{skill.name}" in over 2 weeks.'
            )

    # 2. Check skills with no milestones
    for skill in skills:
        if not skill.milestones:
            insights.append(f'Skill "{skill.name}" has no milestones logged yet.')

    # 3. Check milestones older than 1 month without updates
    one_month_ago = now - timedelta(days=30)
    for milestone in milestones:
        if milestone.timestamp < one_month_ago:
            insights.append(
                f'Milestone from {milestone.timestamp.date()} on skill "{milestone.skill.name}" is over 1 month old.'
            )

    # Add more rules here as needed

    if not insights:
        insights.append("All skills and milestones are up to date. Great job!")

    return insights


def format_datetime(dt):
    """Return human-readable datetime string."""
    return dt.strftime("%Y-%m-%d %H:%M")


def sanitize_text(text):
    """Basic sanitization to prevent XSS or bad chars (if needed)."""
    import html

    return html.escape(text)
