from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


class Dataset:
    def __init__(self, name, url, download_link, tags=[]):
        self.name = name
        self.url = url
        self.download_link = download_link
        self.tags = tags

    def __str__(self):
        return f"Dataset: {self.name},\nURL: {self.url},\nDownload Link: {self.download_link}\nTags: {', '.join(self.tags)}"

    def add_tag(self, tag):
        self.tags.append(tag)


class Theme:
    def __init__(self, name):
        self.name = name
        self.datasets = []

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def __str__(self):
        return f"Theme: {self.name},\nDatasets: {[dataset.name for dataset in self.datasets]}\nDatasets Count: {len(self.datasets)}"


DEBUG = False
VERBOSE = True
HEADLESS = False

# Set up the Selenium WebDriver
chromedriver_path = "./chromedriver-mac-x64/chromedriver"

# Create a Service object passing the path of the Chromedriver
service = Service(chromedriver_path)

options = webdriver.ChromeOptions()
options.headless = HEADLESS
driver = webdriver.Chrome(options=options, service=service)


# Function to get the name of a dataset from a link
def get_dataset_name(link):
    if DEBUG:
        print(f"get_dataset_name: {link}")
    return link.split("/")[-1]


# Function to get tags for a dataset
def get_dataset_tag():
    if DEBUG:
        print(f"get_dataset_tag")
    try:
        # Wait for the tag list to load and get its HTML content
        tag_list_html = (
            WebDriverWait(driver, 5)
            .until(EC.presence_of_element_located((By.CLASS_NAME, "tag-list")))
            .get_attribute("innerHTML")
        )
    except:
        return []

    # Use BeautifulSoup to parse the HTML and extract tags
    soup = BeautifulSoup(tag_list_html, "html.parser")
    tags = [li.get_text().strip() for li in soup.find_all("li")]
    return tags


# Function to get the download link for a dataset
def get_download_link():
    if DEBUG:
        print(f"get_download_link")
    # Wait for the download link to be clickable and get its href attribute
    download_link = (
        WebDriverWait(driver, 5)
        .until(
            EC.presence_of_element_located((By.CLASS_NAME, "resource-url-analytics"))
        )
        .get_attribute("href")
    )
    return download_link


# Function to scrape datasets for a given theme
def get_datasets(theme):
    if DEBUG:
        print(f"get_datasets: {theme.name}")
    # Navigate to the theme page
    driver.get(f"https://data.gov.ma/data/fr/group/{theme.name.lower()}")
    # Use BeautifulSoup to parse the page HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all dataset items and process them
    dataset_items = soup.find_all("li", class_="dataset-item")
    for item in dataset_items:
        link_tag = item.find("a", href=True)
        if link_tag:
            dataset_link = f"https://data.gov.ma{link_tag['href']}"
            driver.get(dataset_link)
            dataset_name = get_dataset_name(dataset_link)
            dataset_tags = get_dataset_tag()
            download_link = get_download_link()
            dataset = Dataset(
                name=dataset_name,
                url=dataset_link,
                download_link=download_link,
                tags=dataset_tags,
            )
            theme.add_dataset(dataset)
        print("=" * 50)
        print(dataset)


# Function to get all themes
def get_themes():
    if DEBUG:
        print(f"get_themes")
    # Navigate to the themes page
    driver.get("https://data.gov.ma/data/fr/group")
    # Use BeautifulSoup to parse the page HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")

    theme_objects = []
    for h2 in soup.find_all("h2", class_="media-heading"):
        theme_name = h2.get_text().strip()
        theme_objects.append(Theme(theme_name))
    return theme_objects


# Main execution function
def main():
    # Get themes and their datasets
    themes = get_themes()
    for theme in themes:
        if VERBOSE:
            print("*" * 80)
            print(f"\n-----\t\tTheme: {theme.name}\t\t-----\n")
            print("*" * 80)
        get_datasets(theme)

    if VERBOSE:
        print("\n\n\n")
        print("===== LOADING COMPLETE =====")
        for theme in themes:
            print(theme)


# Make sure to close the driver after the program is finished
if __name__ == "__main__":
    try:
        main()
    finally:
        # driver.quit()
        pass
