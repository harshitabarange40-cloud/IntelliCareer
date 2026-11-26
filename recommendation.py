"""Rule-based expert system for IntelliCareer. No machine learning is used."""

CAREERS = [
    {
        "career": "Software Developer", "interest": "Programming",
        "skills_match": ["Problem Solving", "Logical Thinking", "Programming"],
        "subject": "Computer Science", "work": "Technical",
        "required_skills": ["Python", "Java", "Data Structures", "Algorithms", "Git", "SQL", "Debugging"],
        "description": "Designs, develops, tests and maintains software applications and systems.",
        "roles": ["Software Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer"],
        "qualification": "B.Tech/B.E. in CSE/IT or equivalent skills and portfolio.",
        "tools": ["VS Code", "Git/GitHub", "Postman", "IntelliJ IDEA"],
        "resources": ["Python: docs.python.org", "Java: dev.java/learn", "Git: git-scm.com/doc", "DSA: takeuforward.org"]
    },
    {
        "career": "Data Analyst", "interest": "Data Analysis",
        "skills_match": ["Analytical Thinking", "Mathematics", "Problem Solving"],
        "subject": "Mathematics", "work": "Data-focused",
        "required_skills": ["Excel", "SQL", "Python", "Pandas", "Statistics", "Power BI", "Data Visualization"],
        "description": "Collects, cleans and analyzes data to discover patterns and support decisions.",
        "roles": ["Junior Data Analyst", "Business Intelligence Analyst", "Reporting Analyst", "Operations Analyst"],
        "qualification": "Bachelor's degree in CSE, IT, mathematics, statistics, business or a related field.",
        "tools": ["Excel", "SQL", "Power BI", "Python", "Jupyter Notebook"],
        "resources": ["SQL: sqlbolt.com", "Python: pandas.pydata.org/docs", "Power BI: learn.microsoft.com/power-bi", "Statistics: khanacademy.org"]
    },
    {
        "career": "UI/UX Designer", "interest": "Designing",
        "skills_match": ["Creativity", "Communication", "Visual Thinking"],
        "subject": "Art and Design", "work": "Creative",
        "required_skills": ["Figma", "Wireframing", "Prototyping", "User Research", "Typography", "Color Theory", "Usability Testing"],
        "description": "Creates intuitive and accessible digital experiences by understanding user needs.",
        "roles": ["UI Designer", "UX Designer", "Product Designer", "Interaction Designer"],
        "qualification": "A degree in design, CSE or a related field; a strong portfolio is especially valuable.",
        "tools": ["Figma", "FigJam", "Adobe Illustrator", "Miro"],
        "resources": ["Figma Learn: help.figma.com", "UX basics: uxdesign.cc", "Design: interaction-design.org"]
    },
    {
        "career": "Cybersecurity Analyst", "interest": "Cybersecurity",
        "skills_match": ["Problem Solving", "Logical Thinking", "Attention to Detail"],
        "subject": "Computer Science", "work": "Security-focused",
        "required_skills": ["Networking", "Linux", "Security Fundamentals", "Python", "Risk Analysis", "SIEM Basics", "Incident Response"],
        "description": "Helps protect computer systems, networks and information by identifying and managing security risks.",
        "roles": ["Security Analyst", "SOC Analyst", "Information Security Associate", "Incident Response Analyst"],
        "qualification": "B.Tech/B.E. in CSE/IT or a related degree; networking and security knowledge are important.",
        "tools": ["Wireshark", "Linux", "Splunk", "Nmap", "VirtualBox"],
        "resources": ["Cisco Networking Academy: netacad.com", "Linux: linuxjourney.com", "OWASP: owasp.org"]
    },
    {
        "career": "Business Analyst", "interest": "Business and Strategy",
        "skills_match": ["Communication", "Analytical Thinking", "Problem Solving"],
        "subject": "Business Studies", "work": "People-focused",
        "required_skills": ["Excel", "SQL Basics", "Communication", "Requirement Analysis", "Documentation", "Data Interpretation", "Presentation"],
        "description": "Connects business needs with practical solutions by analyzing processes and requirements.",
        "roles": ["Business Analyst", "Product Analyst", "Requirements Analyst", "Process Analyst"],
        "qualification": "Bachelor's degree in business, CSE, IT, economics or a related discipline.",
        "tools": ["Excel", "PowerPoint", "Jira", "Confluence", "Draw.io"],
        "resources": ["IIBA: iiba.org", "Atlassian Guides: atlassian.com/agile", "SQL: sqlbolt.com"]
    }
]

# Each rule contributes a fixed number of points, adding up to 100.
RULES = [
    {"id": "R1", "name": "Interest Match", "points": 30, "description": "The selected interest matches the career."},
    {"id": "R2", "name": "Strongest Skill Match", "points": 20, "description": "The selected strongest skill is relevant to the career."},
    {"id": "R3", "name": "Favourite Subject Match", "points": 25, "description": "The favourite subject matches the career."},
    {"id": "R4", "name": "Work Preference Match", "points": 25, "description": "The preferred work style matches the career."}
]

INTERESTS = ["Programming", "Data Analysis", "Designing", "Cybersecurity", "Business and Strategy"]
SKILLS = ["Problem Solving", "Logical Thinking", "Analytical Thinking", "Mathematics", "Creativity", "Communication", "Visual Thinking", "Attention to Detail"]
SUBJECTS = ["Computer Science", "Mathematics", "Art and Design", "Business Studies"]
WORK_PREFERENCES = ["Technical", "Data-focused", "Creative", "Security-focused", "People-focused"]


def _matches(value, candidates):
    """Case-insensitive exact matching helper; empty values never match."""
    return bool(value) and value.strip().casefold() in {item.casefold() for item in candidates}


def recommend_careers(interest, skill, subject, work, known_skills=None):
    """Apply R1-R4 to every career and return the three highest-scoring results.

    Tie-break order: total score descending, then interest-match points descending,
    then career name alphabetically for deterministic output.
    """
    known = {s.strip().casefold() for s in (known_skills or []) if isinstance(s, str) and s.strip()}
    results = []
    for profile in CAREERS:
        score = 0
        interest_points = 0
        reasons, fired = [], []
        checks = [
            ("R1", _matches(interest, [profile["interest"]]), 30, f"Your interest in {profile['interest']} aligns with this career."),
            ("R2", _matches(skill, profile["skills_match"]), 20, f"Your strength in {skill} is useful in this field."),
            ("R3", _matches(subject, [profile["subject"]]), 25, f"Your favourite subject, {subject}, is relevant to this career."),
            ("R4", _matches(work, [profile["work"]]), 25, f"Your preferred {work.lower()} work style fits this career.")
        ]
        for rule_id, matched, points, reason in checks:
            if matched:
                score += points
                fired.append(rule_id)
                reasons.append(reason)
                if rule_id == "R1":
                    interest_points = points
        if not reasons:
            reasons.append("No exact preference rule matched. Explore this career to learn whether it interests you.")
        missing = [s for s in profile["required_skills"] if s.casefold() not in known]
        results.append({
            "career": profile["career"], "score": score, "reason": reasons,
            "rules_fired": fired, "skills": profile["required_skills"],
            "known_skills": [s for s in profile["required_skills"] if s.casefold() in known],
            "missing_skills": missing, "description": profile["description"],
            "roles": profile["roles"], "qualification": profile["qualification"],
            "tools": profile["tools"], "resources": profile["resources"],
            "interest_points": interest_points, "profile": profile
        })
    results.sort(key=lambda item: (-item["score"], -item["interest_points"], item["career"]))
    return results[:3]


def get_career(career_name):
    """Return a full career profile by its exact display name, or None."""
    return next((c for c in CAREERS if c["career"] == career_name), None)


def get_skill_gap(result):
    """Calculate the known-skill percentage for one recommendation."""
    total = len(result.get("skills", []))
    known = len(result.get("known_skills", []))
    return {"known": known, "missing": max(total - known, 0), "total": total,
            "percent": round(known / total * 100) if total else 0}


def build_roadmap(career):
    """Create a three-stage learning plan using the career's required skills."""
    skills = career["required_skills"]
    first = skills[:2]
    middle = skills[2:5]
    advanced = skills[5:]
    return [
        {"level": "Beginner", "duration": "Weeks 1–4", "tasks": first + ["Learn core concepts and practise regularly."]},
        {"level": "Intermediate", "duration": "Weeks 5–8", "tasks": middle + ["Build a small guided project."]},
        {"level": "Advanced", "duration": "Weeks 9–12", "tasks": advanced + ["Build a portfolio project and document your work."]}
    ]
