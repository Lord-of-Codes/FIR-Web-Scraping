import os
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from bs4 import BeautifulSoup as bs 
from pathlib import Path


start_date = datetime(2012, 1, 1)
date= datetime.now()

domain = "https://alipurduarpolice.org/"
url = "https://alipurduarpolice.org/fir.php"

headers = CaseInsensitiveDict()
headers["authority"] = "alipurduarpolice.org"
headers["path"] = "/fir.php"
headers["scheme"] = "https"
headers["accept-language"] = "en-GB,en;q=0.7"
headers["cache-control"] = "max-age=0"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["sec-ch-ua-mobile"] = "?0"
headers["sec-ch-ua-platform"] = "Linux"
headers["sec-fetch-dest"] = "document"
headers["sec-fetch-mode"] = "navigate"
headers["sec-fetch-site"] = "same-origin"
headers["sec-fetch-user"] = "?1"
headers["sec-gpc"] = "1"
headers["upgrade-insecure-requests"] = "1"
headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'

police_station ={
	"1": "Alipurduar",
	"2": "Falakata",
	"3": "Kumargram",
	"4": "Samuktala",
	"5": "Kalchini",
	"6": "Jaigaon",
	"7": "Madarihat",
	"8": "Birpara",
	"9": "Alipurduar Police Head Quarter",
	"10": "CI Office Kalchini",
	"11": "CI Office Birpara",
	"12": "ALIPURDUAR WOMEN PS",
	"13": "Cyber Crime Police Station"
}

data = "start_date=08%2F01%2F2022&police_station=1&submit=Submit"
resp = requests.post(url, headers=headers, data=data)
soup = bs(resp.content, features="html.parser")
firs = soup.find_all("div", {"class": "con1"})

for fir in firs:
	title = fir.find("h4").string
	section = fir.find("p").string
	intermediate_link = fir.find("a").get("href")
	response = requests.get(domain+intermediate_link+"&confirm=yes", headers=headers)
	k = response.content
	k = k.decode()
	k = k.replace("<SCRIPT LANGUAGE='JavaScript'>window.location.href='", "")
	k = k.replace("';</SCRIPT>","")

	response = requests.get(domain+k, headers=headers)
	filename = k.replace('upload_image/download/', '')

	path = Path.cwd().joinpath(str(date.year), date.strftime("%B"), police_station["1"])
	path.mkdir(parents=True, exist_ok=True)
	path.joinpath(filename).write_bytes(response.content)