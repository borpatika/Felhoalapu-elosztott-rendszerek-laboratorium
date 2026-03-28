# Felhőalapú elosztott rendszerek laboratórium  
# Fényképalbum alkalmazás – 1. beadás

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


# Fényképalbum alkalmazás – 2. beadás

### TODO: azt hittem megírtam, de nem.

tldr: létrehoztam egy postgres deploymentet és service-t és külön adatbázis szerver fut a Django alkalmazása mellett és ehhez kapcsolódik az appom. Továbbá létrehoztam kettő PVC-t és hozzácsatoltam egyet-egyet a Django és postgres pod-hoz, így az esetleges újraindítások után se vesznek el az adatok, hanem perzisztensen megmaradnak.

<br>

# Fényképalbum alkalmazás – 3. beadás
## Skálázódó Webalkalmazás Dokumentáció

A feladat célja a fényképalbum alkalmazásszerverének automatikus skálázódásának bemutatása egy PaaS környezetben (OKD/OpenShift), valamint a skálázódás tesztelése terheléspróbával. Ehhez a Django alapú alkalmazást és a Locust terhelésgenerátort használtam.

---

## 2. Alkalmazás beállítása és skálázódás konfigurálása

1. **Django Deployment módosítása**
   - A konténer erőforrásait korlátoztam CPU és memória szempontjából, hogy a HPA kis terhelés esetén is indokolja a több pod elindítását.

2. **HPA (Horizontal Pod Autoscaler) létrehozása**
   - A Deployment-hez HPA-t konfiguráltam a minimum és maximum pod szám megadásával, valamint CPU-arány figyelésével.
   - A HPA-t az OKD webes felületén hoztam létre.
   - A beállított HPA biztosítja, hogy a CPU terhelés növekedése új podokat indít, és a terhelés csökkenésekor visszaskálázódik.

---

## 3. Terheléspróba elkészítése Locust-tal

1. **Locust testfile létrehozása**
   - A teszt lefedi a fényképalbum fő funkcióit: lista, részletezés, feltöltés.
   - Teszt felhasználót hoztam létre a Django appban `testuser`/`testpassword` névvel.
   - A szükséges tesztképet (`test.jpg`) is feltöltöttem a teszt konténerhez.

2. **Dockerfile a Locust számára**  
   - Létrehoztam egy Dockerfile-t, amely tartalmazza a Locust telepítését és a testfile-t.
   - Az image build és deployment OpenShift CLI segítségével történt:
     - `oc new-build` az új image létrehozására
     - `oc start-build` az image felépítésére
     - `oc apply -f <deployment>` a Locust Deployment létrehozására
     - `oc expose svc/locust` a webes felület eléréséhez

3. **Route létrehozása**  
   - Első próbálkozásnál a HTTPS miatt a Locust webes UI nem volt elérhető.
   - Hozzáadtam egy Route-ot a Locust szolgáltatáshoz, így a webes felület elérhetővé vált.

---

## 4. Locust Webes UI

- A webes felületen beállítható a felhasználók száma, a ramp-up idő és a futtatási idő.
- A teszt során például:
  - 10 felhasználó a csúcsban
  - Ramp-up: 1 user/sec
  - Host: a Django alkalmazás elérési címe
- Webes UI képernyőképe: ![alt text](image.png)

---

## 5. Automatikus skálázódás dokumentálása

- A HPA monitorozása OpenShift CLI-vel (`oc get hpa`).
- Terhelés alatt az alkalmazás több podra skálázódott (pl. 1 -> 4 pod).
- Terhelés csökkenésével a podok visszaskálázódtak az eredeti számra (1 pod).
### Skálázódás:
- Terhelés előtt 1 pod fut: ![alt text](image-1.png)
- Terhelés elindítása: ![alt text](image-2.png)
- Terhelés közben 4 pod fut: ![alt text](image-3.png)
- Terhelés leállta után visszaáll 1 pod-ra: ![alt text](image-4.png)
---

## 7. Tanulságok

- **Autoscaling működik**: a HPA sikeresen skálázta a podokat a terhelés növekedésére és csökkenésére.
- **Erőforrás-korlátok**: CPU/memória limit beállítás szükséges a kis terhelésű felskálázódáshoz.
- **Terheléspróba PaaS-on**: a Locust webes UI lehetővé tette a teszt konfigurálását felhőből.

---