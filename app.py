"""Flask web application for IntelliCareer."""
from io import BytesIO
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file, abort, flash
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from recommendation import (CAREERS, RULES, INTERESTS, SKILLS, SUBJECTS,
                             WORK_PREFERENCES, recommend_careers, get_career,
                             get_skill_gap, build_roadmap)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "intell career-local-development-key-change-before-deployment")


def current_results():
    """Rebuild recommendation details from the current session inputs."""
    data = session.get("assessment")
    if not data:
        return None
    results = recommend_careers(data.get("interest", ""), data.get("skill", ""),
                                data.get("subject", ""), data.get("work", ""),
                                data.get("known_skills", []))
    for item in results:
        item["gap"] = get_skill_gap(item)
        item["roadmap"] = build_roadmap(item["profile"])
    return results


@app.route("/")
def home():
    """Render the landing page and its dashboard overview."""
    return render_template("index.html", career_count=len(CAREERS), rule_count=len(RULES))


@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    """Collect four preferences and optional known skills, then calculate results."""
    errors = []
    values = {"interest": "", "skill": "", "subject": "", "work": ""}
    known_skills = []
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in values}
        known_skills = request.form.getlist("known_skills")
        allowed = {"interest": INTERESTS, "skill": SKILLS, "subject": SUBJECTS, "work": WORK_PREFERENCES}
        labels = {"interest": "interest", "skill": "strongest skill", "subject": "favourite subject", "work": "work preference"}
        for key, options in allowed.items():
            if values[key] not in options:
                errors.append(f"Please select a valid {labels[key]}.")
        valid_skills = set(SKILLS)
        known_skills = [s for s in known_skills if s in valid_skills]
        if not errors:
            session["assessment"] = {**values, "known_skills": known_skills}
            return redirect(url_for("result"))
    return render_template("assessment.html", interests=INTERESTS, skills=SKILLS,
                           subjects=SUBJECTS, work_preferences=WORK_PREFERENCES,
                           values=values, known_skills=known_skills, errors=errors)


@app.route("/result")
def result():
    """Show the top three recommendations and personalized learning information."""
    results = current_results()
    if results is None:
        flash("Complete the assessment to view your recommendations.", "info")
        return redirect(url_for("assessment"))
    return render_template("result.html", results=results, assessment=session["assessment"], rules=RULES)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    """Compare two selected career profiles side by side."""
    names = [c["career"] for c in CAREERS]
    first = request.values.get("career1", names[0])
    second = request.values.get("career2", names[1])
    comparison = None
    if request.method == "POST":
        if first not in names or second not in names:
            flash("Please choose two valid careers.", "error")
        elif first == second:
            flash("Choose two different careers to compare.", "error")
        else:
            comparison = [get_career(first), get_career(second)]
    return render_template("compare.html", careers=CAREERS, names=names,
                           career1=first, career2=second, comparison=comparison)


@app.route("/download-report")
def download_report():
    """Generate a downloadable PDF report for the current assessment."""
    results = current_results()
    if results is None:
        flash("Complete the assessment before downloading a report.", "info")
        return redirect(url_for("assessment"))
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=18*mm, bottomMargin=18*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="PurpleTitle", parent=styles["Title"], textColor=colors.HexColor("#673ab7")))
    story = [Paragraph("IntelliCareer – Career Recommendation Report", styles["PurpleTitle"]), Spacer(1, 8)]
    data = session["assessment"]
    story.append(Paragraph("Assessment Summary", styles["Heading2"]))
    summary = [["Interest", data["interest"]], ["Strongest skill", data["skill"]],
               ["Favourite subject", data["subject"]], ["Work preference", data["work"]]]
    table = Table(summary, colWidths=[42*mm, 125*mm])
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (0,-1), colors.HexColor("#eee7fb")),
                               ("GRID", (0,0), (-1,-1), .4, colors.lightgrey),
                               ("PADDING", (0,0), (-1,-1), 7)]))
    story += [table, Spacer(1, 12), Paragraph("Top Career Recommendations", styles["Heading2"])]
    for index, item in enumerate(results, 1):
        story.append(Paragraph(f"{index}. {item['career']} — {item['score']}% match", styles["Heading3"]))
        story.append(Paragraph(item["description"], styles["BodyText"]))
        story.append(Paragraph("Why this career? " + " ".join(item["reason"]), styles["BodyText"]))
        story.append(Paragraph("Roles: " + ", ".join(item["roles"]), styles["BodyText"]))
        story.append(Paragraph("Skills to learn: " + ", ".join(item["missing_skills"]), styles["BodyText"]))
        story.append(Spacer(1, 8))
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="IntelliCareer_Report.pdf", mimetype="application/pdf")


@app.errorhandler(404)
def not_found(error):
    """Render a branded not-found page for unknown routes."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
