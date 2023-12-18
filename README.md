# Yahoo Finance Stocks ETL pipeline
<p align="center">
  <img src="https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/a43910de-a6d7-4baf-bd68-401f6df4421d"/>
</p>

# Overview
- The story starts with Web Scraping Yahoo Finance Stocks on an AWS EC2 instance using a python script that's error proof equipped with a try and error code to run continuously so that it can scrape data in real-time.
- Data is pushed to Kinesis Data Streams using the python SDK library.
- Data is ingested by Kinesis Data Streams and pushed to two destinations which are AWS Lambda and Kinesis Firehose.
- Firehose sends the data to two S3 buckets, one is for backup.
- Athena can then be used to query the data from S3.
- Quick Sight is connected to Athena to visualize the data.
# Realtime ETL Pipeline
## Extracting the data
- Data is extracted from Yahoo Finance asynchronously in a JSON format using a python then it's sent to Kinesis Data Streams using the python SDK library.
- Data is cleaned after scraping it on EC2 using the same python script.
## Loading and Transforming the data
- Data is pushed into Kinesis Data Streams which sends the data into two destinations:
    - AWS Lambda:
        - When the data is pushed to Lambda it prepares the data so that it can be sent to InfluxDB.
        - Grafana is used to visualize the data in realtime by pulling the data from InfluxDB.
    - Kinesis Firehose:
        - Before processing the data ,Firehose dumps the unprocessed data after patching it into a backup bucket.
        - Firehose process the data and transforms the data from a JSON format to a Parquet format with the help of Glue Data Catalog.
        - The processed data is patched and stored in a separate bucket.
    - Transforming the data happens by defining a table schema in AWS Glue and then Firehose uses the table to transform the data to parquet.
         - If there were further transformations on the data. It would require us to use Lambda but since it's a simple transformation doing it inside firehose makes the infrastructure much simpler.
    - The data is transformed to parquet in order to query it with Athena efficiently.
    
# Visualization
## Realtime Visualization with Grafana
- Data is visualized in realtime by sending the data to Lambda then Lambda prepares the data and sends it to InfluxDB.
- Grafana pulls the data from InfluxDB and the data is send used for visualizations.
    - ![ezgif com-grafana1](https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/f7baaa44-5afa-40d6-85bd-5bb46b96e775)

## AWS QuickSight
- The parquet files in S3 is queried by Athena and visualized with QuickSight.
    -  ![ezgif com-QuickSight](https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/9b43d8ac-7c64-402f-99d7-5b10f3c13483)


