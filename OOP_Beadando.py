from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalasok = []

    def szabad_e(self, erkezes_datum, tavozas_datum):
        for foglalas in self.foglalasok:
            if not (foglalas['tavozas_datum'] < erkezes_datum or foglalas['erkezes_datum'] > tavozas_datum):
                return False
        return True

    def foglal(self, erkezes_datum, tavozas_datum):
        if self.szabad_e(erkezes_datum, tavozas_datum):
            self.foglalasok.append({'erkezes_datum': erkezes_datum, 'tavozas_datum': tavozas_datum})
            return f"Szoba {self.szobaszam} foglalása sikeres {erkezes_datum.strftime('%Y-%m-%d')} - {tavozas_datum.strftime('%Y-%m-%d')}."
        else:
            return f"Szoba {self.szobaszam} már foglalt ebben az időpontban."
    pass

    def foglalas_datumok(self):
        foglalasok_str_list = []
        for foglalas in self.foglalasok:
            erkezes_datum_str = foglalas['erkezes_datum'].strftime('%Y-%m-%d')
            tavozas_datum_str = foglalas['tavozas_datum'].strftime('%Y-%m-%d')
            foglalasok_str_list.append(f"{erkezes_datum_str} - {tavozas_datum_str}")
        return ", ".join(foglalasok_str_list)

    @abstractmethod
    def __str__(self):
        pass
class EgyagyasSzoba(Szoba):
    def __str__(self):
        foglalasok_str = self.foglalas_datumok()
        return f"Egy ágyas szoba száma: {self.szobaszam}, szoba ára: {self.ar}, Foglalások: {foglalasok_str if foglalasok_str else 'Üres'}"

class KetagyasSzoba(Szoba):
    def __str__(self):
        foglalasok_str = self.foglalas_datumok()
        return f"Két ágyas szoba száma: {self.szobaszam}, szoba ára: {self.ar}, Foglalások: {foglalasok_str if foglalasok_str else 'Üres'}"
    
class HaromagyasSzoba(Szoba):
    def __str__(self):
        foglalasok_str = self.foglalas_datumok()
        return f"Három ágyas szoba száma: {self.szobaszam}, szoba ára: {self.ar}, Foglalások: {foglalasok_str if foglalasok_str else 'Üres'}"

class Szalloda:
    def __init__(self):
        self.szobak = []

    def szoba_hozzaadas(self, szoba: Szoba):
        self.szobak.append(szoba)

    def adatfeltoltes(self):
        self.szoba_hozzaadas(EgyagyasSzoba(1, 40000))
        self.szoba_hozzaadas(KetagyasSzoba(2, 60000))
        self.szoba_hozzaadas(HaromagyasSzoba(3, 80000))

    def foglalasok_lekerdezes(self):
        return '\n'.join(str(szoba) for szoba in self.szobak)

    def foglalas(self, szobaszam, erkezes_datum, tavozas_datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                return szoba.foglal(erkezes_datum, tavozas_datum)
        return "Szoba nem található."

def foglalasi_folyamat(szalloda: Szalloda):
    szalloda.adatfeltoltes()

    while True:
        valasztas = input("Mit szeretne tenni? (foglalások, foglalás, kilépés): ")
        if valasztas == "foglalások":
            print(szalloda.foglalasok_lekerdezes())
        elif valasztas == "foglalás":
            while True:
                try:
                    szobaszam = int(input("Adja meg a szobának a számát: "))
                    break
                except ValueError:
                    print("Nem adott meg, vagy nem helyes szoba számot adott meg!")
            erkezes_datum_str = input("Adja meg az érkezési dátumot (yyyy-mm-dd): ")
            tavozas_datum_str = input("Adja meg a távozás dátumát (yyyy-mm-dd): ")
            erkezes_datum = datetime.strptime(erkezes_datum_str, '%Y-%m-%d')
            tavozas_datum = datetime.strptime(tavozas_datum_str, '%Y-%m-%d')
            print(szalloda.foglalas(szobaszam, erkezes_datum, tavozas_datum))
        elif valasztas == "kilépés":
            print("Viszlát!")
            break
        else:
            print("Érvénytelen parancs.")

szalloda = Szalloda()
foglalasi_folyamat(szalloda)