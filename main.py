import Kitap_islemleri
import uye_islemleri

def main():
    while True:
        print("\n*** KUTUPHANE SISTEMI ***")
        print("1. Kitap Islemleri")
        print("2. Uye Islemleri")
        print("3. Cikis")
        secim = input("Seciminizi Yapin: ")

        if secim == "1":
            Kitap_islemleri.kitap_menu()
        elif secim == "2":
            uye_islemleri.uye_menu()
        elif secim == "3":
            print("Cikis Yapiliyor...")
            break
        else:
            print("Gecersiz Secim! Tekrar Deneyin.")

if __name__ == "__main__":
    main()
