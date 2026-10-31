# Basit Hesap Makinesi

Python ile yazılmış basit bir hesap makinesi. Toplama, çıkarma, çarpma ve bölme yapar.

## Tarayıcı arayüzü (kurulum gerektirmez)

```bash
python3 web_arayuz.py
```

Tarayıcınız kendiliğinden açılır. Açılmazsa terminalde yazan adresi (ör. `http://127.0.0.1:8000`) tarayıcınıza yapıştırın. Kapatmak için terminalde Ctrl+C'ye basın.

Fareyle düğmelere tıklayabilir ya da klavyeyi kullanabilirsiniz (rakamlar, `+ - * /`, Enter = sonuç, Backspace = sil, Esc = temizle).

- `web_arayuz.py`: Python'un kendi web sunucusu; hesabı yapar.
- `arayuz.html`: tarayıcıda görünen ekran ve düğmeler.

## Tkinter penceresi (isteğe bağlı)

```bash
python3 arayuz.py
```

Bu sürüm tkinter gerektirir. Linux'ta "No module named 'tkinter'" hatası alırsanız önce şunu çalıştırın:

```bash
sudo apt install python3-tk
```

## Terminal sürümü

```bash
python3 hesap_makinesi.py
```

Örnek:

```
İşlem seçin: +
Birinci sayı: 5
İkinci sayı: 3
Sonuç: 8
```

Çıkmak için `q` yazın.

## Testler

```bash
python -m unittest
```
