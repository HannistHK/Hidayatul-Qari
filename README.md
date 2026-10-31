# Hidayat-ul-Qari Sharah Sahih al-Bukhari

> **ہدایۃ القاری شرح صحیح البخاری** — Complete collection of **7,563 Hadiths** of Sahih al-Bukhari with Arabic Matn, Urdu Translation, and Commentary (Sharh) by **Shaykh Abdul Sattar Hammad**, packaged into an ultra-fast, zero-dependency static web application ready for GitHub Pages.

[![Deploy to GitHub Pages](https://github.com/shahzebfaisal/Hidayatul-Qari/actions/workflows/deploy.yml/badge.svg)](https://github.com/shahzebfaisal/Hidayatul-Qari/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hadiths](https://img.shields.io/badge/Hadiths-7%2C563-emerald.svg)](#)
[![Books](https://img.shields.io/badge/Books-98%20Kutub-indigo.svg)](#)
[![Theme](https://img.shields.io/badge/UI-Dark%20%7C%20Light-purple.svg)](#)

---

## Live Demo & GitHub Pages Hosting

Deploy directly to **GitHub Pages** with zero backend infrastructure required:

1. Push this repository to GitHub.
2. Go to **Settings** > **Pages**.
3. Under **Build and deployment**:
   - **Source**: `Deploy from a branch` (or use GitHub Actions).
   - **Branch**: `main`, Folder: `/ (root)`.
4. Click **Save**. Your site will be live at:
   `https://<your-username>.github.io/Hidayatul-Qari/`

Alternatively, the included automated GitHub Action workflow (`.github/workflows/deploy.yml`) handles builds and deployments automatically on every push to `main`.

---

## Features

- **100% Static & Serverless**: Runs entirely in the client's browser with zero backend or API server needed.
- **Instant Search (<3ms)**:
  - Search by Hadith number (e.g. `1`, `42`, `#5448`).
  - Search by keywords in Arabic (with automatic diacritics / tashkeel normalization).
  - Search by Urdu translation and commentary.
  - Search scope selector (`All Fields`, `Arabic Matn`, `Urdu Translation`, `Urdu Commentary`).
- **Dual-Phase Progressive Loading**:
  - **Phase 1 (Instant Paint <100ms)**: Loads table of contents and initial hadiths batch for instantaneous rendering.
  - **Phase 2 (Background Preload)**: Silently preloads the complete 7,563 hadiths dataset in the background.
- **Authentic Islamic Calligraphy & Typography**:
  - **Arabic Matn**: King Fahd Complex **KFGQPC Uthman Taha Naskh** (`fonts/arabic.ttf`).
  - **Urdu Translation & Commentary**: Authentic **Jameel Noori Nastaleeq** (`fonts/urdu.ttf`) with generous word spacing (`0.24em`).
- **Distraction-Free Reader Mode Modal**:
  - Deep reading view with keyboard shortcuts (`Left Arrow` for previous hadith, `Right Arrow` for next hadith, `Esc` to close).
- **Interactive Table of Contents (98 Books)**:
  - Modal drawer listing all 98 books of Sahih al-Bukhari with live title search and hadith count tags.
- **KitaboSunnat-Inspired UI**:
  - Segmented Dark / Light theme switch with `localStorage` memory and zero flash of unstyled content.
  - Reading font size adjusters (`A-` / `A+`).
  - One-click structured text copying and shareable direct URLs (`?hadith=1`).

---

## Directory Structure

```text
Hidayatul-Qari/
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions automated Pages deployment
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
├── index.html                # Main static web application (GitHub Pages entry)
├── 404.html                  # Fallback redirect for single-page routing
├── build_data.py             # Script to regenerate static data files
├── fonts/
│   ├── arabic.ttf            # KFGQPC Uthman Taha Naskh font
│   └── urdu.ttf              # Jameel Noori Nastaleeq font
└── data/
    ├── chapters.json         # 98 Chapters metadata and hadith ranges
    ├── initial_hadiths.json  # First 30 hadiths for instant first paint (<320 KB)
    ├── bukhari_all.json      # Complete 7,563 hadiths dataset (~6.3 MB gzipped)
    └── stats.json            # Collection statistics
```

---

## Local Development

To run the static website locally on your computer:

```bash
# Clone the repository
git clone https://github.com/<your-username>/Hidayatul-Qari.git
cd Hidayatul-Qari

# Start any local HTTP server:
python -m http.server 8000
```

Open your browser and navigate to:
**`http://localhost:8000`**

---

## Regenerating Data

If you modify the source hadith datasets or SQLite database in the parent project, run:

```bash
python build_data.py
```

This will automatically re-extract, normalize, and minify `data/chapters.json`, `data/initial_hadiths.json`, and `data/bukhari_all.json`.

---

## Credits & Acknowledgements

- **Commentary (Sharh)**: *Hidayat-ul-Qari* by **Shaykh Abdul Sattar Hammad** حفظہ اللہ.
- **Hadith Text & Dataset**: Sahih al-Bukhari (7,563 Hadiths).
- **Developer**: **[Shahzeb Faisal](https://shahzebfaisal.com)**.

---

## License

This project is licensed under the [MIT License](LICENSE).
Hadith text and commentary remain public Islamic scholarship for education and research.
