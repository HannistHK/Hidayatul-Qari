#!/usr/bin/env python3
"""
build_data.py
Extracts and generates optimized, minified static JSON datasets for
GitHub Pages deployment of Hidayat-ul-Qari Sharah Sahih al-Bukhari.
"""

import os
import sys
import json
import sqlite3
import time

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(CURRENT_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

CHAPTERS_INPUT = os.path.join(PARENT_DIR, 'chapters.json')
DB_INPUT = os.path.join(PARENT_DIR, 'bukhari.db')

def build_datasets():
    start_time = time.time()
    print("Building datasets for GitHub Pages...")

    # 1. Chapters JSON
    with open(CHAPTERS_INPUT, 'r', encoding='utf-8') as f:
        raw_chapters = json.load(f)

    clean_chapters = []
    for ch in raw_chapters:
        clean_chapters.append({
            'id': ch['chapter_id'],
            'arabic': ch.get('chapter_arabic', ''),
            'urdu': ch.get('chapter_urdu', ''),
            'hadith_start': ch.get('hadith_start', 0),
            'hadith_end': ch.get('hadith_end', 0),
            'hadith_count': ch.get('hadith_count', 0)
        })

    chapters_path = os.path.join(DATA_DIR, 'chapters.json')
    with open(chapters_path, 'w', encoding='utf-8') as f:
        json.dump(clean_chapters, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Generated {chapters_path} ({os.path.getsize(chapters_path) / 1024:.1f} KB)")

    # 2. Stats JSON
    stats_data = {
        'total_hadiths': 7563,
        'total_chapters': 98,
        'book_title_urdu': 'ہدایۃ القاری شرح صحیح البخاری',
        'book_title_arabic': 'صحيح البخاري مع هداية القاري',
        'commentary_author': 'شیخ عبد الستار حماد',
        'commentary_author_en': 'Shaykh Abdul Sattar Hammad'
    }
    stats_path = os.path.join(DATA_DIR, 'stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, ensure_ascii=False, separators=(',', ':'))

    # 3. Read All Hadiths from bukhari.db
    conn = sqlite3.connect(DB_INPUT)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    rows = c.execute('''
        SELECT hadith_number, chapter_id, chapter_arabic, chapter_urdu,
               section_id, section_arabic, section_urdu,
               arabic_text, arabic_text_search,
               urdu_translation, urdu_sharh,
               grading, type_atraaf, type_rawaat, type_qft
        FROM hadiths
        ORDER BY hadith_number ASC
    ''').fetchall()
    conn.close()

    all_hadiths = []
    for r in rows:
        h = {
            'n': r['hadith_number'],
            'c': r['chapter_id'],
            'ca': r['chapter_arabic'],
            'cu': r['chapter_urdu'],
            'sa': r['section_arabic'],
            'su': r['section_urdu'],
            'a': r['arabic_text'],
            'as': r['arabic_text_search'],
            'u': r['urdu_translation'],
            's': r['urdu_sharh'],
            'g': r['grading'] or 'صحيح',
            'ta': r['type_atraaf'] or '',
            'tr': r['type_rawaat'] or '',
            'tq': r['type_qft'] or ''
        }
        all_hadiths.append(h)

    # 4. Initial Batch (First 30 Hadiths) for instant initial page render
    initial_path = os.path.join(DATA_DIR, 'initial_hadiths.json')
    with open(initial_path, 'w', encoding='utf-8') as f:
        json.dump(all_hadiths[:30], f, ensure_ascii=False, separators=(',', ':'))
    print(f"Generated {initial_path} ({os.path.getsize(initial_path) / 1024:.1f} KB)")

    # 5. Full Dataset
    all_path = os.path.join(DATA_DIR, 'bukhari_all.json')
    with open(all_path, 'w', encoding='utf-8') as f:
        json.dump(all_hadiths, f, ensure_ascii=False, separators=(',', ':'))

    size_mb = os.path.getsize(all_path) / (1024 * 1024)
    print(f"Generated {all_path} with {len(all_hadiths)} Hadiths ({size_mb:.2f} MB)")
    print(f"Done in {time.time() - start_time:.2f} seconds!")

if __name__ == '__main__':
    build_datasets()
