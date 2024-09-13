# Photo-Management-Web
Cucu Viorel-Cosmin 314CA
# IAP Assignment: Aplicatie Web de Gestionare a Pozelor

## Introducere

In primele zile ale web-ului, site-urile personale si comunitatile online au inceput sa apara, iar oamenii au inceput sa creeze pagini HTML pentru a-si afisa colectiile de poze manual. Odata cu cresterea popularitatii platformelor de socializare precum MySpace si Flickr, partajarea pozelor online a devenit mai accesibila. Pentru aceasta tema, am implementat o aplicatie web pentru gestionarea pozelor personale (o mini galerie foto) folosind tehnologii Python si Flask.

## Prezentare Generala a Proiectului

Acest proiect implica construirea unei aplicatii web cu urmatoarele caracteristici:

- **Template Personalizat HTML + CSS:** Un design personalizat pentru aplicatie.
- **Functionalitate de Autentificare:** Autentificare pentru administratori pentru a avea permisiunea de a incarca fisiere.
- **Pagina Principala Neautentificata:** Afisarea pozelor incarcate in miniaturi de rezolutie mica, organizate pe categorii.
- **Pagina Autentificata:** Formular de incarcare a pozelor pentru administratori, inclusiv optiuni pentru redenumirea si categorisirea pozelor.
- **Pagina Despre Mine:** O pagina cu continut personal sau fictiv.
- **Stocare Poze:** Stocare persistenta a pozelor incarcate pe filesystem-ul serverului, organizate in directoare pe categorii, cu crearea optionala a miniaturilor.
- **Containerizare Docker:** O imagine Docker pentru a asigura implementarea si portabilitatea consistenta.

## Frontend Web: Interfata Utilizator / Design

Designul web include:

- O pagina principala care afiseaza galeria publica de poze cu miniaturi.
- Un formular de autentificare pentru administratori.
- Un formular de incarcare a fisierelor accesibil doar utilizatorilor autentificati, cu campuri pentru redenumirea pozelor si selectarea categoriilor.
- O pagina "Despre Mine" cu continut personalizabil.
- Utilizarea unui template Jinja2 de baza pentru a evita duplicarea codului.
- O bara de meniuri care leaga toate paginile importante.

## Backend Web: API REST-ful

Aplicatia Flask ofera urmatoarele endpoint-uri:

- `/` (GET): Serveste pagina HTML principala.
- `/login` (POST): Formular de autentificare, cu `username` si `password` ca nume de campuri POST.
- `/upload` (POST): Endpoint pentru incarcare folosind encoding-ul `multipart/form-data` cu campuri `image`, `name` si `category`. Suporta formate PNG si JPEG.

Aplicatia se leaga la toate interfetele folosind `app.run(host="0.0.0.0")` si asculta pe portul 5000.

## Stocare Poze si Miniaturi

Pozele incarcate sunt stocate pe filesystem-ul serverului, organizate in directoare pe categorii. Fiecare poza este insotita de o miniatura de rezolutie mica, creata folosind biblioteca Pillow, si salvata cu sufixul `.thumb.<extension>`.

## Containerizare

Un Dockerfile este inclus pentru a containeriza aplicatia Flask. Aplicatia poate fi construita si rulata folosind:

```bash
docker build -t iap1-tema .
docker run -p 5000:5000 -it iap1-tema
