from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from shl_catalogue import shl_catalogue
from gemini import parse_jd
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# -------------------------------
# Function: Recommend Assessments
# -------------------------------
def recommend_assessments_from_jd(role, skills, catalogue):
    role = role.lower()
    skills = [skill.lower() for skill in skills]

    recommendations = []
    for product in catalogue:
        product_roles = [r.lower() for r in product.get("roles", [])]
        product_skills = [s.lower() for s in product.get("skills", [])]

        if role in product_roles or any(skill in product_skills for skill in skills):
            recommendations.append(product)

    return recommendations[:10]

# ----------------
# Route: Home Page
# ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------------
# Route: HTML Recommend
# ---------------------
@app.route('/recommend', methods=['POST'])
def recommend():
    jd = request.form.get('jd')
    if not jd:
        return render_template("index.html", error="Please enter a job description.")

    try:
        extracted = parse_jd(jd)
        role = extracted.get("role", "")
        skills = extracted.get("skills", [])
        recommendations = recommend_assessments_from_jd(role, skills, shl_catalogue)

        return render_template('index.html',
                               extracted_role=role,
                               extracted_skills=skills,
                               recommendations=recommendations)
    except Exception as e:
        logging.error(f"Error parsing JD or generating recommendations: {e}")
        return render_template("index.html", error="Failed to process job description.")

# --------------------------
# Route: API Recommendation
# --------------------------
@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data = request.json
    jd = data.get("jd", "")
    try:
        extracted = parse_jd(jd)
        role = extracted.get("role", "")
        skills = extracted.get("skills", [])
        recommendations = recommend_assessments_from_jd(role, skills, shl_catalogue)
        return jsonify(recommendations)
    except Exception as e:
        logging.error(f"API Error: {e}")
        return jsonify({"error": "Failed to process the job description"}), 500

# -----------------------
# Run the Flask App
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
