from sqlalchemy import create_engine, text
import dbconn

db_username = dbconn.db_username
db_password = dbconn.db_password
db_host = dbconn.db_host
db_name = dbconn.db_name

db_url = f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}'

engine = create_engine(db_url)
conn = engine.connect()


def loginCustomer(email, password):
    result = conn.execute(text(f"select customer_id from customers where email = '{email}' AND customer_pass = '{password}'"))
    return_id = 0
    for res in result:
        return_id = res[0]

    return return_id

def checkEmail(email):
    result = conn.execute(text(f"select * from customers where email = '{email}'"))
    if (result.first() is None):
        return True
    else:
        return False
    
def getAllProducts():
    result = conn.execute(text(f"select * from products"))
    return [r for r in result]

def getCustomerInfo(cust_id):
    result = conn.execute(text(f"select * from customers where customer_id = {cust_id}"))
    return [r for r in result]

def getProduct(id):
    result = conn.execute(text(f"select product_id, name, price, image, short_description, designer, category_name from products join product_categories using (category_id) where product_id = {id}"))
    return [r for r in result]

if __name__ == '__main__':
    #loginCustomer('test@gmail.com','12345')
    #print(checkEmail('test123123@gmail.com'))
    #result = conn.execute(text("select * from customers"))
    #print(getProduct(102065)[0][0])

    conn.rollback()
