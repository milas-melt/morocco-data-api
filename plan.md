1. Web Scraping Logic ✅

    - `data_get_requests.py`

2. process data ✅

    - `data_processor.py`

3. host data ✅

    - AWS S3 bucket

4. compute layer with aws lambda ✅

    - write lambda functions
    - mimic lambda execution environment in local for api gateway local test
    - setup aws cli
    - local test
    - upload lambda function on the cloud
    - configure event test then test it on the cloud

5. create api
   i. setup api gateway
   ii. define endpoints

6. integrate lambda with s3 ✅
   i. write lambda functions
   ii. set permission

7. Documentation

8. Monitoring and Logging

    - AWS CloudWatch for monitoring the performance and logs APIs and Lambda functions

9. Cost Management: Regularly review your AWS usage and costs to optimize spending

---

improvements

-   automation
    -   CRON jobs: WS CloudWatch Events or AWS EventBridge
    -   enhance lambdas for metadata and tags handling (most important)
    -   data hosting (with AWS CLI, then AWS SDK)
-   space complexity optimisation:
    -   csv compression
-   time complexity optimisation (least important)
-   data visualisation tools
    -   plotting endpoints
    -   live dashboard webapp
-   testing scripts
-   scraping with scrapy for scaling
