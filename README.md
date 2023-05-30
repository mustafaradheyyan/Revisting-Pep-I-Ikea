# Revisting-Pep-I-Ikea

Retail website API for IKEA products. Front-end website functionality!

The database currently has 355 IKEA products from this website: https://www.kaggle.com/datasets/thedevastator/ikea-product. All of the 355 IKEA products have current valid links, contrary to a large number of IKEA products from the data source. We used web scraping to determine which of the products in the dataset have a valid link, by examining if the ID element of valid webpages was present in the link that we searched. We stopped at 355 products because the web scraping operation was taking a long time to complete (around 30 minutes to process 355 correct products).

Instructions to run this application:

1) Message our team for the database connection information (dbconn.py)
1.1) (Optional if did not complete step 1) Go to https://www.kaggle.com/datasets/thedevastator/ikea-product and download the dataset
1.2) (Optional) the ikea_products_schema.sql
3) Run `pip install -e requirements.txt`
4) Wait for required libraries to finish installing
5) Run the website.py script file
6) Open the URL that the script file outputs!
7) Have fun!
