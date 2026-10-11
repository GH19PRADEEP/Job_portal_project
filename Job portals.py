import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.python.org/jobs/"

headers = {
    "User-Agent": "Mozilla/5.0"
}
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, "html.parser")
job_container = soup.find("ol", class_="list-recent-jobs")
if not job_container:
    print("Jobs container not found")
    exit()
jobs = job_container.find_all("li")
print("Jobs found:", len(jobs))
job_info = []
for job in jobs:
    job_info.append(' '.join(job.prettify().split()))
job_df = pd.DataFrame(job_info, columns=['Info'])
job_df['Info'] = job_df['Info'].replace('', None)
job_df = job_df.dropna(axis=0, subset=['Info'])
file_name = r"\Users\dell\Desktop\Data enginnering notes\Job portal\jobs_info_raw.csv"
job_df.to_csv(file_name, index=False)
print("Raw Data Stored Successfully")
job_info = job_df['Info'].to_dict()
job_info = job_info.values()
job_titles = []
companies = []
posted_dates = []
locations = []
for element in job_info:
    job_soup = BeautifulSoup(str(element), "html.parser")
    title_tag = job_soup.find("a")
    if title_tag:
        job_titles.append(title_tag.text.strip())
    else:
        job_titles.append('-')
    company_tag = job_soup.find("span", class_="listing-company-name")
    if company_tag:
        company_lines = company_tag.get_text("\n", strip=True).split("\n")
        cleaned = []
        for item in company_lines:
            item = item.strip()
            if item and item != "New":
                cleaned.append(item)
        if len(cleaned) >= 2:
            companies.append(cleaned[-1])
        else:
            companies.append('-')
    else:
        companies.append('-')
    posted_tag = job_soup.find("time")
    if posted_tag:
        posted_dates.append(posted_tag.text.strip())
    else:
        posted_dates.append('-')
    location_tag = job_soup.find("span", class_="listing-location")
    if location_tag:
        locations.append(location_tag.get_text(strip=True))
    else:
        locations.append('-')
job_df.drop('Info', inplace=True, axis=1)
title_df = pd.DataFrame(job_titles, columns=['Job Title'])
company_df = pd.DataFrame(companies, columns=['Company'])
posted_df = pd.DataFrame(posted_dates, columns=['Posted Date'])
location_df = pd.DataFrame(locations, columns=['Location'])
job_df = pd.concat(
    [title_df, company_df, posted_df, location_df],
    axis=1
)
job_df.columns = ['Job Title', 'Company', 'Posted Date', 'Location']
job_df.to_csv(
    r"c:\Users\dell\Desktop\Data enginnering notes\Job portal\job_lists.csv",
    index=False
)
print(job_df)
print("job_df_Data_Stored_Successfully")