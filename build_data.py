#!/usr/bin/env python3
"""
build_data.py
Generates:
1. data/chapters.json (Table of Contents for 98 Books)
2. data/search_index.json (Pre-normalized lightweight instant search & filter index)
3. data/hadiths/{id}.json (Individual standalone JSON file for every hadith with Matn, Tarjumah, and Sharh)
4. data/stats.json (Metadata)
"""

import os
import sys
import json
import sqlite3
import re
import time

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(CURRENT_DIR, 'data')
HADITHS_DIR = os.path.join(DATA_DIR, 'hadiths')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(HADITHS_DIR, exist_ok=True)

CHAPTERS_INPUT = os.path.join(PARENT_DIR, 'chapters.json')
DB_INPUT = os.path.join(PARENT_DIR, 'bukhari.db')

def normalize_text(text):
    if not text:
        return ''
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)  # remove harakat
    text = re.sub(r'[آأإٱ]', 'ا', text)
    text = text.replace('ة', 'ہ').replace('ك', 'ک')
    for y in ['ي', 'ى', 'ئ']:
        text = text.replace(y, 'ی')
    text = re.sub(r'[،۔؛؟\-\.,\/#!$%\^&\*;:{}=\-_`~()«»]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

def build_all():
    start_time = time.time()
    print("Building datasets...")

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

    print(f"1. Chapters generated: {chapters_path}")

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
               type_atraaf, type_rawaat, type_qft
        FROM hadiths
        ORDER BY hadith_number ASC
    ''').fetchall()
    conn.close()

    print(f"Loaded {len(rows)} hadiths from database.")

    search_index = []
    count_files = 0

    for r in rows:
        hid = r['hadith_number']

        # Individual Hadith JSON file
        hadith_obj = {
            'id': hid,
            'hadith_number': hid,
            'chapter_id': r['chapter_id'],
            'chapter_arabic': r['chapter_arabic'],
            'chapter_urdu': r['chapter_urdu'],
            'section_id': r['section_id'],
            'section_arabic': r['section_arabic'],
            'section_urdu': r['section_urdu'],
            'arabic': r['arabic_text'],
            'arabic_search': r['arabic_text_search'],
            'translation': r['urdu_translation'],
            'sharh': r['urdu_sharh'],
            'classification': {
                'atraaf': r['type_atraaf'] or '',
                'rawaat': r['type_rawaat'] or '',
                'qft': r['type_qft'] or ''
            }
        }

        hadith_file = os.path.join(HADITHS_DIR, f"{hid}.json")
        with open(hadith_file, 'w', encoding='utf-8') as hf:
            json.dump(hadith_obj, hf, ensure_ascii=False, separators=(',', ':'))
        count_files += 1

        # Pre-normalized fields for instant 0-CPU-overhead client search
        norm_ar = normalize_text(r['arabic_text_search'])
        norm_ur = normalize_text(r['urdu_translation'])
        norm_sh = normalize_text(r['urdu_sharh'][:90] if r['urdu_sharh'] else '')

        # Search Index Item
        search_index.append({
            'id': hid,
            'c': r['chapter_id'],
            'su': r['section_urdu'] or '',
            'na': norm_ar,
            'nu': norm_ur,
            'ns': norm_sh
        })

    print(f"2. Generated {count_files} individual hadith JSON files in {HADITHS_DIR}")

    # 4. Save Search Index
    index_path = os.path.join(DATA_DIR, 'search_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, separators=(',', ':'))

    index_mb = os.path.getsize(index_path) / (1024 * 1024)
    print(f"3. Generated pre-normalized search index: {index_path} ({index_mb:.2f} MB)")
    print(f"All done in {time.time() - start_time:.2f} seconds!")

if __name__ == '__main__':
    build_all()
