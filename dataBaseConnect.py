import psycopg2

try:
    connection = psycopg2.connect(
        host='localhost',
        port='5432',
        database='faceData',
        user='postgres',
        password='kafprog',
    )
except psycopg2.Error as ex:
    print(f"Error: {ex}. While connecting to Database or Database not exist.")

except Exception as e:
    print(f"Error: {e}. Unexpected error in Database connect.")

# docker compose -f docker-compose.yml up -d
