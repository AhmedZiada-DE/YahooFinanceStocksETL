# Yahoo Finance Stocks ETL pipeline
<p align="center">
  <img src="https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/a43910de-a6d7-4baf-bd68-401f6df4421d"/>
</p>

# Overview
- The story starts with Web Scraping Yahoo Finance Stocks an AWS EC2 instance using a python script that's error proof equiped with try and error to run continusouly so that it can scrape data in realtime.
-  Data is pushed to Kinesis Data Streams using the python SDK library.
- Data is ingested by Kinesis Data Streams and pushed to two destinations which are AWS Lambda and Kinesis Firehose.
- Firehose send the data to two S3 buckets , one is for backup.
- Athena can then be used to query the data from S3.
- Quicksight is connected to Athena to visualize the data.
# Realtime ETL Pipeline
## Extracting the data
- Data is extracted from Yahoo Finance asynchronously in a JSON format using a python then it's sent to Kinesis Data Streams using the python SDK library.
- Data is cleaned after scraping it on EC2 using the same python script.
## Loading and Transforming the data
- Data is pushed into Kinesis Data Streams which sends the data into two destinations:
    - AWS Lambda:
        - When the data is pushed to Lambda it prepares the data so that it can be sent to InfluxDB.
        - The data is sent from InfluxDB to Grafana Open Source so that it can be visualized in realtime.
    - Kinesis Firehose:
        - Before processing the data Firehose dumps the unprocessed data after patching it into a backup bucket.
        - Firehose process the data and transforms the data from a JSON format to a Parquet format with the help of Glue Data Catalog.
        - The processed data is patched and stored in a separate bucket.
    - The data is transformed to parquet in order to query it with Athena efficiently.
    
#Visualization
##Realtime Visualization with Grafana
- Data is visualized in realtime by sending the data to Lambda then Lambda prepares the data and sends it to InfluxDB.
- Grafana pulls the data from InfluxDB and the data is send used for visualizations.
    - ![ezgif com-grafana1](https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/f7baaa44-5afa-40d6-85bd-5bb46b96e775)

## AWS QuickSight
- The parquet files in S3 is queried by Athena and visualized with QuickSight.
    -  ![ezgif com-QuickSight](https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/9b43d8ac-7c64-402f-99d7-5b10f3c13483)


