# Felhőalapú elosztott rendszerek laboratórium  
## Fényképalbum alkalmazás – 1. beadás

## Projekt célja

A feladat célja egy publikus PaaS környezetben futó, skálázható és többrétegű fényképalbum alkalmazás létrehozása.  

Az alkalmazás lehetővé teszi:

- Fényképek feltöltését és törlését
- Fényképek listázását név és dátum szerint rendezve
- Kép megjelenítését részletes nézetben
- Felhasználókezelést (regisztráció, bejelentkezés, kijelentkezés)
- Jogosultság alapú műveleteket (feltöltés/törlés csak bejelentkezett felhasználónak)

Az alkalmazás GitHubon érhető el, és publikus PaaS környezetben fut.

---

# Felhasznált technológiák

## Backend

- Python 3.12  
- Django 6  
- Gunicorn (WSGI alkalmazásszerver)  
- SQLite (1. beadás – konténeren belüli adatbázis)

A Django keretrendszer választásának indokai:

- Beépített autentikációs rendszer  
- ORM támogatás  
- Gyors fejlesztés  

---

## Frontend / UI

A felhasználói felület:

- Django template rendszerrel készült  
- HTML és alap CSS  
- Django beépített form kezelése  
- Egyszerű, letisztult, reszponzív elrendezés  

A főbb nézetek:

- Navigációs sáv (login / logout / regisztráció)
- Lista nézet rendezési lehetőséggel
- Részletes képnézet
- Feltöltési űrlap fájlfeltöltéssel


---

# PaaS környezet

Az alkalmazás az alábbi környezetben fut:

- OKD (OpenShift Kubernetes Distribution)

A rendszer:

- Konténerizált futtatás
- BuildConfig alapú build
- Deployment objektum
- Route alapú publikus elérés

---

# Konténerizálás

Dockerfile alapú build készült.

Főbb elemek:

- `python:3.12-slim` alap image
- `requirements.txt` telepítése
- Gunicorn indítás
- `entrypoint.sh` migrációk futtatására

Az entrypoint feladata:

1. Adatbázis migráció futtatása
2. Gunicorn indítása

---

# Adatbázis

## 1. beadás

- SQLite adatbázis
- `/tmp/db.sqlite3` helyen fut (OpenShift kompatibilis)

Ez a megoldás működőképes, de:

- Nem perzisztens pod újraindítás esetén
- Nem ideális horizontális skálázáshoz

A 2. beadásban külön adatbázis-szerver (pl. PostgreSQL) kerül bevezetésre.

---

# Fájlkezelés

A feltöltött képek:

- `MEDIA_ROOT` alatt kerülnek mentésre
- Írható könyvtárba konfigurálva OpenShift alatt

Jelenleg nem használ Persistent Volume-t, ezért:

- Pod újraindítás esetén a fájlok elveszhetnek

Ez a 2. beadás során kerül fejlesztésre.

---

# Biztonság

- Django beépített autentikáció
- CSRF védelem
- `CSRF_TRUSTED_ORIGINS` konfigurálva
- `ALLOWED_HOSTS` beállítva
- Jogosultság alapú feltöltés és törlés

---

# Build és deploy folyamat

Jelenlegi állapot:

- A repository publikus GitHubon
- OpenShift BuildConfig használatban
- Az alkalmazás manuális build után deployolható

Még nem teljesen megoldott (nem működik a webhook OKD-nál. 403-as hibát dob):

- GitHub webhook → automatikus build indítás push esetén

Ez a következő fejlesztési lépés része.

---

# Többrétegű architektúra

Az alkalmazás jelenlegi rétegei:

1. Web réteg – Django + Gunicorn  
2. Alkalmazás logika – Django ORM  
3. Adatbázis réteg – SQLite  

A 2. beadás célja:

- Külön adatbázis-szerver
- Perzisztens storage
- Teljes skálázható architektúra

---

# Skálázhatóság

OpenShift Deployment használatával:

- Több pod példány indítható
- Kubernetes load balancing biztosított
- Route biztosítja a külső elérést

SQLite használata miatt jelenleg a horizontális skálázás korlátozott, ezért a 2. beadás során külön adatbázis kerül bevezetésre.

---

# Funkcionális követelmények teljesülése

- Fénykép feltöltés  
- Fénykép törlés  
- Név (max. 40 karakter)  
- Feltöltési dátum mentése  
- Rendezés név szerint  
- Rendezés dátum szerint  
- Kép megjelenítése részletes nézetben  
- Felhasználó regisztráció  
- Bejelentkezés  
- Kijelentkezés  
- Jogosultság alapú műveletek  

---

# Következő fejlesztési lépések (2. beadás)

- Külső adatbázis-szerver
- Perzisztens fájltárolás (PVC)
- GitHub webhook automatikus build

---

# Összegzés

Az első beadás keretében elkészült:

- Egy működő, publikus PaaS környezetben futó fényképalbum alkalmazás
- Teljes felhasználókezelés
- Képfeltöltés és listázás
- Konténerizált deploy OpenShift környezetben

A második beadás során az architektúra továbbfejlesztése történik külön adatbázis-szerver és perzisztens tárolás bevezetésével.