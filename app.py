import os
import tempfile
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
from PyPDF2 import PdfReader

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

DEFAULT_PROMPT = (
    """Extract the following information from the uploaded file and format it as a professional HVAC job whitesheet. Use this exact structure and spacing, and do not add extra blank lines.\n\nJob Name: \nAddress: \nCity: \nState: \nZip: \nCustomer Name: \nContact Name: \nContact Phone: \nContact Email: \nJob Type (Commercial or Residential): \nSystem Type (Split, Package, VRF, or Other): \nTonnage: \nVoltage: \nPhase: \nHeat Type: \nCooling Type: \nGas or Electric: \nGarden or Wrap: \nControls: \nSpecial Instructions: \nNotes: \n\nFor Yes/No fields, present as 'Yes or No'. For Garden/Wrap, present as 'Garden or Wrap'."""
)

SUPPORTED_EXTENSIONS = {".pdf", ".csv"}

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS

def extract_content_from_file(file_storage):
    ext = os.path.splitext(file_storage.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file_storage.save(tmp.name)
        if ext == ".pdf":
            reader = PdfReader(tmp.name)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text
        elif ext == ".csv":
            df = pd.read_csv(tmp.name)
            return df.to_string(index=False)
        else:
            return None

def generate_whitesheet(content):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{DEFAULT_PROMPT}\n\n{content}")
    return response.text.strip() if hasattr(response, "text") else str(response)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    if "files" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    file = request.files["files"]
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Please upload a PDF or CSV file."}), 400
    try:
        content = extract_content_from_file(file)
        if not content:
            return jsonify({"error": "Could not extract content from file."}), 400
        whitesheet = generate_whitesheet(content)
        return jsonify({"whitesheet": whitesheet})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
