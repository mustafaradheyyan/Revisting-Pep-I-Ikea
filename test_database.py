from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import datetime
import dbconn

db_username = dbconn.db_username
db_password = dbconn.db_password
db_host = dbconn.db_host
db_name = dbconn.db_name

db_url = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}"

engine = create_engine(db_url)
conn = engine.connect()


def loginCustomer(email, password):
    result = conn.execute(
        text(
            f"select customer_id from customers where email = '{email}' AND customer_pass = '{password}'"
        )
    )
    return_id = -1
    for res in result:
        return_id = res[0]

    return return_id


def checkEmail(email):
    result = conn.execute(text(f"select * from customers where email = '{email}'"))
    if result.first() is None:
        return True
    else:
        return False


def getAllProducts(sort_parameter=None, sort_method=None, query=None):
    sql_sort_method_string = "desc" if sort_method == "🔼" else "asc"

    if query:
        sql_purchase_order_by_string = f" where {sort_parameter} LIKE '%{query}%'"
    elif sort_parameter:
        if sort_parameter == "total_price":
            sql_purchase_order_by_string = (
                f" order by price * product_quantity {sql_sort_method_string}"
            )
        else:
            sql_purchase_order_by_string = (
                f" order by {sort_parameter} {sql_sort_method_string}"
            )
    else:
        sql_purchase_order_by_string = ""

    sql_review_string = (
        f"select product_id, name, category_name, short_description, price from products\
 join product_categories using(category_id)"
        + sql_purchase_order_by_string
    )
    with Session(engine) as session:
        result = session.execute(text(sql_review_string))

    result_list = [r for r in result]
    return result_list


def getAllReviews(user_id, sort_parameter=None, sort_method=None):
    sql_sort_method_string = "asc" if sort_method == "🔼" else "desc"
    sql_review_order_by_string = (
        f" order by {sort_parameter} {sql_sort_method_string}" if sort_parameter else ""
    )
    sql_review_string = (
        f"select product_id, name, price, num_stars from product_reviews join customer_product_review using(product_review_id)\
                                join products using(product_id) where customer_id = {user_id}"
        + sql_review_order_by_string
    )

    with Session(engine) as session:
        result = session.execute(text(sql_review_string))

    result_list = [r for r in result]
    result_list = [
        tuple(x if i != 3 else "⭐" * x for i, x in enumerate(result))
        for result in result_list
    ]
    return result_list


def getAllPurchases(user_id, sort_parameter=None, sort_method=None, query=None):
    sql_sort_method_string = "desc" if sort_method == "🔼" else "asc"

    if query:
        sql_purchase_order_by_string = f" and {sort_parameter} LIKE '%{query}%'"
    elif sort_parameter:
        if sort_parameter == "total_price":
            sql_purchase_order_by_string = (
                f" order by price * product_quantity {sql_sort_method_string}"
            )
        else:
            sql_purchase_order_by_string = (
                f" order by {sort_parameter} {sql_sort_method_string}"
            )
    else:
        sql_purchase_order_by_string = ""

    sql_review_string = (
        f"select product_id, name, price, category_name, product_quantity, purchase_date, customer_id from customer_products join products using(product_id)\
 join product_categories using(category_id) where customer_id = {user_id}"
        + sql_purchase_order_by_string
    )
    with Session(engine) as session:
        result = session.execute(text(sql_review_string))

    result_list = [r for r in result]
    return result_list


def getCustomerInfo(cust_id):
    result = conn.execute(
        text(f"select * from customers where customer_id = {cust_id}")
    )
    return [r for r in result]


def getProduct(id):
    result = conn.execute(
        text(
            f"select product_id, name, price, image, short_description, designer, category_name from products join product_categories using (category_id) where product_id = {id}"
        )
    )
    return [r for r in result]


def buyProduct(customer_id, cart):
    x = datetime.datetime.now()
    current_time = x.strftime('%Y-%m-%d %H:%M:%S')

    for item in cart:
        conn.execute(text(f"INSERT INTO customer_products(customer_id, product_id, purchase_date, product_quantity) VALUES({customer_id}, {item}, '{current_time}', {cart[item][0]})"))
    conn.commit()

def changeName(customer_id, new_name):
    conn.execute(text(f"UPDATE customers set first_name = '{new_name}' where customer_id = {customer_id}"))
    conn.commit()

def deleteUser(customer_id):
    conn.execute(text(f'DELETE FROM customers WHERE customer_id = {customer_id}'))
    conn.commit()


if __name__ == "__main__":
    # loginCustomer('test@gmail.com','12345')
    # print(checkEmail('test123123@gmail.com'))
    # result = conn.execute(text("select * from customers"))
    # print(getProduct(102065)[0][0])
    #print(loginCustomer('yoelgebre@gmail.com', '123456789'))
    conn.rollback()
