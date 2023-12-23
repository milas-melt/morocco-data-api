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

5. create api ✅

    - setup api gateway
    - define endpoints

6. integrate lambda with s3 ✅

    - write lambda functions
    - set permission

7. Test ✅

    - local lambda
    - cloud lambda

8. Deploy in dev ✅

    - dev stage creation
    - dev stage deployment

9. Security ⏳

    - Implement authorisers
        - Lambda authorisers
        - Cognito User Pools
        - IAM Authorizers
    - Use API keys
        - Create API Key
        - Setup Usage Plans
        - Distribute Keys Securely
    - Enable CORS (cross-origin ressource sharing)
        - Configure CORS
        - Specify Allowed Origins
    - Throttle and Set Quotas
        - Set Rate Limits
        - Quotas

10. Documentation

11. Monitoring and Logging

    - AWS CloudWatch for monitoring the performance and logs APIs and Lambda functions
    - or just import logging for now

    ```
        import logging

        # Initialize Logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        def lambda_handler(event, context):
            # existing code to extract path parameters...

            file_key = f"csv_data/{thematic_subfolder}/{file_name}"
            logger.info(f"Attempting to fetch S3 object: {file_key}")

            # existing S3 get_object code...

    ```

12. Cost Management: Regularly review your AWS usage and costs to optimize spending

13. Deploy
    - deploy
    - test prod

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
-   API gateway testing: if applicable, show how to test the API endpoints through tools like Postman or a web browser
-   API customisation
    -   move to AWS REST API
-   performance tracking
    -   AWS CloudWatch
    -   (?) enabling x-ray tracing for monitoring API calls
-   Standardize csv filenames (lowercase, no special chars, \_, ...) ⚠️
