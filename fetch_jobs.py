import requests
def fetch_greenhouse_jobs(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("jobs",[])
    except requests.exceptions.RequestException as e:
        print(f"An error occured when requesting for URL: {e}")
        return []

anthropic = fetch_greenhouse_jobs("anthropic")
meta = fetch_greenhouse_jobs("meta")
for job in anthropic:
    title = job["title"]
    location = job["location"]["name"]
    link = job["absolute_url"]
    print(f"Job Title: {title}")
    print(f"Job Location: {location}")
    print(f"Link to check: {link}")
print(len(anthropic))
print(len(meta))





    

    

