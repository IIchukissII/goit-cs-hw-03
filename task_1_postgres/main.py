import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

fake = Faker()

# Підключення до бази даних
conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="567234")
cur = conn.cursor()

# Додавання груп
for _ in range(100):
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fake.name(), fake.email()))

# Додавання викладачів
for name in ('new', 'in progress', 'completed'):
    cur.execute("INSERT INTO status (name) VALUES (%s)", (name,))


# Додавання студентів і оцінок
for _ in range(100):
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (fake.word(), fake.sentence(), random.randint(1, 3), random.randint(1, 100)))

try:
    # Збереження змін
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    # Закриття підключення
    cur.close()
    conn.close()
