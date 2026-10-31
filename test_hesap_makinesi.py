import unittest

from hesap_makinesi import bol, carp, cikar, hesapla, topla


class HesapMakinesiTest(unittest.TestCase):
    def test_topla(self):
        self.assertEqual(topla(2, 3), 5)

    def test_cikar(self):
        self.assertEqual(cikar(10, 4), 6)

    def test_carp(self):
        self.assertEqual(carp(3, 4), 12)

    def test_bol(self):
        self.assertEqual(bol(10, 4), 2.5)

    def test_sifira_bolme(self):
        with self.assertRaises(ZeroDivisionError):
            bol(5, 0)

    def test_hesapla(self):
        self.assertEqual(hesapla(6, "*", 7), 42)

    def test_gecersiz_islem(self):
        with self.assertRaises(ValueError):
            hesapla(1, "%", 2)


if __name__ == "__main__":
    unittest.main()
