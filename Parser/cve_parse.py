import requests as r
import matplotlib.pyplot as plt
import numpy as np
import argparse
from bs4 import BeautifulSoup

def parser_cve(keyword) -> list:

    result = []
    res = r.get(f'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={keyword}')
    soup = BeautifulSoup(res.text,'html.parser')
    table = soup.find('div', {"id": "TableWithRules"})
    cves = table.find_all('td')

    for keys in range(len(cves)):

        if keys >= 10:

            break

        if keys % 2 == 0:

            result.append(cves[keys].text)

        print(keys)
    return result

def parser_cvss(keywords: list) -> list:

    result = []

    for keyword in keywords:

        res = r.get(f'https://nvd.nist.gov/vuln/detail?vulnId={keyword}')
        soup = BeautifulSoup(res.text,'html.parser')
        table = soup.find('div',{"id": "Vuln3CvssPanel"})
        num = table.find_all_next('a')
        tt = num[0].text
        t = str(tt)
        temp = t.split(" ")

        if temp[0] == "N/A":

            tt = num[1].text
            t = str(tt)
            temp = t.split(" ")
            result.append(temp[0])
            continue
        
        print(keyword)
        result.append(temp[0])
    
    return result

def cveser(inp):
    cvss = parser_cve(inp)

    height = [float(x) for x in parser_cvss(cvss)]
    x = np.arange(len(cvss))
    width = 0.35

    fig, ax = plt.subplots()
    rects = ax.bar(x-width/3, height, label = "Rating")

    ax.set_ylabel("Rating")
    ax.set_title("Rating of latest 5 cvss")
    ax.set_xticks(x, cvss)
    ax.set_xticklabels(cvss, fontsize = 10, rotation = 45)
    ax.bar_label(rects, padding = 3)

    fig.tight_layout()
    plt.show()