#!/usr/bin/env python3


import requests


balise_page = "?site="
# url = "https://www.cardmarket.com/fr/YuGiOh/Products/Singles/Genesis-Impact"
# quadri = "GEIM"


def download_page_content(url):
    web_content = requests.get(url, allow_redirects=True)
    return web_content


def request_max_pages(raw_content):
    emplacement = raw_content.content.find(b"Page 1 sur ") + 11
    max_pages = int(chr(raw_content.content[emplacement]))
    return max_pages


def clear_page(page, quadri):
    copy = True
    clean_page_web = ""
    for i in page:
        if i == "<":
            copy = False
        if i == ">":
            copy = True
            clean_page_web += " "
            continue
        if copy == True:
            clean_page_web += i
    clean_page_web = clean_page_web[clean_page_web.find(quadri):]
    clean_page_web = clean_page_web[:clean_page_web.find("Page 1 sur ")]
    while clean_page_web.find("  ") != -1:
        clean_page_web = clean_page_web.replace("  ", " ")
    return clean_page_web


def list_cards(page, quadri):
    list_of_cards = page.split("€")

    for n, i in enumerate(list_of_cards):
        if len(i) < 5:
            continue
        list_of_cards[n] = i[i.find(quadri):-1] + "€"

    for n, i in enumerate(list_of_cards):
        list_of_cards[n] = i.split(" ")
    return list_of_cards


def excel_writer(cards, quadri):
    import pandas
    df = pandas.DataFrame(cards)
    writer = pandas.ExcelWriter('YuGiOh.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=quadri, index=False)
    writer.save()


def main():
    url = input("Veuillez saisir l'url du site web : ")
    quadri = input("Veuillez saisir le QUADRIGRAME de la collection en question : ")
    cards = []
    raw_content = download_page_content(url)
    max_pages = request_max_pages(raw_content)
    for i in range(1, max_pages + 1):
        page_raw = download_page_content(url + balise_page + str(i))
        page_prepared = (page_raw.content).decode('utf-8')
        page_to_cook = clear_page(page_prepared, quadri)
        page_cooked = list_cards(page_to_cook, quadri)
        for n, x in enumerate(page_cooked):
            temp_card = [quadri]
            temp_name = ""
            if len(page_cooked[n]) < 4:
                continue
            for i in range(1, len(page_cooked[n]) - 3):
                temp_name += page_cooked[n][i] + " "
            temp_card.append(temp_name)
            for i in range(len(page_cooked[n]) - 3, len(page_cooked[n])):
                temp_card.append(page_cooked[n][i])
            cards.append(temp_card)
    excel_writer(cards, quadri)


if __name__ == "__main__":
    main()