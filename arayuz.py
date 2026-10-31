"""
Hesap makinesinin pencereli (grafik) arayüzü.

Çalıştırmak için:  python3 arayuz.py

Bu dosya sadece "görünüşten" sorumludur: düğmeleri çizer, tıklamaları ve
klavyeyi dinler, ekrana sonuç yazar. Asıl matematik işlemleri (toplama,
bölme vb.) hesap_makinesi.py dosyasındaki `hesapla` fonksiyonunda yapılır.
Böylece hesaplama kodunu bir kere yazıp hem terminal sürümünde hem de bu
pencereli sürümde kullanmış oluyoruz.
"""

# tkinter: Python ile birlikte gelen, pencere ve düğme çizmeye yarayan kütüphane.
import tkinter as tk

# Kendi yazdığımız hesaplama fonksiyonunu diğer dosyadan alıyoruz.
from hesap_makinesi import hesapla


# ---------------------------------------------------------------------------
# RENKLER VE YAZI TİPLERİ
# Tüm renkleri en üstte tek bir yerde topladık. Arayüzün rengini değiştirmek
# isterseniz sadece buradaki değerleri değiştirmeniz yeterli.
# Renkler "#RRGGBB" biçiminde yazılır (kırmızı-yeşil-mavi, onaltılık sayı).
# ---------------------------------------------------------------------------
ARKA_PLAN = "#1e1f26"        # pencerenin koyu arka planı
EKRAN_YAZI = "#ffffff"       # büyük sonuç yazısının rengi
GECMIS_YAZI = "#8b8fa3"      # üstteki küçük "5 +" yazısının rengi

RAKAM_RENK = "#2c2e3a"       # rakam düğmeleri (0-9, virgül)
RAKAM_UZERINDE = "#3a3d4d"   # fare rakam düğmesinin üzerine gelince
ISLEM_RENK = "#ff9f43"       # işlem düğmeleri (+ − × ÷)
ISLEM_UZERINDE = "#ffb36b"
OZEL_RENK = "#4b4e5e"        # C, ⌫, % düğmeleri
OZEL_UZERINDE = "#5d6072"
ESITTIR_RENK = "#10ac84"     # yeşil "=" düğmesi
ESITTIR_UZERINDE = "#1dd1a1"

YAZI_TIPI = "Helvetica"


class HesapMakinesiArayuzu:
    """
    Bütün pencereyi temsil eden sınıf.

    "Sınıf" (class), birbiriyle ilgili verileri ve fonksiyonları bir arada
    tutan bir kalıptır. Burada hem hesap makinesinin hafızası (ekrandaki
    sayı, seçilen işlem...) hem de düğmelere basınca ne olacağı bir arada.
    """

    def __init__(self, pencere):
        # __init__ sınıftan bir nesne oluşturulduğunda ilk çalışan fonksiyondur.
        # Pencerenin ayarlarını yapıyor ve hafızayı sıfırlıyoruz.
        self.pencere = pencere
        self.pencere.title("Hesap Makinesi")
        self.pencere.configure(bg=ARKA_PLAN)
        self.pencere.resizable(False, False)  # pencere boyutu sabit kalsın

        # --- HESAP MAKİNESİNİN HAFIZASI ---
        # mevcut:     şu anda ekranda yazılan sayı (metin olarak tutuyoruz,
        #             çünkü kullanıcı rakamları tek tek ekliyor)
        # ilk_sayi:   bir işlem tuşuna basılmadan önce girilen sayı
        # islem:      seçilen işlem ("+", "-", "*", "/") ya da henüz yoksa None
        # yeni_sayi:  True ise bir sonraki rakam ekrandaki sayıyı silip
        #             yeni bir sayı başlatır (ör. "+" ya da "=" basıldıktan sonra)
        self.mevcut = "0"
        self.ilk_sayi = None
        self.islem = None
        self.yeni_sayi = False

        # tk.StringVar: ekrandaki yazıya bağlı özel bir değişken.
        # Bu değişkeni değiştirdiğimizde ekrandaki yazı kendiliğinden güncellenir.
        self.ekran_metni = tk.StringVar(value="0")
        self.gecmis_metni = tk.StringVar(value="")

        self.ekrani_olustur()
        self.dugmeleri_olustur()
        self.klavyeyi_bagla()

    # -----------------------------------------------------------------------
    # ARAYÜZÜ ÇİZEN FONKSİYONLAR
    # -----------------------------------------------------------------------

    def ekrani_olustur(self):
        """Üst kısımdaki sonuç ekranını çizer."""
        # Frame: diğer parçaları içine koyduğumuz görünmez bir kutu.
        ekran = tk.Frame(self.pencere, bg=ARKA_PLAN, padx=20, pady=20)
        ekran.pack(fill="x")  # kutuyu pencerenin üstüne, tam genişlikte yerleştir

        # Label: ekrana yazı yazan parça. anchor="e" yazıyı sağa (east) yaslar,
        # tıpkı gerçek hesap makinelerinde olduğu gibi.
        tk.Label(
            ekran, textvariable=self.gecmis_metni, anchor="e",
            bg=ARKA_PLAN, fg=GECMIS_YAZI, font=(YAZI_TIPI, 14),
        ).pack(fill="x")

        tk.Label(
            ekran, textvariable=self.ekran_metni, anchor="e",
            bg=ARKA_PLAN, fg=EKRAN_YAZI, font=(YAZI_TIPI, 40, "bold"),
        ).pack(fill="x")

    def dugmeleri_olustur(self):
        """Düğmeleri 4 sütunlu bir ızgara (grid) halinde dizer."""
        izgara = tk.Frame(self.pencere, bg=ARKA_PLAN, padx=12, pady=12)
        izgara.pack()

        # Her satır bir liste. Her düğme için:
        #   (üzerindeki yazı, türü, kaç sütun genişliğinde olacağı)
        # Ekranda "×" ve "÷" gibi güzel simgeler gösteriyoruz; arka planda
        # bunları hesapla fonksiyonunun anladığı "*" ve "/" işaretlerine çeviriyoruz.
        duzen = [
            [("C", "ozel", 1), ("⌫", "ozel", 1), ("%", "ozel", 1), ("÷", "islem", 1)],
            [("7", "rakam", 1), ("8", "rakam", 1), ("9", "rakam", 1), ("×", "islem", 1)],
            [("4", "rakam", 1), ("5", "rakam", 1), ("6", "rakam", 1), ("−", "islem", 1)],
            [("1", "rakam", 1), ("2", "rakam", 1), ("3", "rakam", 1), ("+", "islem", 1)],
            [("0", "rakam", 2), (",", "rakam", 1), ("=", "esittir", 1)],
        ]

        # İki iç içe döngü: dış döngü satırları, iç döngü o satırdaki düğmeleri
        # gezer. enumerate() hem sırayı (0, 1, 2...) hem de elemanı verir.
        for satir_no, satir in enumerate(duzen):
            sutun_no = 0
            for yazi, tur, genislik in satir:
                dugme = self.dugme_yap(izgara, yazi, tur)
                # grid: düğmeyi ızgarada belirtilen satır ve sütuna koyar.
                # columnspan=2 olan "0" düğmesi iki sütun kaplar.
                # sticky="nsew" düğmenin hücreyi tamamen doldurmasını sağlar.
                dugme.grid(
                    row=satir_no, column=sutun_no, columnspan=genislik,
                    sticky="nsew", padx=5, pady=5,
                )
                sutun_no += genislik

        # Tüm sütunlar ve satırlar aynı boyutta olsun diye ağırlık veriyoruz.
        for i in range(4):
            izgara.columnconfigure(i, weight=1, minsize=80)
        for i in range(len(duzen)):
            izgara.rowconfigure(i, weight=1, minsize=70)

    def dugme_yap(self, ust, yazi, tur):
        """Tek bir düğme oluşturur; rengini türüne göre seçer."""
        renkler = {
            "rakam": (RAKAM_RENK, RAKAM_UZERINDE),
            "islem": (ISLEM_RENK, ISLEM_UZERINDE),
            "ozel": (OZEL_RENK, OZEL_UZERINDE),
            "esittir": (ESITTIR_RENK, ESITTIR_UZERINDE),
        }
        normal, uzerinde = renkler[tur]

        # Düğme olarak tk.Label kullanıyoruz, çünkü tk.Button bazı işletim
        # sistemlerinde arka plan rengini görmezden geliyor. Label'a tıklama
        # özelliğini aşağıda kendimiz ekliyoruz.
        dugme = tk.Label(
            ust, text=yazi, bg=normal, fg="#ffffff",
            font=(YAZI_TIPI, 20), cursor="hand2",
        )

        # bind: bir olay olduğunda çalışacak fonksiyonu bağlar.
        #   <Button-1> = sol fare tıklaması
        #   <Enter>    = fare düğmenin üzerine geldi
        #   <Leave>    = fare düğmenin üzerinden çıktı
        # lambda: tek satırlık, isimsiz küçük bir fonksiyon. "y=yazi" kısmı,
        # her düğmenin kendi yazısını hatırlaması için gerekli.
        dugme.bind("<Button-1>", lambda olay, y=yazi: self.dugmeye_basildi(y))
        dugme.bind("<Enter>", lambda olay: dugme.configure(bg=uzerinde))
        dugme.bind("<Leave>", lambda olay: dugme.configure(bg=normal))
        return dugme

    def klavyeyi_bagla(self):
        """Hesap makinesini klavyeden de kullanabilmek için tuşları bağlar."""
        # Her klavye tuşunu, ekrandaki karşılığı olan düğmeye eşliyoruz.
        tuslar = {
            "+": "+", "-": "−", "*": "×", "/": "÷",
            "%": "%", ",": ",", ".": ",",
            "Return": "=", "KP_Enter": "=", "equal": "=",
            "BackSpace": "⌫", "Escape": "C", "Delete": "C",
            # Sayısal tuş takımındaki (sağ taraftaki) işlem tuşları:
            "KP_Add": "+", "KP_Subtract": "−",
            "KP_Multiply": "×", "KP_Divide": "÷", "KP_Decimal": ",",
        }

        def tusa_basildi(olay):
            # olay.char basılan karakteri, olay.keysym tuşun adını verir.
            if olay.char.isdigit():
                self.dugmeye_basildi(olay.char)
            elif olay.keysym in tuslar:
                self.dugmeye_basildi(tuslar[olay.keysym])
            elif olay.char in tuslar:
                self.dugmeye_basildi(tuslar[olay.char])

        self.pencere.bind("<Key>", tusa_basildi)

    # -----------------------------------------------------------------------
    # DÜĞMELERE BASINCA NE OLACAĞINI BELİRLEYEN FONKSİYONLAR
    # -----------------------------------------------------------------------

    def dugmeye_basildi(self, yazi):
        """Hangi düğmeye basıldığına bakıp ilgili fonksiyona yönlendirir."""
        if yazi.isdigit():
            self.rakam_ekle(yazi)
        elif yazi == ",":
            self.virgul_ekle()
        elif yazi in ("+", "−", "×", "÷"):
            self.islem_sec(yazi)
        elif yazi == "=":
            self.esittir()
        elif yazi == "C":
            self.temizle()
        elif yazi == "⌫":
            self.son_rakami_sil()
        elif yazi == "%":
            self.yuzde()
        self.ekrani_guncelle()

    def rakam_ekle(self, rakam):
        # Yeni bir sayı başlıyorsa ya da ekranda sadece "0" ya da bir hata
        # mesajı varsa, eski yazıyı silip rakamı tek başına yazıyoruz.
        if self.yeni_sayi or self.mevcut in ("0", "Hata"):
            self.mevcut = rakam
            self.yeni_sayi = False
        elif len(self.mevcut) < 15:  # ekrana sığmayacak kadar uzamasın
            self.mevcut += rakam

    def virgul_ekle(self):
        # Programın içinde ondalık ayırıcı olarak nokta (".") kullanıyoruz,
        # çünkü Python sayıları öyle anlar. Ekranda ise virgül gösteriyoruz.
        if self.yeni_sayi or self.mevcut == "Hata":
            self.mevcut = "0."
            self.yeni_sayi = False
        elif "." not in self.mevcut:  # bir sayıda iki virgül olamaz
            self.mevcut += "."

    def islem_sec(self, simge):
        # Ekrandaki simgeyi hesapla fonksiyonunun anladığı işarete çeviriyoruz.
        cevir = {"+": "+", "−": "-", "×": "*", "÷": "/"}

        # Kullanıcı zincirleme işlem yapıyorsa (ör. 2 + 3 + ...) ve ikinci
        # sayıyı girmişse, önce önceki işlemi hesaplıyoruz. Böylece ikinci
        # "+" tuşuna basıldığında ekranda 5 görünür.
        if self.islem is not None and not self.yeni_sayi:
            self.esittir()
            if self.mevcut == "Hata":
                return

        self.ilk_sayi = float(self.mevcut)
        self.islem = cevir[simge]
        self.yeni_sayi = True
        self.gecmis_metni.set(f"{self.goster(self.mevcut)} {simge}")

    def esittir(self):
        # Henüz bir işlem seçilmediyse yapılacak bir şey yok.
        if self.islem is None:
            return

        ikinci_sayi = float(self.mevcut)
        simgeler = {"+": "+", "-": "−", "*": "×", "/": "÷"}
        self.gecmis_metni.set(
            f"{self.goster(self.sayiyi_metne(self.ilk_sayi))} "
            f"{simgeler[self.islem]} {self.goster(self.mevcut)} ="
        )

        # try/except: hata çıkabilecek bir işlemi dener. Sıfıra bölme gibi
        # bir hata olursa program çökmek yerine "except" kısmı çalışır.
        try:
            sonuc = hesapla(self.ilk_sayi, self.islem, ikinci_sayi)
            self.mevcut = self.sayiyi_metne(sonuc)
        except ZeroDivisionError:
            self.mevcut = "Hata"
            self.gecmis_metni.set("Sıfıra bölünemez")

        self.ilk_sayi = None
        self.islem = None
        self.yeni_sayi = True

    def temizle(self):
        """C düğmesi: her şeyi başa döndürür."""
        self.mevcut = "0"
        self.ilk_sayi = None
        self.islem = None
        self.yeni_sayi = False
        self.gecmis_metni.set("")

    def son_rakami_sil(self):
        """⌫ düğmesi: son yazılan rakamı siler."""
        if self.yeni_sayi or self.mevcut == "Hata":
            return
        # [:-1] metnin son karakteri hariç hepsini alır.
        self.mevcut = self.mevcut[:-1]
        if self.mevcut in ("", "-"):
            self.mevcut = "0"

    def yuzde(self):
        """% düğmesi: ekrandaki sayıyı 100'e böler (ör. 50 -> 0,5)."""
        if self.mevcut == "Hata":
            return
        self.mevcut = self.sayiyi_metne(float(self.mevcut) / 100)
        self.yeni_sayi = True

    # -----------------------------------------------------------------------
    # YARDIMCI FONKSİYONLAR
    # -----------------------------------------------------------------------

    @staticmethod
    def sayiyi_metne(sayi):
        """Sayıyı ekrana yazılabilecek düzgün bir metne çevirir."""
        # Tam sayı ise (ör. 8.0) sonundaki ".0" kısmını atıyoruz -> "8".
        if sayi == int(sayi) and abs(sayi) < 1e15:
            return str(int(sayi))
        # Değilse en fazla 10 anlamlı basamak gösteriyoruz; böylece
        # 0.1 + 0.2 gibi işlemlerde 0.30000000000000004 yerine 0.3 görünür.
        return f"{sayi:.10g}"

    @staticmethod
    def goster(metin):
        """İçerideki noktalı yazımı, Türkçedeki gibi virgüllü yazıma çevirir."""
        return metin.replace(".", ",")

    def ekrani_guncelle(self):
        """Hafızadaki sayıyı ekrana yazar."""
        self.ekran_metni.set(self.goster(self.mevcut))


# Bu blok, dosya doğrudan çalıştırıldığında (python3 arayuz.py) devreye girer.
# Başka bir dosya bu dosyayı "import" ederse çalışmaz.
if __name__ == "__main__":
    pencere = tk.Tk()                 # boş bir pencere oluştur
    HesapMakinesiArayuzu(pencere)     # içine hesap makinesini yerleştir
    pencere.mainloop()                # pencereyi açık tut, tıklamaları bekle
