# Revisting-Pep-I-Ikea

Retail website API for IKEA products. Front-end website functionality!

The database currently has 245 IKEA products from this website: https://www.kaggle.com/datasets/thedevastator/ikea-product. All of the 245 IKEA products have current valid links, contrary to a large number of IKEA products from the data source. We used web scraping to determine which of the products in the dataset have a valid link, by examining if the image id element that is usually found in valid webpages was present in the list of links that we searched. We stopped at 245 products because the web scraping operation was taking a long time to complete (around 20 minutes to process 245 correct products).

# _**Instructions to run this application:**_ #

1) Run `pip install -r requirements.txt`
2) Message our team for the database connection information (dbconn.py)

(Step 3 is optional if you did not complete step 2)  

3) Go to the backend_products directory and download all of the files  
3.1) Run `pip install -r requirements_exploration.txt`  
3.2) Create a MySQL server locally or through AWS RDS and put the username, password, host and database name (database name is from step 3.3 or name your own) in a file called dbconn.py  
3.3) Run the commands in ikea_products_schema.sql (in the sql_files directory) in your MySQL server  
3.4) Put the dbconn.py file in the same directory as your ikea_exploration.ipynb file.  
3.5) Run all of the cells in the ikea_exloration.ipynb file (for cell 61 feel free to stop execution after 30 minutes or sooner)  


4) Put the dbconn.py file in the same directory as the test_database.py file
5) Run the website.py script file
6) Open the URL that the script file outputs!
7) Have fun!
