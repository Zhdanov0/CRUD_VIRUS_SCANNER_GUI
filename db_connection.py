import psycopg2

con = psycopg2.connect(
      database="project", 
      user="postgres", 
      password="25122002Ibrb", 
      host="127.0.0.1"
    )

cur = con.cursor()
