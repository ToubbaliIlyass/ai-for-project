from fastapi import FastAPI
from pydantic import BaseModel
import vertexai
from vertexai.preview.generative_models import GenerativeModel

import os
import json

# Load the service account key from Railway's secret
service_account_json = os.getenv("GCP_KEY_JSON")
with open("service_account.json", "w") as f:
    f.write(service_account_json)

app = FastAPI()

project_id = "go-vital-ai"
location = "us-central1"

vertexai.init(project=project_id, 
              location=location, credentials="service_account.json")

model = GenerativeModel("gemini-2.0-flash")

class SummaryRequest(BaseModel):
    entries: list[str]


@app.get("/")
async def health_check():
    return {"status": "healthy"}

# Add proper error handling to your existing endpoint
@app.post("/summarize")
async def summarize_reports(data: SummaryRequest):
    try:
        prompt = f"""
You are a medical assistant AI. Given a list of medical appointment outcomes and prescriptions for the same patient, generate a clear, concise summary that:
- Explains the patient's general medical situation
- Lists the main health issues discussed
- Summarizes the prescribed treatments or medications

Here are the entries:
{chr(10).join([f"{i+1}. {entry}" for i, entry in enumerate(data.entries)])}

Now write a summary in bullet points:
"""
        response = model.generate_content(prompt)
        
        return {"summary": response.text}
    except Exception as e:
        return {"error": str(e)}, 500

