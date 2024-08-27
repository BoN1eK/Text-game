import random
import os
import sys
import time
import threading
import msvcrt


def clear():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux / OSX
        os.system('clear')


def write(string, end: str = '\n'):
    stop_animation = threading.Event()

    def animation():
        animated_text = ""
        for s in string:
            animated_text += s
            sys.stdout.write(s)
            sys.stdout.flush()
            time.sleep(0.1)

            if stop_animation.is_set():
                break
        sys.stdout.write(end)
        return animated_text

    animated_text = ""

    animation_thread = threading.Thread(target=lambda: setattr(stop_animation, 'result', animation()))
    animation_thread.start()

    try:
        while animation_thread.is_alive():
            if msvcrt.kbhit() and msvcrt.getch() == b' ':
                stop_animation.set()
                animation_thread.join()  # Animacja czekanie na koniec

                # Sprawdzanie dł. i wypisanie
                remaining_text = string[len(animated_text):]
                sys.stdout.write('\r' + remaining_text + ' ' * (len(string) - len(remaining_text)) + end)
                sys.stdout.flush()
                break
        print()
    except KeyboardInterrupt:
        stop_animation.set()


def mistakes():
    while True:
        try:
            wybor = input("Wybierz opcję 1/2/3: ")
            if wybor in ("1", "2", "3"):
                return wybor
            else:
                print("\033[31m" + "Nieodpowiedni numer" + "\033[0m")
        except ValueError:
            print("\033[31m" + "Niepoprawny format, wprowadź liczbę 1, 2 lub 3." + "\033[0m")


def mistakes2(lista):
    write("Posiadane przedmioty: ", end=" ")
    for i in lista:
        print('-', i)
    while True:
        try:
            wybor = input("Wybierz przedmiot: ")
            if wybor in (lista):
                return wybor
            else:
                print("\033[31m" + "Nieodpowiedni przedmiot" + "\033[0m")
        except ValueError:
            print("\033[31m" + "Niepoprawny format, wybierz przedmiot z dostępnych: " + lista + "\033[0m")


def mistakes3():
    while True:
        try:
            wybor = input("tak lub nie: ")
            if wybor == "tak" or wybor == "nie":
                return wybor
            else:
                print("\033[31m" + "Nieodpowiedni wybor" + "\033[0m")
        except ValueError:
            print("\033[31m" + "Niepoprawny format, wybierz tak lub nie: " + "\033[0m")


def print_loading_frame(percentage):
    bar_length = 14
    loaded_length = int(bar_length * percentage)
    remaining_length = bar_length - loaded_length

    fill_char = "█"
    space_char = " "

    # Wypełnienie paska
    loading_bar = fill_char * loaded_length + space_char * remaining_length

    sys.stdout.write("\033[33m" + "\r" + "[" + loading_bar + "]" + f" {int(percentage * 100)}%")
    sys.stdout.flush()


class uczen:
    def __init__(self, nazwa, zdrowie, nauka, pieniadze):
        self.nazwa = nazwa
        self.zdrowie = zdrowie
        self.nauka = nauka
        self.pieniadze = pieniadze


class przedmiot:
    def __init__(self, nazwa, efekt, opis):
        self.nazwa = nazwa
        self.efekt = efekt
        self.opis = opis

    def __str__(self):
        return f"Nazwa: {self.nazwa}, Efekt: {self.efekt}, Opis: {self.opis}"


okulary = przedmiot("okulary", 1.15, "Zwyczajne okulary, w nich czujesz sie mądrzejszy, +15% do nauki")
karta = przedmiot("karta kredytowa rodziców", 1.25, "Złota karta kredytowa rodziców, dostajesz o 25% więcej pieniędzy")
materac = przedmiot("materac", 1.20, "W końcu nie będe musiał spać na podłodze, +20% do zdrowia")
piwo = przedmiot("piwo", False, "Tanie, ale kopie")
kwiaty = przedmiot("kwiaty", False, "Bezużyteczne zielsko, ale może sie kiedyś przydać")
gaz_pieprzowy = przedmiot("gaz pieprzowy", False, "Ach te lata 40..")
klucz_francuski = przedmiot("klucz francuski", False, "Niech sie sypie, działa na zasadzie im mocniej tym lepiej")
kamizelka_kuloodporna = przedmiot("kamizelka kuloodporna", False, "Na wypadek spotkania z irytującymi sąsiadami")


def menel(itemy, postac):
    write("Napotykasz nieznajomą twarz, okazuje się, że jest to żul mietek", end='')
    write("Prosi cie o drobny datek", end='')
    if len(itemy) > 0:
        write("Czy chcesz dać panu mietkowi jakiś przedmiot?", end='')
        if mistakes3() == 'tak':
            wybor_menel = mistakes2(itemy)
            write("Dajesz panu mietkowi: " + wybor_menel + " Napewno dobrze cie zapamięta", end='')
            itemy.remove(wybor_menel)
            return True
        else:
            write("Pan mietek odchodzi bez niczego", end='')
            return False
    elif len(itemy) == 0 and postac.pieniadze > 40:
        write("Czy chcesz dac panu mietkowi 40 zasobów pieniędzy?", end='')
        if mistakes3() == 'tak':
            postac.pieniadze -= 40
            write("Dajesz 40 pieniedzy, pan mietek bedzie mial dzisiaj dobry dzień, napewno dobrze cie zapamięta",
                  end='')
            return True
        else:
            write("Pan mietek odchodzi bez niczego", end='')
            return False
    else:
        write("Nie masz niczego do oddania żulowi..", end='')
        return False


def symulator_studenta():
    dzien = poziom = doswiadczenie = czy1 = czy2 = szczur = kot = poz1 = poz3 = 0
    itemy = []
    itemy_s = []
    pomogl_mietkowi = False
    write("\033[1m" + "Jesteś studentem." + "\033[0m", end='')
    write("Twoim celem jest przetrwanie jak największej ilości dni.", end='')
    write("W środku tygodnia tracisz zdrowie i zyskujesz naukę (pn-czw).", end='')
    write("W weekend zyskujesz zdrowie (pt-nd).", end='')
    write("Z każdym dniem wydajesz 5 zasobów pieniędzy na jedzenie i picie.", end='')
    time.sleep(1)
    print(
        "\nPostacie: " + "\033[33m" + "1. Intelektualista: " + "\033[34m" + "Nauka = 90, Zdrowie = 50, pieniądze: 80" + "\033[0m")
    print("\033[33m" + "          2. Banan: " + "\033[34m" + "Nauka = 60, Zdrowie = 60, pieniądze: 110" + "\033[0m")
    print("\033[33m" + "          3. Explorer: " + "\033[34m" + "Nauka = 45, Zdrowie = 90, pieniądze: 90" + "\033[0m")

    wybor = mistakes()

    if wybor == '1':
        postac = uczen("Intelektualista", 50, 90, 80)
    elif wybor == '2':
        postac = uczen("Banan", 60, 60, 110)
    elif wybor == "3":
        postac = uczen("Explorer", 90, 45, 90)

    while postac.zdrowie > 0 and postac.nauka > 0 and postac.pieniadze > 0:
        dzien += 1

        lista_dni = ["Niedziela", "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota"]
        for i in range(7):
            if dzien % 7 == i:
                dzien_tygodnia = lista_dni[i]

        if dzien == 6:  # spotkanie nerda
            write("Nerd cie zagaduje, chcesz z nim porozmawiać?", end='')
            if mistakes3() == 'tak':
                if random.randint(1, 11) == 3:
                    write("Jego niepojęta wiedza cie przerasta, tracisz 8 zdrowia, ale za to daje ci okulary", end='')
                    write("opis okularów: " + okulary.opis, end='')
                    itemy_s.append(okulary.napis)
                    postac.zdrowie -= 8
                    czy = 1
                else:
                    write("Jego niepojęta wiedza cie przerasta, odchodzisz w rozpaczy i tracisz 15 zdrowia", end='')
                    postac.zdrowie -= 15
                    czy = 0
            else:
                write(
                    "Odchodzisz, może porozmawiam z nim w przyszlości jak znajdzie prawdziwą pasję, poza kodowaniem w C++",
                    end='')
                czy = 0
        if dzien == 9:  # staż
            write("Masz szanse zrozumienia tajników sztuki naprawy samochodów.", end='')
            if mistakes3() == 'tak':
                write(
                    "Czy ktoś widział klucz francuski? Pytam dla zasady, bo zaczynam wątpić, czy istnieje poza legendami warsztatowymi.",
                    end='')
                write("zyskujesz klucz francuski", end='')
                write("Opis przedmioti: " + klucz_francuski.opis, end='')
                itemy.append(klucz_francuski.nazwa)
            else:
                write(
                    "Zapach smaru i oleju: Początkowo myślałem, że to zapach sukcesu, ale po chwili zastanowienia odmawiam.",
                    end='')

        if dzien == 13:
            write('Napotykasz czarnego kota, chcesz go wziąć jako swojego towarzysza?')
            if mistakes3() == 'tak':
                a = random.randint(3, 5)
                if a == 5:
                    write('Zostałeś podrapany przez tą małą wredote, tracisz 5 pkt zdrowia, ale kot uległ tobie.',
                          end='')
                    kot = 1
                    postac.zdrowie -= 5
                elif a == 4:
                    write("Niedość, że ten mały pchlarz cie podrapał to jeszcze uciekł, -5pkt do zdrowia", end='')
                    kot = 0
                    postac.zdrowie -= 5
                else:
                    write("Zdaje sie kot cie polubił", end='')
                    kot = 1
        if dzien == 17:  # spotkanie żula
            pomogl_mietkowi = menel(itemy, postac)

        if dzien == 25:  # spotkanie wroga
            write("Spotykasz zaciętego wroga, który wydaje się być wściekły", end='')
            if len(itemy) > 0:
                write("Czy chcesz użyć któregoś z posiadanych przedmiotów?", end='')
                if mistakes3() == 'tak':
                    wybor_wrog = mistakes2(itemy)
                    itemy.remove(wybor_wrog)
                else:
                    if pomogl_mietkowi == True:
                        write("Okazuje się, że pan mietek jest w okolicy.", end='')
                        write("Wdzięczny za twoją pomoc, jegomość decyduje się ci pomóc.", end='')
                        write("Oferuje ci swoją pomoc w zamian, a ty odchodzisz bez szwanku.", end='')
                        pomogl_mietkowi = False
                    else:
                        write("Wrogi jegomość nie ma zamiaru się z tobą łagodzić.", end='')
                        write("Jest agresywny i atakuje ciebie.", end='')
                        postac.zdrowie -= 30
                        write(f"Tracisz 30 punktów zdrowia. Obecne zdrowie: {postac.zdrowie}", end='')
            else:
                if pomogl_mietkowi == True:
                    write("Okazuje się, że pan mietek jest w okolicy.", end='')
                    write("Wdzięczny za twoją pomoc, jegomość decyduje się ci pomóc.", end='')
                    write("Oferuje ci swoją pomoc w zamian, a ty odchodzisz bez szwanku.", end='')
                    pomogl_mietkowi = False

                else:
                    write("Wrogi jegomość nie ma zamiaru się z tobą łagodzić.", end='')
                    write("Jest agresywny i atakuje ciebie.", end='')
                    postac.zdrowie -= 30
                    write(f"Tracisz 30 punktów zdrowia. Obecne zdrowie: {postac.zdrowie}", end='')

        if dzien == 30 and czy == 0:  # spotkanie nerda po raz 2
            write("Nerd nalega na rozmowe, chcesz porozmawiać?", end='')
            if mistakes3() == 'tak':
                write(
                    "Może i jego komunikatywność jest na poziomie zaawansowanego algorytmu, ale za to daje ci okulary",
                    end='')
                itemy_s.append(okulary.nazwa)
                write("opis okularów: " + okulary.opis, end='')
                czy = 1
            else:
                write(
                    "Nerd odchodzi, a śladem za nim zostają tylko kody kreskowe książek i mikropłatki zanurzone w kawie.",
                    end='')
                czy = 0
        if dzien == 40:
            write("W twoim pokoju zadomowił sie dużych rozmiarów szczur", end='')
            if kot == 1:
                write("Na szczęście ten mały czarny pchlarz rozprawił sie ze szczurem i możesz spać spokojnie.", end='')
            else:
                if len(itemy) > 0:
                    write("Czy chcesz sie rozprawić z tym gigantem?", end='')
                    if mistakes3() == 'tak':
                        write("Wybierz czym", end='')
                        wybor = mistakes2(itemy)
                        write("ten skurczybyk na szczęście chyba nie przetrwał", end='')
                        itemy.remove(wybor)
                    else:
                        write(
                            "Niestety.. nowy wspolokator nie płacący czynszu musi zostać. Z każdym dniem teraz tracisz 2pkt zdrowia i 3 pkt nauki.",
                            end='')
                        szczur = 1
                else:
                    write("Ten wstrętny szczur... Z każdym dniem teraz tracisz 2pkt zdrowia i 3 pkt nauki.", end='')
                    szczur = 1

        if dzien >= 50:
            if dzien == 50:
                print("\033[31m" + "Dzień 50.. Częstotliwość testów wzrasta." + "\033[0m")
            if dzien_tygodnia in ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek'] and random.randint(4,
                                                                                                    9) == 8 and dzien < 64:
                doswiadczenie_los = random.randint(50, 150)
                print(
                    "\033[31m" + "... Test!" + "\033[32m" + f'  Tracisz: 100 nauki, ale zyskujesz {doswiadczenie_los} doświadczenia' + '\033[0m')
                postac.nauka -= 100
                doswiadczenie += doswiadczenie_los
            if dzien == 64:
                print(
                    "\033[31m" + "Dzień 64.. Teraz tracisz 150 punktów nauki z testów, lecz ich częstotliwość maleje." + "\033[0m")
            if dzien_tygodnia in ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek'] and random.randint(1,
                                                                                                    10) == 8 and dzien >= 64:
                doswiadczenie_los = random.randint(75, 185)
                print(
                    "\033[31m" + "... Test!" + "\033[32m" + f'  Tracisz: 150 nauki, ale zyskujesz {doswiadczenie_los} doświadczenia' + '\033[0m')
                postac.nauka -= 150
                doswiadczenie += doswiadczenie_los

        else:
            if dzien_tygodnia in ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek'] and dzien > 10 and random.randint(1,
                                                                                                                   10) == 8:
                doswiadczenie_los = random.randint(50, 150)
                print(
                    "\033[31m" + "... Test!" + "\033[32m" + f'  Tracisz: 100 nauki, ale zyskujesz {doswiadczenie_los} doświadczenia' + '\033[0m')
                postac.nauka -= 100
                doswiadczenie += doswiadczenie_los
        if doswiadczenie >= 100:
            for i in range(4, 0, -1):
                if doswiadczenie >= 100 * i:
                    poziom += i
                    doswiadczenie -= 100 * i

        print("\n\033[1m" + f'Dzień {dzien}' + "\033[35m" + f' {dzien_tygodnia}:' + "\033[0m")

        print_loading_frame(doswiadczenie / 100)
        print()
        print("\033[33m" + f'Poziom bohatera: {poziom}')
        print()
        print("\033[34m" + f"Nauka: {postac.nauka}")
        print(f"Zdrowie: {postac.zdrowie}%")
        print(f"Zasoby: Pieniądze - {postac.pieniadze}" + "\033[0m")

        print("Co chciałbyś zrobić?")
        print("1. Nauka")
        print("2. Odpoczynek")
        print("3. Praca")

        wybor = mistakes()
        clear()
        if wybor == '2':
            losowy_zysk_zdrowia = random.randint(1, 15)
            if postac.zdrowie + losowy_zysk_zdrowia > 100:
                postac.zdrowie = 100
                print("\033[4m" + f"\nJesteś w pełni wypoczęty." + "\033[0m")
            else:
                postac.zdrowie += losowy_zysk_zdrowia
                print("\033[4m" + f"\nOdpoczywasz i zyskujesz {losowy_zysk_zdrowia} zdrowia." + "\033[0m")
        elif wybor == '1':
            losowa_ilosc_nauki = random.randint(1, 15)
            losowa_strata_zdrowia = random.randint(1, 5)
            postac.zdrowie -= losowa_strata_zdrowia
            if okulary.nazwa in itemy_s:
                postac.nauka += int(losowa_ilosc_nauki * okulary.efekt)
                print(
                    "\033[4m" + f"\nUczysz się i zyskujesz {int(losowa_ilosc_nauki * okulary.efekt)} nauki, ale tracisz {losowa_strata_zdrowia} zdrowia." + "\033[0m")
            else:
                postac.nauka += losowa_ilosc_nauki
                print(
                    "\033[4m" + f"\nUczysz się i zyskujesz {losowa_ilosc_nauki} nauki, ale tracisz {losowa_strata_zdrowia} zdrowia." + "\033[0m")
        elif wybor == '3':
            losowy_zysk_pieniedzy = random.randint(1, 20)
            postac.pieniadze += losowy_zysk_pieniedzy
            losowa_strata_zdrowia = random.randint(1, 5)
            postac.zdrowie -= losowa_strata_zdrowia
            losowy_zysk_doswiadczenia = random.randint(4, 10)
            doswiadczenie += losowy_zysk_doswiadczenia
            print(
                "\033[4m" + f"\nPracujesz i zyskujesz {losowy_zysk_pieniedzy} pieniędzy, {losowy_zysk_doswiadczenia} doświadczenia, ale tracisz {losowa_strata_zdrowia} zdrowia." + "\033[0m")

        if dzien % 7 >= 1 and dzien % 7 <= 4:
            postac.zdrowie -= 8
            postac.nauka += 5
        else:
            postac.zdrowie += 5
        postac.pieniadze -= 5

        if postac.nauka <= 0 and czy == 1:
            write("Zostałbyś wyrzucony z uczelni, gdyby nie nerd  który ci pomaga i daje korki +100pkt nauki.", end='')
            czy = 2

        if poziom >= 1 and czy1 == 0 and poz1 == 0:
            write('Twój poziom społeczny sie zwiększył, zyskujesz butelke piwa.', end='')
            itemy.append(piwo.nazwa)
            czy1 = 1
            poz1 = 1
        if poziom >= 3 and czy2 == 0 and poz3 == 0:
            write('Tak dalej a dziekan wreczy ci list gratulacyjny..', end='')
            p = random.randint(1, 2)
            czy = 1
            poz3 = 1
            if p == 1:
                write(
                    "Podczas przeszukiwania magazynu natrafiasz na tajemniczą skrzynię, a zamiast cennego skarbu, znajdujesz zestaw planszowy 'Gaz Pieprzowy: Edycja Patologiczna' oraz prawdziwy, nieużywany karton z gazem pieprzowym. Twoja przygoda nabiera absurdalnego smaku, gdy decydujesz się zabrać to nietypowe znalezisko ze sobą.",
                    end='')
                itemy.append(gaz_pieprzowy.nazwa)
                write("Opis przedmiotu: " + gaz_pieprzowy.opis, end='')
            if p == 2:
                write(
                    "Podczas eksploracji opuszczonej fabryki natrafiasz na kamizelkę kuloodporną w bardzo nietypowym kolorze tęczy. Zastanawiasz się, czy projektant miał na myśli ochronę przed kulami czy po prostu chciał stworzyć najbarwniejszą kamizelkę na świecie. Ostatecznie decydujesz się zabrać ją ze sobą, dodając nowy wymiar kolorów do swojego niezwykłego ekwipunku.",
                    end='')
                itemy.append(kamizelka_kuloodporna.nazwa)
                write("Opis przedmiotu: " + kamizelka_kuloodporna.opis, end='')
        if szczur == 1:
            postac.zdrowie -= 2
            postac.nauka -= 3

    if postac.nauka <= 0 and czy != 1:
        print("\033[31m" + "\nZostajesz wyrzucony z uczelni." + "\033[0m")
    if postac.zdrowie <= 0:
        print("\033[31m" + "\nUmierasz z przemęczenia." + "\033[0m")
    if postac.pieniadze <= 0:
        print("\033[31m" + "\nUmierasz z głodu." + "\033[0m")
    print("\033[31m" + f'Przetrwałeś {dzien} dni' + "\033[0m")


if __name__ == "__main__":
    symulator_studenta()
# rekord Mateusz Nowotka 191dni