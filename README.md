# IntelliCareer – Intelligent Career Recommendation Expert System

A responsive Flask web application that uses a transparent, rule-based expert system to recommend career paths. It is an educational guidance tool, not a machine-learning model or a substitute for professional career counselling.

## Features

- Home dashboard with five career paths, feature cards, FAQ accordion and three-step explanation.
- Assessment with four required dropdowns and optional known-skill chips.
- Knowledge base containing five career profiles and an IF–THEN rule base.
- Four scoring rules (maximum 100 points), top-three recommendations and deterministic tie-breaking.
- Explanation facility showing why each career was recommended and which rules fired.
- Skill-gap analysis, progress bars and Beginner → Intermediate → Advanced roadmap.
- Side-by-side comparison of any two different careers.
- PDF report download using ReportLab.
- Responsive purple-white interface, mobile navigation, scroll reveal, count-up cards, dark mode saved in localStorage and back-to-top button.
- No database. Assessment data is held in the Flask session.

## Folder structure

```text
IntelliCareer/
├── app.py
├── recommendation.py
├── requirements.txt
├── README.md
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── index.html
    ├── assessment.html
    ├── result.html
    ├── compare.html
    └── 404.html
```

## Setup and run

Python 3.10 or newer is recommended.

1. Open a terminal in the `IntelliCareer` folder.
2. (Optional) Create and activate a virtual environment:

   **Windows CMD**
   ```bat
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000/` in your browser.

For a public deployment, set a strong secret key through an environment variable and turn Flask debug mode off. The included development secret key is for local demonstration only.

## Expert system design

### Knowledge base

The `CAREERS` list in `recommendation.py` stores the five career profiles. Each profile includes interest, matching strengths, favourite subject, work preference, required skills, description, roles, qualification, tools and learning resources.

### Rule base and scoring

| Rule | IF condition | THEN points |
|---|---|---:|
| R1 – Interest Match | User interest matches the career interest | 30 |
| R2 – Strongest Skill Match | Selected strongest skill appears in the career's matching skills | 20 |
| R3 – Favourite Subject Match | User subject matches the career subject | 25 |
| R4 – Work Preference Match | User work preference matches the career work style | 25 |
| **Total** | **All four rules match** | **100** |

### Inference engine

`recommend_careers(interest, skill, subject, work, known_skills)` checks all four rules for every career. It adds points for matched rules, stores rule IDs and explanation sentences, then sorts by score descending. If scores tie, the career with an interest match ranks first; any remaining tie is resolved alphabetically so the result is predictable. It returns at most three careers.

### Explanation facility

Each recommendation includes `reason` and `rules_fired`. The result page displays these values under **Why this career?**, making the recommendation traceable to the rules.

## Screenshots

Add screenshots after running the app. Suggested screenshots:

1. `screenshots/home.png` – homepage and dashboard cards.
2. `screenshots/assessment.png` – assessment form and skill chips.
3. `screenshots/result.png` – top-three recommendations and explanation.
4. `screenshots/compare.png` – side-by-side career comparison.
5. `screenshots/report.png` – downloaded PDF report.

Create a `screenshots/` folder and place your own screenshots there. No screenshot files are bundled because they depend on your local browser and run.

## Test cases

The following are manual functional test cases for the web app and inference engine.

| # | Input | Expected output |
|---:|---|---|
| 1 | Programming, Problem Solving, Computer Science, Technical | Software Developer scores 100 and ranks first. |
| 2 | Data Analysis, Analytical Thinking, Mathematics, Data-focused | Data Analyst scores 100 and ranks first. |
| 3 | Designing, Creativity, Art and Design, Creative | UI/UX Designer scores 100 and ranks first. |
| 4 | Cybersecurity, Mathematics, Computer Science, Security-focused | Cybersecurity Analyst scores 80 (R1, R3, R4); R2 does not match. |
| 5 | Business and Strategy, Communication, Business Studies, People-focused | Business Analyst scores 100 and ranks first. |
| 6 | Programming, Communication, Mathematics, Creative | No career scores above 30 unless a selected value matches another rule; exactly three results are returned. |
| 7 | Valid four preferences, known skills left empty | Recommendations are still generated; all required career skills appear as skills to develop. |
| 8 | All four dropdowns left blank and form submitted | Server rejects the submission and displays validation errors; no result session is created. |
| 9 | Two careers have equal total scores, one has an interest match | The career with the interest-match rule ranks ahead of the other tied career. |
| 10 | Open `/this-page-does-not-exist` | Branded custom 404 page is displayed with HTTP status 404. |

## Notes and limitations

- The score is a rule-match percentage, not a prediction of job success or employability.
- Known skills are used for the skill-gap section, not for the 100-point career ranking.
- Skill names are illustrative starting points. Actual job requirements vary by employer and experience level.
- The app stores assessment inputs in the browser session cookie, not in a database.
