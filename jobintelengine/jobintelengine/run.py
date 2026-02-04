from jobintelengine import scrape_jobs

print("🔍 Scraping jobs...")

jobs = scrape_jobs(
    site_name=["indeed"],
    search_term="software engineer intern",
    location="India",
    results_wanted=5
)

print(jobs[["title", "company", "location"]])
