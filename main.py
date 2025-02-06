import os
import requests
import smtplib
from bs4 import BeautifulSoup
from unidecode import unidecode
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SET_PRICE = 1800

headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,ml;q=0.8",
    "Priority": "u=0, i",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

url="https://www.amazon.in/Skechers-Women-Run-400-BKPK/dp/B0BQHSTLDN/ref=sr_1_3?crid=1WCLNZJBCU4I2&dib=eyJ2IjoiMSJ9.ZrFeBzQnOMVvxyMty07EwH92dl5Q9zVkzAgBJBO2r9TCr4YkSKcLhTLzf1DuhaK4BFiL9h6xml0Fc0Lj_T00mGQkLwS9Kqx7CMtw0xsEvD7nuXY2prbXM-bluh9XkW-w4-_FXxg1Og0tUCXkhiBufk_SRI3nUueIgXONulmCBpBawDlEPys6q9MCJ5NT1IoMeVouyA0G3yzapxJjFphiajjmIvGFNudZNy9_v3AHaz2hc9q_JdJqR3DJ4mzocoWONNVUXZbCrovoefJUk-0KdcZs89nYxGEnEYAdC2MrL3dQt_gQD3EbVpMAmv0-v7RGM1OM9q-4mFopeeRb5c7a8vGelb1kCsWybbNjS1N56MiSWmWt_3-tsfYJYQn5IJc8iHIy0zMwv83qOmMTpd99hHW6p9bHrUMP7g0D2XBaoWh3vu_Ht1p7XIJ_zqDPUOmN.yJrHd4xMaTRnl67IxjsjJRlmxCZhp9Xdi97MT7oJXHk&dib_tag=se&keywords=sketchershoes+for+women&nsdOptOutParam=true&qid=1738830654&sprefix=ske%2Caps%2C365&sr=8-3"
response=requests.get(url=url,headers=headers)
data=response.text

soup=BeautifulSoup(data,"html.parser")
# print(soup.prettify())

"""To fetch price"""

#Pre-decimal
price_whole=soup.find("span",class_="a-price-whole")
price_first=price_whole.getText()

#Post-decimal
price_fraction=soup.find("span",class_="a-price-fraction")
price_second=price_fraction.getText()

#Combining Pre and Post decimal
final_price=float((price_first+price_second).replace(",",""))
print(final_price)

"""To fetch title"""
title=soup.find("span",id="productTitle")
product_title=unidecode(title.getText()) #To convert to english alphabet
print(product_title)

"""Sending Email"""
if final_price<SET_PRICE:
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL,password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=f"Subject: Amazon Price Alert!! \n\n The '{product_title}' you wanted to buy"
                                f", is now at your desired price of Rs.{final_price}. Go to this link: {url} soon!")
