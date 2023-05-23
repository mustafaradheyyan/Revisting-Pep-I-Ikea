from sqlalchemy import text
from test_database import conn


def addCustomer(email, first_name, password):
    conn.execute(text(f"insert into customers values (NULL, '{email}', '{first_name}', '{password}')"))
    conn.commit()


if __name__ == '__main__': pass