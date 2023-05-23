from sqlalchemy import text
from test_database import conn


def addCustomer(email, first_name, password):
    conn.execute(text(f"insert into customers values (NULL, '{email}', '{first_name}', '{password}')"))
    conn.commit()
    result = conn.execute(text(f"select customer_id from customers where email = '{email}'"))
    return_id = 0
    for res in result:
        return_id = res[0]
    return return_id


if __name__ == '__main__': pass