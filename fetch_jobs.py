import requests
import re
companies = ["anthropic","binance","databricks","stripe","figma"]
def fetch_greenhouse_jobs(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        response = requests.get(url,timeout=30)
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

EXCLUDE_WORDS = ["architects","senior","sr", "snr", "staff engineer", "senior staff", "principal", "lead", "tech lead", "technical lead", "team lead", "lead engineer", "solutions architect", "distinguished", "expert", "specialist", "senior specialist", "consultant", "senior consultant", "manager", "engineering manager", "senior manager", "head of", "director", "associate director", "senior director", "vp", "vice president", "avp", "svp", "chief", "cto", "mid-level", "mid level", "mid-senior", "experienced", "seasoned","account executive", "sales", "operations", "planning", "partnerships", "marketing", "recruiter", "recruiting", "counsel", "legal", "finance", "accounting", "policy", "communications", "customer success", "support", "program manager","staff", "architect", "designer", "compliance", "analyst", "economist", "transformation", "enablement", "leader", "practitioner", "product builder"]
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

US_COUNTRY_NAMES = [
    "united states", "united states of america", "usa", "u.s.a.", "u.s.", "us",
    "us-based", "us based", "us only", "usa only",
    "remote - us", "remote (us)", "remote, us", "remote-us", "us remote",
    "remote us", "anywhere in the us", "anywhere in the united states", "nationwide",
]

STATE_CODES = [
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id",
    "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms",
    "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc", "nd", "oh", "ok",
    "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv",
    "wi", "wy", "dc", "d.c.",
]

US_STATE_NAMES = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine",
    "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey",
    "new mexico", "new york", "north carolina", "north dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
    "south dakota", "tennessee", "texas", "utah", "vermont", "virginia",
    "washington", "west virginia", "wisconsin", "wyoming",
    "district of columbia",
]

US_CITIES = [
    "washington dc", "washington, dc", "washington d.c.",
    "san francisco", "sf", "bay area", "sf bay area", "silicon valley",
    "san jose", "palo alto", "mountain view", "sunnyvale", "menlo park",
    "santa clara", "cupertino", "redwood city", "foster city", "san mateo",
    "oakland", "berkeley", "fremont", "los angeles", "santa monica",
    "culver city", "irvine", "san diego", "sacramento", "pasadena",
    "seattle", "bellevue", "redmond", "kirkland", "portland",
    "new york city", "nyc", "manhattan", "brooklyn",
    "jersey city", "hoboken", "newark", "princeton", "boston",
    "somerville", "waltham", "providence", "hartford", "stamford",
    "philadelphia", "pittsburgh",
    "arlington", "alexandria", "mclean", "reston", "herndon", "tysons",
    "chantilly", "bethesda", "rockville", "baltimore", "richmond",
    "atlanta", "miami", "tampa", "orlando", "jacksonville", "raleigh","research triangle", "charlotte", "nashville", "new orleans","huntsville",
    "austin", "dallas", "houston", "san antonio", "fort worth", "plano",
    "irving", "frisco",
    "chicago", "detroit", "ann arbor", "columbus", "cleveland", "cincinnati",
    "minneapolis", "st. louis", "saint louis", "kansas city", "indianapolis",
    "madison", "milwaukee", "omaha", "des moines",
    "denver", "boulder", "salt lake city", "lehi", "provo", "phoenix",
    "scottsdale", "tempe", "chandler", "las vegas", "albuquerque", "boise",
    "honolulu", "anchorage",
]

def is_us_location(location:str)->bool:
    location = location.lower()
    if location == "n/a":
        return True
    for area in US_COUNTRY_NAMES :
        if re.search(rf"\b{re.escape(area)}\b",location):
            return True
    pieces = re.split(r"[;|•]", location)
    for piece in pieces:
        last = piece.split(",")[-1].strip()
        if last in US_STATE_NAMES:
            return True
        if last in STATE_CODES:
            return True
    for city in US_CITIES:
        if re.search(rf"\b{re.escape(city)}\b",location):
            return True
    return False

relevent_jobs = []
for job in all_jobs:
    if is_relevent(job["title"]) == True and is_us_location(job["location"]["name"]) == True:
        relevent_jobs.append(job)
for job in relevent_jobs:
    title = job["title"]
    location = job["location"]["name"]
    company = job["company"]
    print(f"{company}: {title} | {location}")
print(f"Total Jobs: {len(all_jobs)} in this relevent jobs: {len(relevent_jobs)}")