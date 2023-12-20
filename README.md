**for data_processor**
make sure `xlrd` module is installed

**workflow**
install packages & setup => `data_get_request.py` => `data_processor.py`

**AWS considerations**
S3:

-   bucket => data-morocco
-   structure => csv_data/<theme>/<filename>.csv

Lambda:

-   using arm64 architecture because more cost-efficient. if bugs, move to x86_64, but very unlikely.
-   function => DataRevriever

---

**misc**
**_API starter_**
`uvicorn api_creation_test:app --reload`

**_webdriver_**
[Click here](https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/mac-x64/chromedriver-mac-x64.zip) to download chrome webdriver for selenium (assuming user is user chrome latest version @wed 20 dec 2023)
