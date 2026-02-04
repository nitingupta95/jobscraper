# jobintelengine

**jobintelengine** is a Python job intelligence engine that scrapes and normalizes job listings from multiple job boards into a single, consistent dataset or API response.

It is useful for analytics, job discovery platforms, automation, and research workflows where aggregated job data is required.

---

## Features ✅

- Aggregate job postings from multiple job boards with a single API
- Supports **LinkedIn, Indeed, Google Jobs, ZipRecruiter, Glassdoor, Bayt, Naukri, BDJobs**
- Normalizes fields (title, company, location, salary, description, skills, etc.)
- Exports results as **CSV** or **Pandas DataFrame**
- Fast concurrent scraping with optional proxy support
- Flexible search options: remote, location, distance, recent postings, job type
- Easy integration with FastAPI/Flask or data pipelines

---

## Installation

Install the published package from PyPI:

```bash
pip install -U python-jobintelengine
```

> Note: the package on PyPI is named `python-jobintelengine`.

---

## Quickstart

Simple Python example:

```python
from jobintelengine import scrape_jobs

# Scrape multiple sites concurrently
jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "google"],
    search_term="software engineer",
    location="San Francisco, CA",
    results_wanted=50,
    hours_old=72,
    country_indeed="usa",
)

print(f"Found {len(jobs)} jobs")
print(jobs.head())

# Save to CSV
jobs.to_csv("jobs.csv", index=False)
```

There is a local example script in the repository (`run.py`) demonstrating more options (proxies, linkedin_fetch_description, google_search_term, etc.).

---

## Usage notes

- Use `google_search_term` to fine-tune Google Jobs queries (e.g. `"software engineer jobs near San Francisco, CA since yesterday"`).
- To fetch full LinkedIn descriptions, set `linkedin_fetch_description=True` (slower).
- For country-specific Indeed searches, use `country_indeed` with values like `"usa"`.
- Pass `proxies` as a list of proxy strings if needed to reduce blocking.

---

## Contributing

Contributions welcome — please open issues or pull requests. Follow the repo style (Black) and add tests when applicable.

---

## License

Licensed under the project license (see `LICENSE`).
