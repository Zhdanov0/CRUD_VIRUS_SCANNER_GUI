import psycopg2

con = psycopg2.connect(
      database="project", 
      user="postgres", 
      password="", 
      host="127.0.0.1"
    )

cur = con.cursor()
