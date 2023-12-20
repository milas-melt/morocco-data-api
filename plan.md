1. Web Scraping Logic ✅
    - `data_get_requests.py`

2. process data ✅
    - `data_processor.py`

3. host data ✅
    - AWS S3 bucket

4. compute layer with aws lambda

5 create api
    i. setup api gateway
    ii. define endpoints

6. integrate lambda with s3
    i. write lambda functions
    ii. set permission

--- 

improvements
- automation
    - CRON jobs 
    - enhance lambdas for metadata and tags handling (most important)
    - data hosting (with AWS CLI, then AWS SDK)
- space complexity optimisation:
    - csv compression
- time complexity optimisation (least important)
- data visualisation tools
    - plotting endpoints
    - live dashboard webapp
- testing scripts