# API for Morocco Open data

## Getting started

-   prerequisites
    -   Basic understanding: `Python`, `AWS`, `Command Line`
    -   Software requirements: `Python`, `AWS CLI`, ... (check `requirements.txt`)
    -   AWS Account Setup
-   Clone the repo
-   setup virtual environment

```
# -------- e.g. virtual environment setup --------
python -m venv venv
source venv/bin/activate  # On Unix/macOS
venv\Scripts\activate     # On Windows
```

-   run `pip install -r requirements.txt`

-   AWS Configuration with `aws configure` followed by your aws creds. (aws services include `Lambda`, `S3`, `API Gateway`)

-   local testing with `mimic_lambda_execution_environment.py`

-   deploying to AWS (you shouldn't need to setup anything, skip this step)

-   Testing the Deployed Application
    -   Invoke Lambda via AWS Console (you shouldn't need to setup anything, skip this step)
    -   API Gateway Testing

## `data_processor.py`

make sure `xlrd` module is installed

## workflow

install packages & setup => `data_get_request.py` => `data_processor.py`

## AWS considerations

to test Lambda functions, we mimic Lambda Execution Environment => `mimic_lambda_execution_environment.py`

**instal packages**:

-   AWS SDK `boto3`
-   AWS CLI: `awscli`

### S3

-   bucket => data-morocco
-   structure => csv_data/<theme>/<filename>.csv

### Lambda

-   using arm64 architecture because more cost-efficient. if bugs, move to x86_64, but very unlikely.
-   function => DataRevriever

---

## misc

### API starter

`uvicorn api_creation_test:app --reload`

### chrome webdriver (Selenium usecase)

[Click here](https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/mac-x64/chromedriver-mac-x64.zip) to download chrome webdriver for selenium (assuming user is user chrome latest version @wed 20 dec 2023)
