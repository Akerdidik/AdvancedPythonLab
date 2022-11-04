import requests as r
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

def parser(keywords) -> list:

    res = []

    for keys in keywords:

        url = f"https://finance.yahoo.com/quote/{keys}"
        resp = r.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        ids = soup.find("div", {"id":"quote-summary"})
        tds = ids.find_all('td')
        prev = tds[1]
        nexter = tds[3]
        res.append(prev.text)
        res.append(nexter.text)
        print(prev.text)
        print(nexter.text)
        
    return res

def justifier(lister) -> list:
    res = []

    for i in range(len(lister)):

        if i+1!=len(lister):

            if i%2==0:

                temp = lister[i] - lister[i+1]
                res.append(temp)

    return res

def shares(url1) -> list:

    res = []
    resp = r.get(url1)
    soup = BeautifulSoup(resp.text, "html.parser")
    name = soup.find("section", {"id":"lookup-page"})
    s = name.find_all('a')

    for i in s:
        print(i.text)
        res.append(i.text)

    return res

def ploter(url1):
    inp = shares(url1)
    temp = [float(x) for x in parser(inp)]
    print(temp)
    height = justifier(temp)
    print(height)
    x = np.arange(len(inp))
    width = 0.35
    
    fig, ax = plt.subplots()
    rects = ax.bar(x-width/3, height, label = "Names")

    ax.set_ylabel("Value")
    ax.set_title("The difference the certain shares (latest sales)")
    ax.set_xticks(x, inp)
    ax.set_xticklabels(inp, fontsize = 10, rotation = 45)
    ax.bar_label(rects, padding = 3)

    fig.tight_layout()
    plt.show()
