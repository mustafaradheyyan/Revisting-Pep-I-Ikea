from sqlalchemy import text
from test_database import conn, check_customer_product


def addCustomer(email, first_name, password):
    conn.execute(
        text(
            f"insert into customers values (NULL, '{email}', '{first_name}', '{password}')"
        )
    )
    conn.commit()
    result = conn.execute(
        text(f"select customer_id from customers where email = '{email}'")
    )
    return_id = 0
    for res in result:
        return_id = res[0]
    return return_id


def buyProduct(customer_id, cart):
    for item in cart:
        if check_customer_product(customer_id, item):
            conn.execute(
                text(
                    f"UPDATE customer_products set product_quantity = product_quantity + {cart[item][0]} where product_id = {item}"
                )
            )
        else:
            conn.execute(
                text(
                    f"INSERT INTO customer_products(customer_id, product_id, product_quantity) VALUES({customer_id}, {item}, {cart[item][0]})"
                )
            )

    conn.commit()
