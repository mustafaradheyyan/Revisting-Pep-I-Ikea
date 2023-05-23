from sqlalchemy import text
from test_database import conn


def addCustomer(email, first_name, password):
    result = conn.execute(text(f"insert into customers values (NULL, '{email}', '{first_name}', '{password}')"))
    conn.commit()
    return result


if __name__ == '__main__': pass