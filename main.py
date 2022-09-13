import requests
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time


BASE_URL = 'http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn=27820002070792'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_html(url):
    driver = webdriver.Chrome(
        executable_path="D:\\practice\\bot_parcer\\chromedriver\\chromedriver.exe"
    )
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(5)

        with open("page.html", "w") as file:
            file.write(driver.page_source)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_url():

    with open("page.html")as file:
        src = file.read()

    soup = bs(src, "lxml")
    commission_url = []

    commissions = soup.find_all('li', attrs={'aria-expanded': "false"})

    for x in commissions:
        x = 'http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn=' + x.get('id')
        commission_url.append(x)

    return commission_url


def get_html1(url):

    driver = webdriver.Chrome(
        executable_path="D:\\practice\\bot_parcer\\chromedriver\\chromedriver.exe"
    )
    driver.maximize_window()

    try:
        driver.get(url)
        time.sleep(3)
        with open("jstree.html", "w") as file:
            file.write(driver.page_source)

    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()


def get_url1(url):

    with open("jstree.html")as file:
        src = file.read()

    soup = bs(src, "lxml")
    commission_url = []

    items = soup.find_all('li', attrs={'role': 'treeitem'})

    for x in items:
        z = 0
        c = 0
        x = 'http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn=' + x.get('id')
        for y in range(len(url)):
            for a in range(len(commission_url)):
                if x == commission_url[a]:
                    c = 1
                else:
                    continue

            if x == url[y]:
                z = 1
            else:
                continue

        if z != 1 and c != 1:
            commission_url.append(x)

    return commission_url


def get_links(url):
    links = []
    for x in url:
        get_html1(x)
        links.append(get_url1(url))

    return links


def first_step():
    get_html(BASE_URL)
    url_collection = get_url()
    links = get_links(url_collection)

    with open("links.txt", "w") as file:
        print(links, file=file)


def string_to_list(string):
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace(',', '')
    string = string.replace("'", '')
    res = list(string.split(' '))
    return res


def concat_txt():
    open("links2.txt", "w").write(open("links.txt", "r").read() + open("links1.txt", "r").read())


def get_name():
    with open("links2.txt", "r") as file:
        link = file.read().rstrip()

    links = set(string_to_list(link))

    result_data = []
    for x in enumerate(links):

        print(x)

        r = requests.get(x[1], headers=HEADERS)
        soup = bs(r.text, "lxml")
        block = soup.find('div', class_='center-colm')
        commission_name = block.find('h2').text

        table = soup.find('div', class_='table margtab')
        count = table.find_all('nobr')
        time.sleep(0.3)

        for y in enumerate(count):
            result_data.append(
                {
                    'commission_name': commission_name,
                    'num_in_table': y[0] + 1,
                    'commission_url': x[1],
                    'name': y[1].get_text()
                }
            )

    with open("people.json", "w") as file:
        json.dump(result_data, file, indent=2, ensure_ascii=False)


def main():
    get_name()


if __name__ == '__main__':
    main()