"""Günün sahnesini seçer: sahneler/ altındaki SVG'lerden biri, yılın gününe göre sırayla.

Çıktı: sahneler/gunun-sahnesi.svg (README bunu gösterir) ve README'deki
<!--sahne-->...<!--/sahne--> arasına bugünün sahnesinin adı.
Tarih argümanla verilebilir (test için): python scripts/gunun_sahnesi.py 2026-11-14
"""
import datetime
import pathlib
import re
import shutil
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
SAHNELER = [
    ("game-jam.svg", "Game jam görev seçimi"),
    ("piksel-oda.svg", "Piksel çalışma odası"),
    ("commit-metro.svg", "Commit Metro"),
    ("karakter-kagidi.svg", "RPG karakter kâğıdı"),
    ("cizgi-roman.svg", "Dikey çizgi roman"),
]


def sec(gun: datetime.date):
    return SAHNELER[gun.toordinal() % len(SAHNELER)]


def main():
    gun = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
    dosya, ad = sec(gun)
    shutil.copyfile(KOK / "sahneler" / dosya, KOK / "sahneler" / "gunun-sahnesi.svg")
    readme = KOK / "README.md"
    metin = readme.read_text(encoding="utf-8")
    yeni = re.sub(r"<!--sahne-->.*?<!--/sahne-->", f"<!--sahne-->{ad}<!--/sahne-->", metin, flags=re.S)
    if yeni == metin and "<!--sahne-->" not in metin:
        sys.exit("README'de <!--sahne--> işareti yok")
    readme.write_text(yeni, encoding="utf-8", newline="\n")
    print(gun, "->", ad)


if __name__ == "__main__":
    main()
