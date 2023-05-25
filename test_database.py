from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
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
    return_id = 0
    for res in result:
        return_id = res[0]

    return return_id


def checkEmail(email):
    result = conn.execute(text(f"select * from customers where email = '{email}'"))
    if result.first() is None:
        return True
    else:
        return False


def getAllProducts():
    result = conn.execute(text(f"select * from products"))
    return [r for r in result]


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
    if not query:
        sql_sort_method_string = "asc" if sort_method == "🔼" else "desc"
        sql_purchase_order_by_string = (
            f" order by {sort_parameter} {sql_sort_method_string}"
            if sort_parameter
            else ""
        )
    else:
        sql_purchase_order_by_string = f" and category_name LIKE '%{query}%'"

    sql_review_string = (
        f"select product_id, name, price, category_name, product_quantity from customer_products join products using(product_id)\
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


if __name__ == "__main__":
    # loginCustomer('test@gmail.com','12345')
    # print(checkEmail('test123123@gmail.com'))
    # result = conn.execute(text("select * from customers"))
    # print(getProduct(102065)[0][0])

    conn.rollback()
