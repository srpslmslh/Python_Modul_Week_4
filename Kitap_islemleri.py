import json
import os
KITAP_DOSYASI="Kitap.json"

#Kitaplari Yukleme
def kitaplari_yukle():
    if os.path.exists(KITAP_DOSYASI):
        with open (KITAP_DOSYASI, "r") as file:
            return json.load(file)
    return []

#Kitaplari Kaydetme
def kitaplari_kaydet(kitaplar):
    with open (KITAP_DOSYASI, "w") as file:
        json.dump(kitaplar, file, indent=4)

#Menu
def kitap_menu():
    while True:
        print("\n****** KITAP ISLEMLERI ******")
        print("1. Kitaplari Listele")
        print("2. Kitap Ekle")
        print("3. Kitap Sil")
        print("4. Ana Menuye Don")
        secim=input("Seciminizi Yapiniz:")

        if secim=="1":
            kitaplari_listele()
        elif secim=="2":
            kitap_ekle()
        elif secim== "3":
            kitap_sil()
        elif secim=="4":
            break
        else:
            print("Gecersiz Secim! Tekrar Deneyiniz.")

#Kitaplari Listele
def kitaplari_listele():
    kitaplar=kitaplari_yukle()
    if not kitaplar:
        print("Kutuphanede Hic Kitap Yok!")
    else:
        print("Kayitli Kitaplar:")
        for kitap in kitaplar:
            print(f"-{kitap}")

#Kitap Eklemek
def kitap_ekle():
    yeni_kitap=input("Eklemek Istediginiz Kitabin Adini Giriniz:")
    kitaplar=kitaplari_yukle()
    kitaplar.append(yeni_kitap)
    kitaplari_kaydet(kitaplar)
    print(f"{yeni_kitap} Kutuphaneye Eklendi.")

#Kitap Sil
def kitap_sil():
    kitap_adi=input("Silmek Istediginiz Kitabin Adini Giriniz:")
    kitaplar=kitaplari_yukle()
    if kitap_adi in kitaplar:
        kitaplar.remove(kitap_adi)
        kitaplari_kaydet(kitaplar)
        print(f"{kitap_adi} Kutuphaneden silindi.")
    else:
        print(f"{kitap_adi} Kutuphanede Bulunamadi.")
