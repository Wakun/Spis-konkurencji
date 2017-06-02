# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import xlwt  # zapis dla spisu konkurencji
# import openpyxl   # zapis dla DG3 !!! może użyć CSV?!!!
from url_dict import RTV_url_dict, AGD_url_dict, AGD_zabudowa_url_dict, AGD_male_url_dict, Komputery_url_dict, \
    Gry_i_konsole_url_dict, Foto_i_kamery_url_dict, Telefony_i_GPS_url_dict   # słowniki do adresów stron

dict_games = {"gry-pc": "PC", "gry-playstation-4": "PS4", "gry-xbox-one": "X1", "gry-xbox-360": "XBOX 360",
              "gry-playstation-3": "PS3"}   # słownik do rozróżniania gier

prod_temp = []  # tymczasowa lista produktów
ceny_temp = []  # tymczasowa lista cen
param_temp = []  # tymczasowa lista parametrów


def nazwy_produktow(max_pages, cat):
    # pobieranie nazw produktów
    page = 1

    while page <= max_pages:
        url = "http://www.euro.com.pl/" + cat + ",strona-" + str(page) + ".bhtml"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for prod in soup.find_all('h2', {'class': 'product-name'}):
            if cat in dict_games:
                for p in prod.stripped_strings:
                    prod_temp.append(dict_games[cat] + " " + p)
            else:
                for p in prod.stripped_strings:
                    prod_temp.append(p)
        page += 1


def ceny_produktow(max_pages, cat, sync):
    # pobieranie cen produktów
    page = 1

    while page <= max_pages:
        url = "http://www.euro.com.pl/" + cat + ",strona-" + str(page) + ".bhtml"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for cena in soup.find_all('div', {'class': "price-normal selenium-price-normal"}):
            ceny_temp.extend(cena.stripped_strings)
        for i in range(sync):
            ceny_temp.pop(-1)
        page += 1


def parametry_produktow(max_pages, cat):
    # pobieranie parametrów produktów wraz z nazwami
    page = 1

    while page <= max_pages:
        url = "http://www.euro.com.pl/" + cat + ",strona-" + str(page) + ".bhtml"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for param in soup.find_all('span', {'class': "attribute-value"}):
                param_temp.extend(param.stripped_strings)
        page += 1


def make_param_temp(nazwy):
    # utworzenie listy nazw produktów z parametrami !!!chyba nawet nieużywane w tej chwili!!!
    params = [prod.encode('utf-8') for prod in nazwy]
    return dict.fromkeys(params, [])


def get_max_pages(x):
    # ustalenie ilości stron dla danej kategorii
    max_p = []

    url = "http://www.euro.com.pl/" + x + ",strona-1.bhtml"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for page in soup.find_all('a', {'class': 'paging-number'}):
        max_p.extend(page.stripped_strings)

    if max_p == []:
        return 1
    else:
        p = int(max_p[-1])
        return p


def pricesynchro(cat):
    # synchronizacja cen dla spisu konkurencji

    sync_lst = []
    num = 0

    url = "http://www.euro.com.pl/" + cat + ",strona-1.bhtml"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for price in soup.find_all('div', {'class': "price-normal selenium-price-normal"}):
        sync_lst.extend(price)

    if len(sync_lst) == 34:
        num = 4
    elif len(sync_lst) == 33:
        num = 3
    elif len(sync_lst) == 30:
        return num

    return num


def param_synchro(cat):
    # synchronizacja parametrów !!!nie działa póki co!!!, !!! prawdopodobnie zrobi się to w parametry_produktów()

    sync_lst = []
    ilosc_prod = 0

    url = "http://www.euro.com.pl/" + cat + ",strona-1.bhtml"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for param in soup.find_all('span', {'class': "attribute-value"}):
        sync_lst.extend(param.stripped_strings)

    # for prod in soup.find_all('h2', {'class': 'product-name'}):
        # ilosc_prod += 1

    return len(sync_lst) / ilosc_prod


def kategoria():
    # pobranie kategorii do spisu konkurencji z url_dict

    cat = raw_input("Wpisz kategorię do spisania: ")

    if cat in RTV_url_dict:
        cat = RTV_url_dict[cat]
    elif cat in AGD_url_dict:
        cat = AGD_url_dict[cat]
    elif cat in AGD_zabudowa_url_dict:
        cat = AGD_zabudowa_url_dict[cat]
    elif cat in AGD_male_url_dict:
        cat = AGD_male_url_dict[cat]
    elif cat in Komputery_url_dict:
        cat = Komputery_url_dict[cat]
    elif cat in Gry_i_konsole_url_dict:
        cat = Gry_i_konsole_url_dict[cat]
    elif cat in Foto_i_kamery_url_dict:
        cat = Foto_i_kamery_url_dict[cat]
    elif cat in Telefony_i_GPS_url_dict:
        cat = Telefony_i_GPS_url_dict[cat]
    return cat


def printcat():
    # wyświetlenie wszystkich możliwych kategorii do spisania

    print "Kategorie: "
    print "\033[93m" + "\tRTV: " + "\033[0m"
    for cat in RTV_url_dict:
        print "\t\t-" + cat
    print "\033[93m" + "\tAGD: " + "\033[0m"
    for cat in AGD_url_dict:
        print "\t\t-" + cat
    print "\033[93m" + "\tAGD do zabudowy: " + "\033[0m"
    for cat in AGD_zabudowa_url_dict:
        print "\t\t-" + cat
    print "\033[93m" + "\tAGD Małe: " + "\033[0m"
    for cat in AGD_male_url_dict:
        print "\t\t-" + cat
    print "\033[93m" + "\tKomputery: " + "\033[0m"
    for cat in Komputery_url_dict:
        print "\t\t-" + cat
    print "\033[93m" + "\tGry i konsole: " + "\033[0m"
    for cat in Gry_i_konsole_url_dict:
        print "\t\t-" + cat
    print "\033[93m" + "\tFoto i kamery: " + "\033[0m"
    for cat in Foto_i_kamery_url_dict:
        print "\t\t-" + cat
    print "\033[93m" + "\tTelefony i GPS: " + "\033[0m"
    for cat in Telefony_i_GPS_url_dict:
        print "\t\t-" + cat


def saveresults_spis(pages, cat, sync):
    # zapisanie wyników spisu konkurencji do pliku excel

    nazwy_produktow(pages, cat)
    ceny_produktow(pages, cat, sync)

    lista_prod = [x.encode('utf-8') for x in prod_temp]
    lista_cen = [x.encode('utf-8') for x in ceny_temp]

    spisik = xlwt.Workbook(encoding="utf-8")
    sheet = spisik.add_sheet("Spis konkurencji")
    sheet.write(0, 0, "Produkt")
    sheet.write(0, 1, "Cena")

    i = 1

    for prod in lista_prod:
        i += 1
        sheet.write(i, 0, prod)

    j = 1

    for cena in lista_cen:
        j += 1
        sheet.write(j, 1, cena)

    spisik.save("Spisik.xls")


def saveresults_dg3():
    # zapisanie wyników spisu DG3 do formatki excela
    pass


def spis():
    # główny blok spisu konkurencji

    czas_start = time.time()

    print "\nSpis konkurencji\n"
    printcat()

    while True:
        ans = raw_input("Naciśnij ENTER aby spisać kategorię; Wpisz 'exit' aby zakończyć:  \n")
        if ans == 'exit':
            break
        else:
            k = kategoria()
            synchro = pricesynchro(k)
            strony = get_max_pages(k)
            saveresults_spis(strony, k, synchro)

    czas_end = time.time()
    czas_wykonania = czas_end - czas_start
    print "Czas wykonania: " + str(czas_wykonania)


def degjetrzy():
    # główny blok spisu DG3
    pass


if __name__ == "__main__":
    kat = kategoria()
    parametry_produktow(1, kat)
    sy = param_synchro(kat)
    print sy

    # lista_par = [x.encode('utf-8') for x in param_temp]
    # chunks = [lista_par[x:x + 5] for x in xrange(0, len(lista_par), 5)]

    # wb = openpyxl.load_workbook('DG3.xlsx')
    # sheet = wb.get_sheet_by_name('Spis')
    # sheet['B50'] = 'txesty'
    # wb.save('DG3.xlsx')

    # działa zapisywanie zostało !!!pobieranie parametrów!!!!!!synchro!!! i zapis ich do excela wraz z nazwą i ceną

    # pobranie cen do DG3 zrobić ze spisu konkurencji
