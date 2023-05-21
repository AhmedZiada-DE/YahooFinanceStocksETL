# Yahoo Finance Stocks ETL pipeline
<p align="center">
  <img src="https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/a43910de-a6d7-4baf-bd68-401f6df4421d"/>
</p>

# Overview
- This project starts with Web Scraping Yahoo Finance Stocks in JSON on an AWS EC2 instance using a python script that's error proof running continusouly to scrape data in realtime then the data is sent to Kinesis using the AWS SDK library.
- The data is ingested by Kinesis Data Streams and pushed to two destinations:
    - AWS Lambda:
        - When the data is pushed to Lambda it prepares the data so that it can be sent to InfluxDB.
        - The data is sent from InfluxDB to Grafana Open Source so that it can be visualized in realtime.
        - <p align="center">
          <img src="https://github.com/AhmedZiada-DE/YahooFinanceStocksETL/assets/35679850/a43910de-a6d7-4baf-bd68-401f6df4421d"/>
          </p>
          
    - Kinesis Firehose:
        - Before processing the data Firehose dumps the unprocessed data after patching it into a backup bucket.
        - Firehose process the data and transforms the data from a JSON format to a Parquet format with the help of Glue Data Catalog.
        - The processed data is patched and stored in a separate bucket.
- Athena works best with parquet data that's why we transform the data to parquet.
- Athena can then be used to query the parquet data effiecently from S3.
- Quicksight is connected to Athena to visualize the data.



