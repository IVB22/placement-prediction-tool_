import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

postings_path = os.path.join(BASE_DIR, "job_postings.csv")
skills_path   = os.path.join(BASE_DIR, "job_skills.csv")
summary_path  = os.path.join(BASE_DIR, "job_summary.csv")

out_path      = os.path.join(BASE_DIR, "jobs_and_skills.csv")

postings = pd.read_csv(postings_path)
skills   = pd.read_csv(skills_path)
summary  = pd.read_csv(summary_path)

# Merge on job_link (common key)
df = postings.merge(skills, on="job_link", how="left").merge(summary, on="job_link", how="left")

# Keep only the needed columns for your app
# (company, title, skills, description/summary)
final = df[["job_link", "company", "job_title", "job_skills", "job_summary"]].copy()

# Rename to what the backend expects
final = final.rename(columns={
    "job_title": "title",
    "job_skills": "skills",
    "job_summary": "description"
})

final.to_csv(out_path, index=False)
print("✅ Created:", out_path)
print("Columns:", final.columns.tolist())
print("Rows:", len(final))
