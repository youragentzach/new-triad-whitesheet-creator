# Gemini File Extractor with Whitesheet Generator

This application allows you to upload PDF or CSV files and generates a professional, structured HVAC job whitesheet using Google's Gemini AI. All compliance and chatbot features have been removed, focusing solely on robust, high-quality whitesheet generation.

## Features
- Upload PDF or CSV files
- Whitesheet generation using Gemini AI with strict formatting
- Responsive, modern UI
- Render.com deployment ready
- Robust error handling, no sample data fallbacks

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set your `GOOGLE_API_KEY` in a `.env` file or your deployment environment
4. Run locally: `python app.py`

## Deployment
- Ready for Render.com with `render.yaml`
- Ensure `GOOGLE_API_KEY` is set as an environment variable in Render

## Whitesheet Format Requirements
- Strict adherence to template structure
- Professional, visually appealing spacing
- Yes/No options as "Yes or No"
- Minimal unnecessary blank lines
- "Garden/Wrap" as "Garden or Wrap"

## License
MIT
