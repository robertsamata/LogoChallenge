# Logo Extraction and Clustering Pipeline

Acest proiect este destinat să extragă logo-uri de pe site-uri web și să le grupeze în funcție de similitudinea lor.

## Descrierea proiectului

Pipeline-ul include următoarele etape:
1. **Extrage URL-ul logo-ului** de pe un site web (domeniu).
2. **Descarcă imaginea logo-ului** de la URL-ul extras.
3. **Calculează un hash perceptual** al imaginii logo-ului pentru a o reprezenta într-o formă ușor comparabilă.
4. **Construiește un grafic de similitudine** între logo-uri, unde nodurile sunt site-urile web și muchiile reprezintă similitudinea dintre logo-urile lor.
5. **Gruparea logo-urilor similare** într-un cluster bazat pe distanța dintre hash-urile perceptuale.

## Fișierele proiectului

1. **`logo_extraction_clustering.py`**
   - Acesta este fișierul principal al proiectului care implementează întregul pipeline.
   - Include următoarele funcții:
     - `extract_logo_url(domain)` - Extrage URL-ul logo-ului pentru un site dat.
     - `download_logo(domain, url)` - Descarcă și salvează logo-ul într-un fișier local.
     - `compute_hash(image_path)` - Calculează hash-ul perceptual pentru o imagine.
     - `build_clusters(hashes, threshold=5)` - Creează grupuri de logo-uri similare pe baza hash-urilor perceptuale.
   - Se rulează printr-o listă de domenii, extrăgând, descărcând și procesând logo-urile.

2. **`logos.csv`**
   - Fișier CSV care conține lista de domenii de pe care se vor extrage logo-urile.
   - 
3. **`extracted_logos.csv`**
   - Fișier CSV generat de program, care conține informații despre fiecare logo extras:
     - `domain`: Domeniul site-ului.
     - `logo_url`: URL-ul logo-ului.
     - `logo_path`: Calea locală a fișierului logo descărcat.
     - `phash`: Hash-ul perceptual al logo-ului.
   - Acest fișier este folosit pentru a salva rezultatele intermediare.

4. **`logo_clusters.txt`**
   - Fișier text care conține grupurile de site-uri web cu logo-uri similare, fiecare cluster fiind definit de o listă de domenii.
   - Fiecare cluster este identificat printr-un număr și conține o listă de domenii care au logo-uri suficient de asemănătoare pentru a fi grupate împreună.

5. **`logos/`**
   - Directorul în care sunt salvate toate logo-urile descărcate. Fiecare logo este salvat ca fișier PNG, denumit după domeniul site-ului (ex: `example.com.png`).
   - 
