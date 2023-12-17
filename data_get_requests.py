import requests
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
        self.url = ""

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def change_url(self, url):
        self.url = url

    def __str__(self):
        return f"Theme: {self.name},\nDatasets: {[dataset.name for dataset in self.datasets]}\nDatasets Count: {len(self.datasets)}\nTheme url: {self.url}"


DEBUG = True
VERBOSE = True


def get_dataset_name(link):
    if DEBUG:
        print(f"get_dataset_name: {link}")
    db_name = link.split("/")[4]
    return db_name


def get_dataset_tag(link):
    if DEBUG:
        print(f"get_dataset_tag: {link}")
    nav = f"https://data.gov.ma/data/fr/dataset/{get_dataset_name(link)}"
    link_page = requests.get(nav)
    if DEBUG:
        _status = link_page.status_code

        if _status != 200:
            print(f"\n\nERROR")
            print(f"link: {link_page}")
            print(f"status code: {_status}\n\n")
        else:
            print(f"status code: {_status}")
    link_soup = BeautifulSoup(link_page.content, "html.parser")
    try:
        tag_elements = link_soup.find("ul", class_="tag-list well").find_all("li")
        tags = [tag.get_text().strip() for tag in tag_elements]
    except AttributeError:
        tags = []
    return tags


def get_download_link(link):
    if DEBUG:
        print(f"get_download_link: {link}")
    nav = f"https://data.gov.ma/data/fr/dataset/{get_dataset_name(link)}"
    link_page = requests.get(nav)
    if DEBUG:
        _status = link_page.status_code

        if _status != 200:
            print(f"\n\nERROR")
            print(f"link: {link_page}")
            print(f"status code: {_status}\n\n")
        else:
            print(f"status code: {_status}")
    link_soup = BeautifulSoup(link_page.content, "html.parser")
    download_link = link_soup.find("a", class_="resource-url-analytics")["href"]
    return download_link


def get_datasets(theme):
    if DEBUG:
        print(f"get_datasets: {theme.name}")
    url = f"https://data.gov.ma/{theme.url}"
    page = requests.get(url)
    if DEBUG:
        _status = page.status_code

        if _status != 200:
            print(f"\n\nERROR")
            print(f"link: {page.url}")
            print(f"status code: {_status}\n\n")
        else:
            print(f"status code: {_status}")
    soup = BeautifulSoup(page.content, "html.parser")

    dataset_items = soup.find_all("li", class_="dataset-item")
    for item in dataset_items:
        link = item.find("ul").find("li").find("a")["href"]

        nav = f"https://data.gov.ma/{link}"
        link_page = requests.get(nav)
        if DEBUG:
            _status = link_page.status_code

            if _status != 200:
                print(f"\n\nERROR")
                print(f"link: {link_page.url}")
                print(f"status code: {_status}\n\n")
            else:
                print(f"status code: {_status}")
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
        if VERBOSE:
            print("=" * 50)
            print(dataset)


def get_themes():
    if DEBUG:
        print(f"get_themes")
    url = "https://data.gov.ma/data/fr/group"
    page = requests.get(url)
    if DEBUG:
        _status = page.status_code
        if _status != 200:
            print(f"\n\nERROR")
            print(f"link: {page.url}")
            print(f"status code: {_status}\n\n")
        else:
            print(f"status code: {_status}")

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


if __name__ == "__main__":
    main()
