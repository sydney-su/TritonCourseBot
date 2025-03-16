import requests
from bs4 import BeautifulSoup
import re

# Fetch the webpage
url = "https://catalog.ucsd.edu/courses/CSE.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Initialize a list to store course data
courses = []

# Find the main div containing all the courses
main_div = soup.find("div", class_="col-md-12 blank-slate")

# Iterate over all <p> tags within this main div
p_tags = main_div.find_all("p")

for i in range(0, len(p_tags), 2):  # Assuming alternating title-description pairs
    # Extract the course title from <p class="course-name">
    title_tag = p_tags[i]  # We directly use the <p> tag for the title
    if title_tag and "course-name" in title_tag.get("class", []):
        title = title_tag.text.strip()

    # Extract the course description from <p class="course-descriptions">
    description_tag = p_tags[i + 1] if i + 1 < len(p_tags) else None
    if description_tag and "course-descriptions" in description_tag.get("class", []):
        description = description_tag.text.strip()

        # Extract prerequisites if they exist in the description
        prereqs = "None"
        if "Prerequisites" in description:
            # Regex to capture everything after "Prerequisites:"
            match = re.search(r"Prerequisites?:?\s*(.*)", description)
            if match:
                prereqs = match.group(1).strip()

        # Append the course information to the list
        courses.append({
            "title": title,
            "description": description,
            "prerequisites": prereqs
        })

print(courses)