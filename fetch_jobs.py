import requests
import re
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

EXCLUDE_WORDS = ["senior","sr", "snr", "staff engineer", "senior staff", "principal", "lead", "tech lead", "technical lead", "team lead", "lead engineer", "solutions architect", "distinguished", "expert", "specialist", "senior specialist", "consultant", "senior consultant", "manager", "engineering manager", "senior manager", "head of", "director", "associate director", "senior director", "vp", "vice president", "avp", "svp", "chief", "cto", "mid-level", "mid level", "mid-senior", "experienced", "seasoned","account executive", "sales", "operations", "planning", "partnerships", "marketing", "recruiter", "recruiting", "counsel", "legal", "finance", "accounting", "policy", "communications", "customer success", "support", "program manager","staff", "architect", "designer", "compliance", "analyst", "economist", "transformation", "enablement", "leader", "practitioner", "product builder"]
INCLUDE_WORDS = ["junior", "jr", "jr.", "entry level", "entry-level", "associate", "associate engineer", "assistant", "graduate", "new grad", "new graduate", "recent graduate", "university graduate", "early career", "early-career", "early in career", "early talent", "emerging talent", "intern", "internship", "co-op", "coop", "apprentice", "apprenticeship", "trainee", "fellowship", "fellow", "residency", "resident", "rotational program", "development program", "analyst", "junior analyst", "beginner", "novice", "fresher", "campus hire", "university hire", "college hire", "starter", "level 1", "level i" ]
AI_ML_WORDS = ["machine learning", "ml", "ai", "artificial intelligence", "ai/ml", "llm", "deep learning", "nlp", "computer vision", "genai", "gen ai", "generative ai", "mlops", "llmops", "applied scientist", "research engineer", "research scientist", "data scientist", "data science", "prompt engineer", "agentic", "ai agent", "rag", "conversational ai", "reinforcement learning", "perception", "speech recognition", "recommendation systems"]

def is_relevent(title):
    title=title.lower()
    for word in EXCLUDE_WORDS:
        if re.search(rf"\b{re.escape(word)}\b",title):
            return False
    for role in AI_ML_WORDS:
        if re.search(rf"\b{re.escape(role)}\b",title):
            return True
    return False
print(is_relevent("Machine Learning Engineer"))
print(is_relevent("Senior ML Engineer"))
print(is_relevent("AI Outcomes Manager, Financial Services"))
print(is_relevent("Retail Maintenance Coordinator"))
print(is_relevent("Research Engineer, Interpretability"))
print(is_relevent("HTML Developer"))
print(is_relevent("Software Engineer, AI Infrastructure"))

relevent_jobs = []
for job in all_jobs:
    if is_relevent(job["title"]) == True:
        relevent_jobs.append(job)

print(f"Total Jobs: {len(all_jobs)} in this relevent jobs: {len(relevent_jobs)}")
for job in relevent_jobs:
    title = job["title"]
    location = job["location"]["name"]
    company = job["company"]
    print(f"{company}: {title} | {location}")

    