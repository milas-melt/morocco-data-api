import requests
from bs4 import BeautifulSoup
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="data_get_requests.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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
        self.url = ""

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def change_url(self, url):
        self.url = url

    def __str__(self):
        return f"Theme: {self.name},\nDatasets: {[dataset.name for dataset in self.datasets]}\nDatasets Count: {len(self.datasets)}\nTheme url: {self.url}"


def get_dataset_name(link):
    logging.debug(f"get_dataset_name: {link}")
    db_name = link.split("/")[4]
    return db_name


def get_dataset_tag(link):
    logging.debug(f"get_dataset_tag: {link}")
    nav = f"https://data.gov.ma/data/fr/dataset/{get_dataset_name(link)}"
    link_page = requests.get(nav)
    _status = link_page.status_code

    if _status != 200:
        logging.debug(f"\n\nERROR")
        logging.debug(f"link: {link_page}")
        logging.debug(f"status code: {_status}\n\n")
    else:
        logging.debug(f"status code: {_status}")
    link_soup = BeautifulSoup(link_page.content, "html.parser")
    try:
        tag_elements = link_soup.find("ul", class_="tag-list well").find_all("li")
        tags = [tag.get_text().strip() for tag in tag_elements]
    except AttributeError:
        tags = []
    return tags


def get_download_link(link):
    logging.debug(f"get_download_link: {link}")
    nav = f"https://data.gov.ma/data/fr/dataset/{get_dataset_name(link)}"
    link_page = requests.get(nav)

    _status = link_page.status_code

    if _status != 200:
        logging.debug(f"\n\nERROR")
        logging.debug(f"link: {link_page}")
        logging.debug(f"status code: {_status}\n\n")
    else:
        logging.debug(f"status code: {_status}")
    link_soup = BeautifulSoup(link_page.content, "html.parser")
    download_link = link_soup.find("a", class_="resource-url-analytics")["href"]
    return download_link


def local_download(dataset, theme_name):
    logging.debug(f"local_download. dataset: {dataset}, theme_name: {theme_name}")

    file_extension = dataset.download_link.split(".")[-1]
    folder_path = os.path.join(f"data/{theme_name}")  # Folder path for the theme

    # Create the folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{dataset.name}.{file_extension}")
    r = requests.get(dataset.download_link, allow_redirects=True)
    with open(file_path, "wb") as file:
        file.write(r.content)


def get_datasets(theme):
    logging.debug(f"get_datasets: {theme.name}")

    current_page = 1  # Start from the first page of the theme
    base_url = f"https://data.gov.ma/{theme.url}"
    while (
        True or current_page < 50
    ):  # <========= maybe find a better secondary condition ?
        logging.debug(f"current_page: {current_page}")
        paginated_url = f"{base_url}?page={current_page}"
        page = requests.get(paginated_url)

        _status = page.status_code

        if _status != 200:
            logging.debug(f"\n\nERROR")
            logging.debug(f"link: {page.url}")
            logging.debug(f"status code: {_status}\n\n")
            break
        else:
            logging.debug(f"status code: {_status}")
        soup = BeautifulSoup(page.content, "html.parser")

        dataset_items = soup.find_all("li", class_="dataset-item")
        if not dataset_items:
            break  # while loop breakpoint

        for item in dataset_items:
            try:
                link = item.find("ul").find("li").find("a")["href"]
            except:
                break

            nav = f"https://data.gov.ma/{link}"
            link_page = requests.get(nav)
            _status = link_page.status_code

            if _status != 200:
                logging.debug(f"\n\nERROR")
                logging.debug(f"link: {link_page.url}")
                logging.debug(f"status code: {_status}\n\n")
            else:
                logging.debug(f"status code: {_status}")
            link_soup = BeautifulSoup(link_page.content, "html.parser")
            db_link = link_soup.find("li", class_="resource-item").find("a")["href"]
            db_name = get_dataset_name(db_link)
            db_tags = get_dataset_tag(db_link)
            download_link = get_download_link(db_link)
            dataset = Dataset(
                name=db_name,
                url=f"https://data.gov.ma/data/fr/dataset/{db_name}",
                download_link=download_link,
                tags=db_tags,
            )
            theme.add_dataset(dataset)
            local_download(dataset, theme.name)

            logging.info("=" * 50)
            logging.info(dataset)

        current_page += 1  # move onto next page


def get_themes():
    logging.debug(f"get_themes")
    url = "https://data.gov.ma/data/fr/group"
    page = requests.get(url)

    _status = page.status_code
    if _status != 200:
        logging.debug(f"\n\nERROR")
        logging.debug(f"link: {page.url}")
        logging.debug(f"status code: {_status}\n\n")
    else:
        logging.debug(f"status code: {_status}")

    soup = BeautifulSoup(page.content, "html.parser")

    theme_objects = []
    for h2 in soup.find_all("h2", class_="media-heading"):
        text = h2.get_text().strip()
        theme_objects.append(Theme(text))

    theme_cnt = 0
    for a in soup.find_all("a", class_="media-view"):
        link = a["href"]
        theme_objects[theme_cnt].change_url(link)
        theme_cnt += 1

    return theme_objects


def main():
    themes = get_themes()
    for theme in themes:
        logging.info("*" * 80)
        logging.info(f"\n-----\t\tTheme: {theme.name}\t\t-----\n")
        logging.info("*" * 80)
        get_datasets(theme)

    logging.info("\n\n\n")
    logging.info("===== LOADING COMPLETE =====")
    for theme in themes:
        logging.info(theme)


if __name__ == "__main__":
    main()
