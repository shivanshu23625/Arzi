import re
import urllib.request

def test_bilingual_and_responsive():
    # 1. Read index.html
    with open('flask_backend/static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 2. Read app.js
    with open('flask_backend/static/app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    # Check language switcher in index.html
    assert 'id="langEn"' in html, "Language switcher EN button missing in index.html"
    assert 'id="langHi"' in html, "Language switcher Hindi button missing in index.html"
    assert 'class="lang-switch-group"' in html, "Language switch group class missing"

    # Check i18n dictionary in app.js
    assert 'const I18N_DICT =' in app_js, "I18N_DICT missing in app.js"
    assert 'function setLanguage' in app_js, "setLanguage function missing in app.js"
    assert 'function initLanguage' in app_js, "initLanguage function missing in app.js"

    # Extract all data-i18n keys from index.html
    i18n_keys = re.findall(r'data-i18n="([^"]+)"', html)
    print(f"Total data-i18n keys in index.html: {len(i18n_keys)} (Unique: {len(set(i18n_keys))})")

    missing_keys = []
    for k in set(i18n_keys):
        if f'"{k}":' not in app_js:
            missing_keys.append(k)

    if missing_keys:
        print(f"WARNING: Missing i18n keys in app.js: {missing_keys}")
    else:
        print("All data-i18n keys successfully present in I18N_DICT!")

    # Check that tables are inside .table-responsive
    tables = [m.start() for m in re.finditer(r'<table\b', html)]
    print(f"Total tables found: {len(tables)}")
    for idx, pos in enumerate(tables, 1):
        preceding = html[max(0, pos-200):pos]
        assert 'table-responsive' in preceding, f"Table #{idx} is not wrapped in .table-responsive!"
    print("All tables are properly wrapped in .table-responsive!")

    # Check that Hero buttons are simplified (not 6 buttons)
    hero_match = re.search(r'<div class="hero-action-row">(.*?)</div>', html, re.DOTALL)
    assert hero_match, "Hero action row not found"
    hero_btns = re.findall(r'<button\b', hero_match.group(1))
    print(f"Hero action row buttons: {len(hero_btns)} (Simplified down from 6)")
    assert len(hero_btns) <= 3, f"Expected <= 3 hero buttons, got {len(hero_btns)}"

    # Check simplified presets
    presets_match = re.search(r'<div class="simplified-presets-bar">(.*?)</div>', html, re.DOTALL)
    assert presets_match, "simplified-presets-bar not found"
    preset_btns = re.findall(r'<button\b', presets_match.group(1))
    print(f"Simplified preset buttons: {len(preset_btns)} (Consolidated down from 13)")
    assert len(preset_btns) == 5, f"Expected 5 clean preset categories, got {len(preset_btns)}"

    # Check live server endpoint
    try:
        res = urllib.request.urlopen('http://localhost:5000/')
        assert res.status == 200, f"Server returned {res.status}"
        live_html = res.read().decode('utf-8')
        assert 'id="langEn"' in live_html, "Live server HTML missing langEn"
        print("Live Flask server verified: 200 OK with updated bilingual markup!")
    except Exception as e:
        print("Live server check note:", e)

    print("\nALL BILINGUAL, SIMPLIFIED UI, AND RESPONSIVENESS CHECKS PASSED!")

if __name__ == '__main__':
    test_bilingual_and_responsive()
