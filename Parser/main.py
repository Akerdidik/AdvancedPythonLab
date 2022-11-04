import requests as r
import matplotlib.pyplot as plt
import numpy as np
import argparse
from bs4 import BeautifulSoup
from cve_parse import cveser
from clone import ploter

def main():
    url = "https://finance.yahoo.com/lookup"
    parser = argparse.ArgumentParser()
    parser.add_argument("parser", type=str, choices={"cve","finance"})
    parser.add_argument("--target","-t",type=str,required=False)
    args = parser.parse_args()

    if args.parser == "cve":
        if not args.target:
            print("Supply -t for target")
            exit()
        cveser(args.target)
    # elif args.parser == "finance": Works incorrectly! sometimes
    #     ploter(url)

if __name__=="__main__":

    main()

