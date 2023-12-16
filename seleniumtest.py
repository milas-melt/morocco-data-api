from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to the Chromedriver
chromedriver_path = "./chromedriver-mac-x64/chromedriver"

# Create a Service object passing the path of the Chromedriver
service = Service(chromedriver_path)

# Initialize the Chrome Driver with the Service object
driver = webdriver.Chrome(service=service)

# Open Google
driver.get("http://www.google.com")

# Find the search box
search_box = driver.find_element_by_name("q")

# Type in a search query
search_box.send_keys("Hello World")

# Wait for the results to load
driver.implicitly_wait(5)

# Print the titles of the search results
for title in driver.find_elements_by_xpath("//h3"):
    print(title.text)

# Close the browser
driver.quit()
