import requests
from bs4 import BeautifulSoup
import re

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


""""  Send a GET request to the /countri endpoint and store the response in req
Get  JSON content and store it in the countres variable and display the request's status code
and countries variabel"""
countries_url = root_url + "/countries"  
req = requests.get(countries_url)  
countries = req.json()  
print("Request status code:", req.status_code)  
print("Countries :", countries) 

""" Set the cookie_url variable
 and send a GET request to the /cookie endpoint and store the response 
 set variable cookies to req.cookies"""
cookie_url = root_url + "/cookie"  
req = requests.get(cookie_url)  
cookies = req.cookies 
print("Cookies:", cookies)


"""Set the leaders_url variable Query the /leaders endpoint, assign the output to the leaders variable"""
leaders_url = root_url + "/leaders" 
leaders = requests.get(leaders_url)

"""Query the /leaders endpoint using cookies and parameters (take any country in countries)"""
leaders_params = {"country": "us"}  
leaders_url = root_url + "/leaders"
leaders = requests.get(leaders_url, params=leaders_params, cookies=cookies).json() 

"""Function Get leaders"""
def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    status_url = root_url + "/status/"
    countries_url = root_url + "/countries"
    cookie_url = root_url + "/cookie"
    leaders_url = root_url + "/leaders"
    
    s = requests.Session()
    cookies = s.get(cookie_url).cookies 
    
    req = s.get(status_url)
    if req.status_code != 200:
        return "Error1"
    
    req = s.get(countries_url)
    if req.status_code != 200:
        return "Error2"
    
    countries = req.json()
    leaders_per_country = {}
    for country in countries:
        leaders_params = {"country": country}
        req = s.get(leaders_url, params=leaders_params)
        leaders = req.json()
        leaders_per_country[country] = leaders if leaders else []
    
    return leaders_per_country

leaders_per_country = get_leaders()
print("Leaders per country:", leaders_per_country)


#We gonna request the url of Pressident Emmanuel Macron and recieve a full HTML file.
leader_url = "https://nl.wikipedia.org/wiki/Abraham_Lincoln"
req = requests.get(leader_url)
leader_text = req.text
print(leader_text)

#We gonna parse the html file with beautifull soup
leader_html = req.text
soup = BeautifulSoup(leader_html, "html.parser")
print(soup.prettify())

#Extracting the right part of the webpage.
paragraphs = soup.find_all("p")
print(paragraphs)


def get_first_paragraph(wikipedia_url):
    print(wikipedia_url)  
    req = requests.get(wikipedia_url)
    leader_html = req.text

    soup = BeautifulSoup(leader_html, "html.parser")
    first_paragraph = ""

    for paragraph in soup.find_all("p"):
        if paragraph.get_text().strip():
            first_paragraph = paragraph.get_text()
            break

    return first_paragraph

#Testing our funtion get_first_paragraph()
wikipedia_url = "https://nl.wikipedia.org/wiki/Abraham_Lincoln"
first_paragraph = get_first_paragraph(wikipedia_url)
print(first_paragraph)

#Using regular expression
sanitized_text = re.sub(r"\[\d+\]", "", first_paragraph)
sanitized_text = re.sub(r"<.*?>", "", sanitized_text)
print(sanitized_text)

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
    sanitized_text = re.sub(r"\[\d+\]", "", first_paragraph_text)
    sanitized_text = re.sub(r"<.*?>", "", sanitized_text)
    return sanitized_text

"""EXTRA EXERCISE FOR THE END COME UP WITH OTHER regexes to capture other patterns"""

# < 20 lines
import requests

def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    status_url = root_url + "/status/"
    countries_url = root_url + "/countries"
    cookie_url = root_url + "/cookie"
    leaders_url = root_url + "/leaders"

    try:
        # Get initial cookies
        cookies = requests.get(cookie_url).cookies

        # Check if status code indicates a cookie error
        if requests.get(status_url, cookies=cookies).status_code == 401:
            # Refresh cookies
            cookies = requests.get(cookie_url).cookies

        # Check status code of /status endpoint
        if requests.get(status_url, cookies=cookies).status_code != 200:
            return "Error: /status endpoint returned an error"

        # Check status code of /countries endpoint
        if requests.get(countries_url, cookies=cookies).status_code != 200:
            return "Error: /countries endpoint returned an error"

        # Get countries
        countries = requests.get(countries_url, cookies=cookies).json()

        # Loop over countries and retrieve leaders
        leaders_per_country = {}
        for country in countries:
            leaders_params = {"country": country}
            req = requests.get(leaders_url, params=leaders_params, cookies=cookies)

            # Check if status code indicates a cookie error
            if req.status_code == 401:
                # Refresh cookies
                cookies = requests.get(cookie_url).cookies

                # Retry getting leaders for the current country
                req = requests.get(leaders_url, params=leaders_params, cookies=cookies)

            if req.status_code == 200:
                leaders_per_country[country] = req.json()

        return leaders_per_country

    except requests.exceptions.RequestException as e:
        return "Error: " + str(e)
