from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
from datetime import datetime
from jobintelengine import scrape_jobs

# -------------------------
# Load environment variables
# -------------------------
if os.path.exists(".env"):
    load_dotenv(".env")

# -------------------------
# App setup
# -------------------------
app = FastAPI(title="Job Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request schema
# -------------------------
class ScrapeRequest(BaseModel):
    search_terms: List[str]
    locations: List[str]

    site_names: Optional[List[str]] = Field(
        default=["indeed", "linkedin", "google"],
        description="Job sites to scrape"
    )
    results_wanted: Optional[int] = Field(
        default=40,
        description="Jobs per search"
    )
    hours_old: Optional[int] = Field(
        default=168,
        description="Max job age in hours"
    )

# -------------------------
# Core scraper logic
# -------------------------
def run_hunt(
    search_terms: List[str],
    locations: List[str],
    site_names: List[str],
    results_wanted: int,
    hours_old: int,
):
    all_jobs = []

    for term in search_terms:
        for location in locations:
            print(f"🔍 Searching for {term} in {location}...")
            try:
                kwargs = {
                    "site_name": site_names,
                    "search_term": term,
                    "google_search_term": f"{term} jobs near {location} since last week",
                    "results_wanted": results_wanted,
                    "hours_old": hours_old,
                    "linkedin_fetch_description": False,
                }

                if location.lower() == "remote":
                    kwargs["location"] = "Remote"
                else:
                    kwargs["location"] = location
                    kwargs["country_indeed"] = "Nigeria"

                jobs = scrape_jobs(**kwargs)

                if jobs is not None and not jobs.empty:
                    all_jobs.append(jobs)

            except Exception as e:
                print(f"❌ Error fetching {term} in {location}: {e}")

    if not all_jobs:
        return None

    final_jobs = pd.concat(all_jobs).drop_duplicates(
        subset=["title", "company", "site"],
        keep="first"
    )

    final_jobs.sort_values(by="date_posted", ascending=False, inplace=True)

    columns_to_keep = [
        "title", "company", "location", "via", "site", "date_posted",
        "job_url", "is_remote", "salary", "job_type", "description"
    ]

    for col in columns_to_keep:
        if col not in final_jobs.columns:
            final_jobs[col] = ""

    final_jobs = final_jobs[columns_to_keep]

    final_jobs.rename(columns={
        "title": "job_title",
        "via": "posted_via",
        "site": "source_site",
        "is_remote": "remote",
    }, inplace=True)

    final_jobs.fillna("N/A", inplace=True)

    final_jobs["description"] = final_jobs["description"].apply(
        lambda x: x[:500] + "..." if isinstance(x, str) and x != "N/A" else "N/A"
    )

    final_jobs.sort_values(by=["location", "job_title"], inplace=True)

    return final_jobs

# -------------------------
# API: Returns JSON + forwards to external API
# -------------------------
@app.post("/scrape-json")
def scrape_json(payload: ScrapeRequest):
    df = run_hunt(
        payload.search_terms,
        payload.locations,
        payload.site_names,
        payload.results_wanted,
        payload.hours_old,
    )

    if df is None or df.empty:
        generated_response = {
            "success": False,
            "message": "No jobs found",
            "count": 0,
            "data": []
        }
    else:
        def convert_dates(obj):
            if isinstance(obj, dict):
                return {k: convert_dates(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_dates(i) for i in obj]
            elif hasattr(obj, "isoformat"):
                return obj.isoformat()
            return obj

        data_records = convert_dates(df.to_dict(orient="records"))

        generated_response = {
            "success": True,
            "count": len(df),
            "generated_at": datetime.utcnow().isoformat(),
            "data": data_records
        }

    # -------------------------
    # Forward to external API
    # -------------------------
    api_url = os.getenv("EXTERNAL_API_URL")
    if not api_url:
        return generated_response

    try:
        print("[LOG] Sending data to external API")
        response = requests.post(api_url, json=generated_response, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ External API error: {e}")
        return generated_response
