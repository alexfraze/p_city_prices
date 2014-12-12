
##########################
To install and run the scraper run the following:

    bash ./install.sh && python3 downloader.py
    
##########################
# Notes
##########################

The basic structure of the scraper is here.

It does however need one more module to convert the scraped prices.

It reads from the product_map.csv and converts it to yaml. ( ease of 
migration to MySQL, or future adaptability, price conversion, etc) 
    - The product_map.csv is intended to be a map that contains the
    conversion prices for PowderCity to each other retailer.
    
It then reads from the yaml file and downloads the urls in parallel. 
    - there is a half second pause between threads so the servers dont
    503 )
    
After getting the sites it parses the sites for product, names,
sizes, and prices.

All in all it only takes a few minutes to snag 200 urls or so.


