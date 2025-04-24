# Logo Extraction and Clustering Pipeline

import os
import requests
from bs4 import BeautifulSoup # os, requests, bs4 pentru manipularea fisierelor,extragerea continutului html si procesarea site-urilor web
from urllib.parse import urljoin
from PIL import Image # procesarea  si manipularea imaginilor
import imagehash # pentru a calcula hash-urile perceptuale ale imaginilor
import networkx as nx # pentru construirea graficului de similitudini intre imagini si gruparea lor
from io import BytesIO
import pandas as pd #manipularea datelor
from tqdm import tqdm #bara de progres pentru lista domeniilor

# Citirea domeniilor de pe care se vor extrage logo-urile
df = pd.read_csv("logos.csv")
domains = df['domain'].dropna().unique().tolist()

# Crearea unui director pentru stocarea logo-urilor
os.makedirs("logos", exist_ok=True)

# Extragerea logo URL
# aceasta functie preia url-ul unui site si cauta logo-ul in codul sursa al paginii
# cautarile se  fac in tag-urile link si meta
# daca nu se gaseste logo-ul se presupune ca este la adresa default /favicon
def extract_logo_url(domain):
    base_url = f"https://{domain}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; LogoBot/1.0)"}
    try:
        r = requests.get(base_url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
        if icon_link:
            return urljoin(base_url, icon_link.get("href"))

        og_img = soup.find("meta", property="og:image")
        if og_img:
            return urljoin(base_url, og_img.get("content"))

        return urljoin(base_url, "/favicon.ico")
    except:
        return None

# Download logo
# aceasta functie descarca imaginea logo-ului de la url-ul obtinut anterior si o salveaza intr-un fisier
def download_logo(domain, url):
    try:
        r = requests.get(url, timeout=10)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        path = f"logos/{domain}.png"
        img.save(path)
        return path
    except:
        return None

# Calculam hash-ul perceptual(bazat pe caractersiticile vizuale ale imaginii)
# acest hash il folosim pentru a compara similaritati intre imagini
def compute_hash(image_path):
    try:
        img = Image.open(image_path)
        return str(imagehash.phash(img))
    except:
        return None

# Functia build clusters
# foloseste un grafic pentru a grupa site-urile in functie de similitudinea logo-urilor
# daca diferenta dintre hash-urile a 2 logo-uri este mai mica sau egala decat 5 atunci le considera similare si sunt grupate impreuna
def build_clusters(hashes, threshold=5):
    G = nx.Graph()
    items = list(hashes.items())
    for i in range(len(items)):
        domain1, hash1 = items[i]
        for j in range(i+1, len(items)):
            domain2, hash2 = items[j]
            if hash1 and hash2:
                dist = imagehash.hex_to_hash(hash1) - imagehash.hex_to_hash(hash2)
                if dist <= threshold:
                    G.add_edge(domain1, domain2)
    return list(nx.connected_components(G))

# Executare pipeline
results = []
for domain in tqdm(domains):
    logo_url = extract_logo_url(domain)
    if not logo_url:
        continue
    logo_path = download_logo(domain, logo_url)
    if not logo_path:
        continue
    phash = compute_hash(logo_path)
    if not phash:
        continue
    results.append((domain, logo_url, logo_path, phash))

# Save interim results
logos_df = pd.DataFrame(results, columns=["domain", "logo_url", "logo_path", "phash"])
logos_df.to_csv("extracted_logos.csv", index=False)

# Cluster similar logos
hash_dict = dict(zip(logos_df['domain'], logos_df['phash']))
clusters = build_clusters(hash_dict)

# Save clusters
with open("logo_clusters.txt", "w") as f:
    for i, cluster in enumerate(clusters):
        f.write(f"Cluster {i+1} ({len(cluster)} logos):\n")
        for domain in cluster:
            f.write(f"  - {domain}\n")
        f.write("\n")
