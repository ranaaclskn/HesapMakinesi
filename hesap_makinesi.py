"""Basit komut satırı hesap makinesi."""


def topla(a, b):
    return a + b


def cikar(a, b):
    return a - b


def carp(a, b):
    return a * b


def bol(a, b):
    if b == 0:
        raise ZeroDivisionError("Sıfıra bölme yapılamaz.")
    return a / b


ISLEMLER = {
    "+": topla,
    "-": cikar,
    "*": carp,
    "/": bol,
}


def hesapla(a, islem, b):
    if islem not in ISLEMLER:
        raise ValueError(f"Geçersiz işlem: {islem}")
    return ISLEMLER[islem](a, b)


def sayi_al(mesaj):
    while True:
        deger = input(mesaj).strip().replace(",", ".")
        try:
            return float(deger)
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")


def main():
    print("Basit Hesap Makinesi")
    print("İşlemler: +  -  *  /   (çıkmak için 'q')")
    while True:
        islem = input("\nİşlem seçin: ").strip()
        if islem.lower() == "q":
            print("Görüşmek üzere!")
            break
        if islem not in ISLEMLER:
            print("Geçersiz işlem. +, -, * veya / girin.")
            continue
        a = sayi_al("Birinci sayı: ")
        b = sayi_al("İkinci sayı: ")
        try:
            sonuc = hesapla(a, islem, b)
        except ZeroDivisionError as hata:
            print(f"Hata: {hata}")
            continue
        if sonuc == int(sonuc):
            sonuc = int(sonuc)
        print(f"Sonuç: {sonuc}")


if __name__ == "__main__":
    main()
