import psycopg2
from WebScrape import WebScrape

conn = psycopg2.connect(
    dbname="cse_courses_db",
    user="postgres",
    password="john3:16_!",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
scrape = WebScrape()
courses = scrape.getCourses()

insert_query = """
    INSERT INTO courses (id, title, units, description, prerequisites)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;  -- Avoid duplicate ID errors
"""

for course in courses:
    cursor.execute(insert_query, (
        course["id"],
        course["title"],
        course["units"],
        course["description"],
        course["prerequisites"]
    ))

conn.commit()
cursor.close()
conn.close()