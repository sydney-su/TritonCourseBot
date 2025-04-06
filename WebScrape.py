import requests
from bs4 import BeautifulSoup
import re

class WebScrape:
    def scrape(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the main div containing all the courses
        main_div = soup.find("div", class_="col-md-12 blank-slate")

        # Iterate over all <p> tags within this main div
        p_tags = main_div.find_all("p")[6:280]

        for i in range(0, len(p_tags), 3):  # Assuming alternating title-description pairs
            # Extract the course title from <p class="course-name">
            title_tag = p_tags[i]  # We directly use the <p> tag for the title
            id = title = units = pattern = description = "n/a"
            if title_tag and "course-name" in title_tag.get("class", []):
                title_tag = title_tag.text.strip()
                pattern = r"^(?P<id>[A-Z]+\s*\d+[A-Za-z]*)\.\s+(?P<title>.*?)\s+\((?P<units>[\d–]+)\)"
                match = re.match(pattern, title_tag)
                if match:
                    id = match.group("id")
                    title = match.group("title")
                    units = match.group("units")

            # Extract the course description from <p class="course-descriptions">
            description_tag = p_tags[i + 1] if i + 1 < len(p_tags) else None
            if description_tag and "course-descriptions" in description_tag.get("class", []):
                pattern = r"^(?P<description>.+?)\s*Prerequisites:\s*(?P<preq>.+)$"
                description_tag = description_tag.text.strip()
                # Split on 'Prerequisites:' if it exists
                parts = re.split(r"\s*Prerequisites:\s*", description_tag, maxsplit=1)
                description = parts[0].strip()
                prereqs = parts[1].strip() if len(parts) > 1 else "None"

                # Append the course information to the list
            self.courses.append({
                "id": id,
                "title": title,
                "units": units,
                "description": description,
                "prerequisites": prereqs
            })

    
    def getCourses(self):
        return self.courses
    

    def printItems(self):
        for item in self.courses:
            for key in item:
                print(f"{key}: {item[key]}")
            print()


    def __init__(self, url = "https://catalog.ucsd.edu/courses/CSE.html"):
        # Fetch the webpage
        self.courses = []
        self.scrape(url)
        #self.printItems()

scrape = WebScrape()