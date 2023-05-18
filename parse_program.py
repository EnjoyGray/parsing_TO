import time
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime


yy = datetime.now().year
mm = datetime.now().month
dd = datetime.now().day
mtime = datetime.now().strftime("%H.%M")
date = f"{yy}.{mm}.{dd}_{mtime}"


def pob_info_to():
    def pobieranie_id_z_to(link_strony):
        req = requests.get(link_strony, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        moja_lista = soup.find("head").find("script").text.strip()
        lista_id = moja_lista[147:-40].replace(',', ', ').split(', ')
        data_id.extend(lista_id)

    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; C6503)"
                             "AppleWebKit/537.36 (KHTML, like Gecko)"
                             "Chrome/81.0.4044.117 Mobile Safari/537.36"}

    data_id = []

    for i in range(1, 7):
        pobieranie_id_z_to(fr"https://tabelaofert.pl/nowe-mieszkania?inwestycja_3d=1&page={i}")

    link_to = "https://tabelaofert.pl/nowe-ogrody-8.0-janusza-meissnera-3-poznan-jezyce-wola-mieszkania-na-sprzedaz,"
    project_data_list = []
    start = time.time()
    for num in data_id:

        sleep(3)
        url = link_to + num

        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        all_product = soup.find_all("div", class_="ng-sz-content inwestycja")

        # Finding a file element individually
        for item in all_product:
            try:
                inwest_name = item.find(class_="szczegoly-header__title").find("h1")  # nazwa inwestycji
            except Exception:
                inwest_name = "Nie znaleziono"

            try:
                devop_name = item.find(class_="szczegoly-header__title").find("h2")  # nazwa inswetora
            except Exception:
                devop_name = "Nie znaleziono"

            try:
                url_inwestora = item.find(class_="oferent-www").find("a").get("href")
            except Exception:
                url_inwestora = "Nie znaleziono"

            try:
                makiet = item.find("div", class_="gallery-static__item-ico")  # czy jest makiet 3d
            except Exception:
                makiet = "Nie znaleziono"

            try:
                plan_kondygnacji = item.find("div", class_="gallery-static__thumbs-plan-kondygnacji")\
                   .get("data-popup-tab")  # czy sa plany kontygnacij
            except Exception:
                plan_kondygnacji = "Nie znaleziono"

            try:
                # Czy 1 wizka jest obrysowana
                wizki = item.find_next(class_="gallery-static__images-container").find("svg")
                wizki = str(wizki)
                if "svg" in wizki:
                    wizki = "Wizka_Obrysowana"
                else:
                    wizki = "jest do zrobienia"
            except Exception:
                wizki = "Nie znaleziono"

            try:
                ilosc_wizek = item.find(class_="gallery-static__image-count")  # ilosc wizek
            except Exception:
                ilosc_wizek = "Nie znaleziono"

            project_data_list.append(
                {
                    "id_inwestycji": num[1:],
                    "nazwa_inwestycji": inwest_name.text.strip(),
                    "glowna wizka": wizki,
                    "url_projektu": url,
                    "ilosc_wizek": ilosc_wizek.text.strip(),
                    "makieta_3d": makiet.text.strip(),
                    "plany_kontygnacji": plan_kondygnacji,
                    "nazwa-developera": devop_name.text.strip(),
                    "url_developera": url_inwestora

                }
            )
        df = pd.DataFrame(project_data_list)
        current_directory = os.getcwd()
        data_directory = os.path.join(current_directory, "data")
        if not os.path.exists(data_directory):
            os.mkdir(data_directory)
        df.to_excel(f'data/to_d_base_{date}.xlsx')
        print(df)
    end = time.time()
    total = end - start
    print("Пройшло часу: ", "%.2f" % total)


if __name__ == '__main__':
    pob_info_to()
