import requests
companies = ["anthropic","binance","databricks","stripe","figma"]
def fetch_greenhouse_jobs(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("jobs",[])
    except requests.exceptions.RequestException as e:
        print(f"failed to fetch {slug}: {e}")
        return []

all_jobs = []
for company in companies:
    jobs = fetch_greenhouse_jobs(company)
    for job in jobs:
        job["company"] = company
    print(f"Total jobs at {company}: {len(jobs)}")
    all_jobs.extend(jobs)
print(f"Total {len(all_jobs)} jobs.")

for job in all_jobs[:10]:
    title = job["title"]
    location = job["location"]["name"]
    company = job["company"]
    print(f"{company}: {title} | {location}")








    

    

