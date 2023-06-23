import requests
from bs4 import BeautifulSoup
import re
import json

"""Assign the root URL to the root_url variable
Assign the /status endpoint URL to the status_url variable
Send a GET request to the /status endpoint and store the response in req"""
root_url = "https://country-leaders.onrender.com"  
status_url = root_url + "/status/"  
req = requests.get(status_url) 


# Check the status_code of the response and print response
if req.status_code == 200:  
    print("Successful!")  
    print("Response:", req.text)  
else:
    print("Request failed with status code:", req.status_code)  
    
#Function get leaders is already the last modifyt version
def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    status_url = root_url + "/status/"
    countries_url = root_url + "/countries"
    cookie_url = root_url + "/cookie"
    leaders_url = root_url + "/leaders"

    # Create a session object
    session = requests.Session()

    try:
        # Get Cookie
        cookies = session.get(cookie_url).cookies

        # Check status code cookie
        if session.get(status_url, cookies=cookies).status_code == 422:
            cookies = session.get(cookie_url).cookies

        # Get countries
        countries = session.get(countries_url, cookies=cookies).json()

        # Loop over countries and retrieve leaders
        leaders_per_country = {}
        for country in countries:
            leaders_params = {"country": country}
            req = session.get(leaders_url, params=leaders_params, cookies=cookies)

            # Check if status code indicates a cookie error
            if req.status_code == 422:
                cookies = session.get(cookie_url).cookies

                # Retry getting leaders for the current country
                req = session.get(leaders_url, params=leaders_params, cookies=cookies)

            if req.status_code == 200:
                # Pass the session to the get_first_paragraph() function
                first_paragraph = get_first_paragraph(req.url, session)
                leaders_per_country[country] = {"leaders": req.json(), "first_paragraph": first_paragraph}

        return leaders_per_country

    except requests.exceptions.RequestException as e:
        return "Error: " + str(e)

#Function get first paragraph but it's cleaned up 
def get_first_paragraph(wikipedia_url):
    # Retrieve the HTML content from the Wikipedia URL
    response = requests.get(wikipedia_url)
    html_content = response.content

    # Create a BeautifulSoup object for parsing the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the first paragraph element
    first_paragraph = soup.find("p")

    # Extract the text from the first paragraph
    first_paragraph_text = first_paragraph.get_text()

    # Apply regular expressions to sanitize the text only thing we don't return are the anchors and wiki link
    sanitized_text = re.sub(r"\[\d+]|\[\/?\w+\]", "", first_paragraph_text)
    sanitized_text = re.sub(r"<.*?>", "", sanitized_text)
    return sanitized_text

#testing sanitezed get first paragraph
wikipedia_url = "https://nl.wikipedia.org/wiki/Abraham_Lincoln"
first_paragraph = get_first_paragraph(wikipedia_url)
print(first_paragraph)

#Modifyt version of get first paragraph
def get_first_paragraph(wikipedia_url, session):
    response = session.get(wikipedia_url)
    leader_html = response.text

    soup = BeautifulSoup(leader_html, "html.parser")
    first_paragraph = ""

    for paragraph in soup.find_all("p"):
        if paragraph.get_text().strip():
            first_paragraph = paragraph.get_text()
            break

    return first_paragraph

# Create a session object
session = requests.Session()
# Testing the get_first_paragraph() function with the session
wikipedia_url = "https://nl.wikipedia.org/wiki/Abraham_Lincoln"
first_paragraph = get_first_paragraph(wikipedia_url, session)
print(first_paragraph)

leader_per_country = get_leaders()
print(leader_per_country)

#Code to easily save
def save(data):
    with open("leaders.json", "w") as file:
        file.write(json.dumps(data))
#Calling the function 
save(leader_per_country)

# Read the leaders.json file
with open("leaders.json", "r") as file:
    loaded_data = json.load(file)

# Check if the loaded data matches the original leaders_per_country dictionary
if loaded_data == leader_per_country:
    print("Load data match leaders_pet_country")
else:
    print("Loaded data does not match the leaders_per_country")
