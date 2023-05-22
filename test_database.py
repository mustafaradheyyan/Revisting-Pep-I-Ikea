from sqlalchemy import create_engine, text

db_username = 'admin'
db_password = 'ikeasolutionsarchitect'
db_host = 'revisiting-pep-i-ikea.c5lobpudlayi.us-west-1.rds.amazonaws.com:3306'
db_name = 'ikea_products'

db_url = f'mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}'

engine = create_engine(db_url)
conn = engine.connect()
result = conn.execute(text("select * from customers"))

for person in result:
    print(person[0])

def getCustomer(email, password):
    result = conn.execute(text(f"select customer_id from customers where email = '{email}' AND customer_pass = {password}"))
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
    


if __name__ == '__main__':
    getCustomer('test@gmail.com','12345')
    print(checkEmail('test123123@gmail.com'))
