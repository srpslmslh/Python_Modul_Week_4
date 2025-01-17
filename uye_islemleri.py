from datetime import datetime, timedelta
import json
import os


UYE_DOSYASI = "Uye.json"
KITAP_DOSYASI = "Kitap.json"
TAKIP_DOSYASI = "Takip.json"


# Üyeleri yükleme
def uyeleri_yukle():
    if os.path.exists(UYE_DOSYASI):
        with open(UYE_DOSYASI, "r") as file:
            return json.load(file)
    return []


# Üyeleri kaydetme
def uyeleri_kaydet(uyeler):
    with open(UYE_DOSYASI, "w") as file:
        json.dump(uyeler, file, indent=4)


# Kitapları yükleme
def kitaplari_yukle():
    if os.path.exists(KITAP_DOSYASI):
        with open(KITAP_DOSYASI, "r") as file:
            print (json.load(file))
    return []


# Kitapları kaydetme
def kitaplari_kaydet(kitaplar):
    with open(KITAP_DOSYASI, "w") as file:
        json.dump(kitaplar, file, indent=4)


# Takip dosyasını yükleme
def takip_yukle():
    if os.path.exists(TAKIP_DOSYASI):
        with open(TAKIP_DOSYASI, "r", encoding='utf-8') as file:
            return json.load(file)
    return {}


# Takip dosyasını kaydetme
def takip_kaydet(takip):
    with open(TAKIP_DOSYASI, "w", encoding='utf-8') as file:
        json.dump(takip, file, indent=4, ensure_ascii=False)


# Menü
def uye_menu():
    while True:
        print("\n****** UYE ISLEMLERI ******")
        print("1. Uyeleri Listele")
        print("2. Uye Ekle")
        print("3. Uye Sil")
        print("4. Uye Kontrolu")
        print("5. Uyeye Kitap Ver")
        print("6. Uyeden Kitap Al")
        print("7. Odunc Verilen Kitapları Listele")  
        print("8. Ana Menuye Don")
        secim = input("Seciminizi Yapin: ")

        if secim == "1":
            uyeleri_listele()
        elif secim == "2":
            uye_ekle()
        elif secim == "3":
            uye_sil()
        elif secim == "4":
            uye_kontrol()
        elif secim == "5":
            uye_id = input("Uyenin ID'sini Giriniz: ")
            kitap_adi = input('Vereceginiz Kitabin Adini Giriniz: ')
            uyeye_kitap_ver(uye_id, kitap_adi)
        elif secim == "6":
            uye_id = input("Uyenin ID'sini Giriniz: ")
            kitap_adi = input("Aldiginiz Kitabin Adini Giriniz: ")
            uyeden_kitap_al(uye_id, kitap_adi)
        elif secim == "7":  
            takip_listesini_goster()
        elif secim == "8":
            break
        else:
            print("Gecersiz secim! Tekrar deneyin.")


# Üyeleri listele
def uyeleri_listele():
    uyeler = uyeleri_yukle()
    takip = takip_yukle()  
    if not uyeler:
        print("Kutuphanede hic uye yok.")
    else:
        print("Kayitli Uyeler:")
        for uye in uyeler:
            # Üyenin aldığı kitapları takip dosyasından al
            uye_kitaplar = [kitap['kitap'] for kitap in takip.get(str(uye['id']), [])]

            # Kitaplar listesi boşsa "Hiç kitap alınmamış" yazalım
            if uye_kitaplar:
                kitaplar_listesi = ", ".join(uye_kitaplar)
            else:
                kitaplar_listesi = "Hic kitap alinmamis"

            print(f"ID: {uye['id']}, Ad: {uye['ad']}, Kitaplar: {kitaplar_listesi}")

# Üye ekle
def uye_ekle():
    uyeler = uyeleri_yukle()
    yeni_uye_adi = input("Eklemek istediginiz uyenin adini girin: ")
    yeni_uye_id = len(uyeler) + 1
    uyeler.append({"id": yeni_uye_id, "ad": yeni_uye_adi, "kitaplar": []})
    uyeleri_kaydet(uyeler)
    print(f"{yeni_uye_adi} (ID: {yeni_uye_id}) kutuphaneye eklendi.")


# Üye sil
def uye_sil():
    uye_id = input("Silmek istediginiz uyenin ID numarasini girin: ")
    uyeler = uyeleri_yukle()
    uyeler = [uye for uye in uyeler if str(uye["id"]) != uye_id]
    uyeleri_kaydet(uyeler)
    print(f"ID {uye_id} uyelikten silindi.")


# Üye kontrolü
def uye_kontrol():
    uye_id = input("Kontrol etmek istediginiz uyenin ID numarasini girin: ")
    uyeler = uyeleri_yukle()
    uye = next((uye for uye in uyeler if str(uye["id"]) == uye_id), None)
    if uye:
        print(f"Uye Bulundu: ID: {uye['id']}, Ad: {uye['ad']}, Kitaplar: {uye['kitaplar']}")
    else:
        print(f"ID {uye_id} ile eslesen uye bulunamadı.")


# Üyeye kitap ver
def uyeye_kitap_ver(uye_id, kitap_adi):
    kitaplar = kitaplari_yukle()
    takip = takip_yukle()

    # Kitap başka bir üyede mi kontrol et
    for mevcut_uye, kitaplar_listesi in takip.items():
        if kitap_adi in [kitap['kitap'] for kitap in kitaplar_listesi]:
            print(f"Bu kitap su anda Uye ID {mevcut_uye}'de.")
            return

    # Kitap kütüphanede mevcut mu kontrol et
    if kitap_adi not in kitaplar:
        print("Bu kitap kutuphanede mevcut degil.")
        return

    # Kitap ödünç verilme tarihi ve geri getirme tarihi
    geri_getirme_tarihi = (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d")

    # Kitapları takip dosyasına kaydet
    if uye_id not in takip:
        takip[uye_id] = []
    takip[uye_id].append({"kitap": kitap_adi, "geri_getirme_tarihi": geri_getirme_tarihi})

    # Kitap kütüphaneden çıkarılıyor
    kitaplar.remove(kitap_adi)
    kitaplari_kaydet(kitaplar)

    # Takip dosyasına kaydet
    takip_kaydet(takip)
    print(f"{kitap_adi} kitabi Uye ID {uye_id}'ye odunc verilmistir. Geri getirme tarihi: {geri_getirme_tarihi}.")


# Üyeden kitap al
def uyeden_kitap_al(uye_id, kitap_adi):
    takip = takip_yukle()

    # Üye mevcut mu ve kitap üyenin listesinde mi kontrol et
    if uye_id in takip:
        kitaplar_listesi = [kitap for kitap in takip[uye_id] if kitap["kitap"] == kitap_adi]
        if kitaplar_listesi:
            kitap = kitaplar_listesi[0]
            geri_getirme_tarihi = datetime.strptime(kitap["geri_getirme_tarihi"], "%Y-%m-%d")
            if datetime.now() > geri_getirme_tarihi:
                print(f"Kitap gecikmeli! {geri_getirme_tarihi} tarihinde geri getirilmesi gerekiyordu.")
            else:
                print(f"Kitap zamanında geri getirildi.")

            # Kitap alındıktan sonra takipten ve kitap listesinden çıkarılıyor
            takip[uye_id] = [kitap for kitap in takip[uye_id] if kitap["kitap"] != kitap_adi]
            kitaplar = kitaplari_yukle()
            kitaplar.append(kitap_adi)
            kitaplari_kaydet(kitaplar)

            # Takip dosyasını güncelle
            takip_kaydet(takip)
            print(f"{kitap_adi} kitabi Uye ID {uye_id}'den alindi ve kutuphaneye geri eklendi.")
        else:
            print(f"Uye ID {uye_id} bu kitabi odunc almamis.")


# Ödünç Verilen Kitapları Listele
def takip_listesini_goster():
    takip = takip_yukle()
    if not takip:
        print("Hicbir kitap odunc verilmemis.")
    else:
        print("Odunc Verilen Kitaplar ve Uyeler:")
        for uye_id, kitaplar_listesi in takip.items():
            print(f"Uye ID: {uye_id}")
            for kitap in kitaplar_listesi:
                print(f"  Kitap: {kitap['kitap']}, Geri Getirme Tarihi: {kitap['geri_getirme_tarihi']}")

