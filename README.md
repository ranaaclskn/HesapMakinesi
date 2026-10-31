# Basit Hesap Makinesi

Python ile yazılmış, komut satırında çalışan basit bir hesap makinesi. Toplama, çıkarma, çarpma ve bölme yapar.

## Pencereli arayüz

```bash
python3 arayuz.py
```

Fareyle düğmelere tıklayabilir ya da klavyeyi kullanabilirsiniz (rakamlar, `+ - * /`, Enter = sonuç, Backspace = sil, Esc = temizle).

Linux'ta "No module named 'tkinter'" hatası alırsanız önce şunu çalıştırın:

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
