import pandas as pd
from jobintelengine import scrape_jobs

def scrape_jobs_to_df():
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter", "google"],
        search_term="software engineer",
        google_search_term="software engineer jobs near San Francisco, CA since yesterday",
        location="San Francisco, CA",
        results_wanted=100,
        hours_old=72,
        country_indeed="USA",
        # linkedin_fetch_description=True
    )

    # jobspy already returns pandas DataFrame
    return jobs
