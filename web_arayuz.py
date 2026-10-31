"""
Hesap makinesinin TARAYICIDA açılan arayüzü.

Çalıştırmak için:  python3 web_arayuz.py

Hiçbir ek kurulum gerekmez: burada kullanılan her şey Python ile birlikte
gelir. Program bilgisayarınızda küçük bir web sunucusu başlatır ve
tarayıcınızı otomatik olarak açar. Kapatmak için terminalde Ctrl+C'ye basın.

Nasıl çalışır?
    1. arayuz.html dosyası, tarayıcıda gördüğünüz düğmeleri ve ekranı çizer.
    2. "=" ya da bir işlem tuşuna basınca sayfa, bu Python programına
       "şu iki sayıyla şu işlemi yap" diye bir istek gönderir.
    3. Bu program, hesap_makinesi.py içindeki `hesapla` fonksiyonuyla
       sonucu bulur ve sayfaya geri yollar.
    Yani matematik Python'da, görünüş tarayıcıda yapılıyor.
"""

# Aşağıdakilerin hepsi Python'un standart kütüphanesinden gelir (kurulum yok).
import json                                   # Python verisini sayfanın anlayacağı metne çevirir
import webbrowser                             # varsayılan tarayıcıyı açar
from http.server import BaseHTTPRequestHandler, HTTPServer   # basit web sunucusu
from pathlib import Path                      # dosya yollarıyla çalışmak için
from urllib.parse import parse_qs, urlparse   # adres çubuğundaki bilgileri okur

from hesap_makinesi import hesapla            # kendi hesaplama fonksiyonumuz

# arayuz.html dosyası bu Python dosyasıyla aynı klasörde duruyor.
# __file__ bu dosyanın yerini verir; .parent onun bulunduğu klasördür.
HTML_DOSYASI = Path(__file__).parent / "arayuz.html"


class IstekIsleyici(BaseHTTPRequestHandler):
    """
    Tarayıcıdan gelen her isteği karşılayan sınıf.

    Tarayıcı bir adres istediğinde (GET isteği) do_GET fonksiyonu çalışır.
    İki adresimiz var:
        /                 -> hesap makinesi sayfasını gönder
        /hesapla?a=..&islem=..&b=..  -> hesabı yap, sonucu gönder
    """

    def do_GET(self):
        # urlparse adresi parçalarına ayırır: ör. "/hesapla?a=5&islem=%2B&b=3"
        # adresinde path "/hesapla", query ise "a=5&islem=%2B&b=3" olur.
        adres = urlparse(self.path)

        if adres.path == "/":
            self.sayfayi_gonder()
        elif adres.path == "/hesapla":
            self.hesapla_ve_gonder(adres.query)
        else:
            # Bilmediğimiz bir adres istendiyse "404 bulunamadı" diyoruz.
            self.send_error(404, "Sayfa bulunamadı")

    def sayfayi_gonder(self):
        """arayuz.html dosyasını okuyup tarayıcıya yollar."""
        icerik = HTML_DOSYASI.read_bytes()
        self.cevap_gonder(200, "text/html; charset=utf-8", icerik)

    def hesapla_ve_gonder(self, sorgu):
        """Sayfadan gelen sayıları hesaplar, sonucu JSON olarak geri yollar."""
        # parse_qs "a=5&islem=%2B&b=3" metnini
        # {"a": ["5"], "islem": ["+"], "b": ["3"]} sözlüğüne çevirir.
        parametreler = parse_qs(sorgu)

        # try/except: bir şey ters giderse program çökmesin, hata mesajı dönsün.
        try:
            a = float(parametreler["a"][0])
            b = float(parametreler["b"][0])
            islem = parametreler["islem"][0]
            veri = {"sonuc": hesapla(a, islem, b)}
        except ZeroDivisionError:
            veri = {"hata": "Sıfıra bölünemez"}
        except (KeyError, ValueError):
            veri = {"hata": "Geçersiz giriş"}

        # JSON: tarayıcının (JavaScript'in) kolayca okuyabildiği veri biçimi.
        # Örnek çıktı: {"sonuc": 8.0}
        icerik = json.dumps(veri).encode("utf-8")
        self.cevap_gonder(200, "application/json", icerik)

    def cevap_gonder(self, kod, tur, icerik):
        """Tarayıcıya bir cevap gönderir: önce başlık bilgileri, sonra içerik."""
        self.send_response(kod)                       # 200 = "her şey yolunda"
        self.send_header("Content-Type", tur)         # gönderilen şeyin türü
        self.send_header("Content-Length", str(len(icerik)))
        self.end_headers()
        self.wfile.write(icerik)

    def log_message(self, *args):
        # Sunucu normalde her isteği terminale yazar. Ekran kalabalık olmasın
        # diye bu fonksiyonu boş bırakarak o yazıları kapatıyoruz.
        pass


def main():
    # "127.0.0.1" sadece kendi bilgisayarınızdan erişilebilir demektir;
    # başkaları ağ üzerinden bu sayfaya ulaşamaz.
    # Port olarak 8000'i deniyoruz; doluysa 0 veriyoruz, yani
    # "boş olan herhangi bir portu seç" diyoruz.
    try:
        sunucu = HTTPServer(("127.0.0.1", 8000), IstekIsleyici)
    except OSError:
        sunucu = HTTPServer(("127.0.0.1", 0), IstekIsleyici)

    adres = f"http://127.0.0.1:{sunucu.server_port}"
    print(f"Hesap makinesi açıldı: {adres}")
    print("Tarayıcı kendiliğinden açılmazsa bu adresi tarayıcınıza yapıştırın.")
    print("Kapatmak için Ctrl+C'ye basın.")

    webbrowser.open(adres)

    # serve_forever: sunucuyu sürekli açık tutar ve gelen istekleri bekler.
    # Ctrl+C'ye basılınca KeyboardInterrupt hatası oluşur; onu yakalayıp
    # programı düzgünce kapatıyoruz.
    try:
        sunucu.serve_forever()
    except KeyboardInterrupt:
        print("\nHesap makinesi kapatıldı.")
        sunucu.server_close()


if __name__ == "__main__":
    main()
