# Come sono fatte le immagini del profilo

Tre SVG animati scritti a mano (niente servizi esterni): GitHub li mostra come immagini e le animazioni CSS dentro l'SVG funzionano.

- `header.py` → `header.svg`: le creste del Monte Disgrazia (DEM Copernicus GLO-30, griglia del portfolio in `src/data/ridges/disgrazia.json`) che si disegnano, il sole che tramonta, il saluto.
- `portrait.py` → `portrait.svg`: ritratto ASCII dalla foto in vetta; la persona è scontornata con [rembg](https://github.com/danielgatis/rembg) (maschera salvata in `mask-full.png`), lo sfondo diventa un cielo a puntini.
- `card.py` → `card.svg`: la scheda `whoami` in stile terminale; i testi sono in cima al file.

Si rigenerano da questa cartella con `python3 header.py`, `python3 card.py`, `python3 portrait.py` (Pillow e NumPy; i percorsi puntano al portfolio sul Desktop). COLS=74 ROWS=56 per il ritratto.
Ispirato a [Build an animated GitHub profile README](https://www.avivashishta.com/blog/build-animated-github-profile-readme).
