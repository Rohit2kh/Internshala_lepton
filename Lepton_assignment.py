import requests
from bs4 import BeautifulSoup
import pandas as pd

# csv file from Kaggle.com that have multiple cities of India
df = pd.read_csv("cities.csv")
df.head()
cities = df.City

# just using another user agents beacause justdial.com have authentication for web scraping for any unauthorized user
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

# csv file where data will be store
filename = "Lepton_assign.csv"


# taking each city into account and find departmental stores from justdial.com
for city in cities:
    Name = []
    Time = []
    Place = []
    Phone_number = []
    Link = []
    Rate = []
    url = "https://www.justdial.com/" + city + "/Departmental-Stores/nct-10156727"
    response = requests.get(url, headers=HEADERS)
    if str(response) == "<Response [200]>":
        soup = BeautifulSoup(response.text, 'html.parser')
        if "Search Not Found" not in str(soup):
            phone_number = soup.find_all("span", {"class": "callcontent callNowAnchor"})
            size = len(phone_number)

            timing = soup.find_all("span", {"class": "font14 fw400 color111"})
            place = soup.find_all("div", {"class": "font15 fw400 color111"})
            anchor = soup.find_all("a", {"class": "resultbox_title_anchor line_clamp_1 font22 fw500 color111"})
            rating = soup.find_all("div", {"class": "resultbox_countrate ml-12 mr-12 font14 fw400 color777"})
            #for name and link
            for temp in anchor:
                Name.append(temp.get_text())
                Link.append("https://www.justdial.com" + temp.get('href'))

            #for phone numbers
            for temp in phone_number:
                Phone_number.append(temp.get_text())
            for temp in place:
                Place.append(temp.get_text())

            #for timimg if it is there
            for temp in timing:
                if ("Years" not in temp.get_text()):
                    Time.append(temp.get_text())
                else:
                    Time.append(None)
                    
            #for rating
            for temp in rating:
                Rate.append(temp.get_text())

            #writing into csv
            with open(filename, 'a') as f:
                for i in range(size):
                    try:
                        f.write(f"{Name[i]},{Rate[i]},{Link[i]},{Place[i]},{Time[i]},{Phone_number[i]} \n")
                    except:
                        {}
