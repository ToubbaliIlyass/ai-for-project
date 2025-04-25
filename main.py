from fastapi import FastAPI
from pydantic import BaseModel
import vertexai
from vertexai.preview.generative_models import GenerativeModel

import os
import base64

service_account_b64 = os.getenv("GCP_KEY_JSON")
if service_account_b64:
    decoded_key = base64.b64decode(service_account_b64).decode("utf-8")
    with open("service_account.json", "w") as f:
        f.write(decoded_key)


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

