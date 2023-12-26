import psycopg2

connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='faceData',
    user='postgres',
    password='123',
)

# docker compose -f faceDataBase/postgres/docker-compose.yml up -d