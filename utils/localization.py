
def t(key: str, lang: str = "ko") -> str:
    dicts = {
        "app_title": {"ko": "냉장고 파먹기", "en": "Fridge Meal Planner"},
        "app_subtitle": {"ko": "있는 재료로 3끼 식단을 자동 추천합니다", "en": "Get 3 meal ideas from what you already have"},
        "your_ingredients": {"ko": "내 재료", "en": "Your ingredients"},
        "ingredient_text_placeholder": {
            "ko": "예: 두부(내일 만료), 양파 1개, 시금치 100g",
            "en": "e.g., tofu (expires tomorrow), onion, 100g spinach"
        },
        "exclude_allergens": {"ko": "알레르기 제외", "en": "Exclude allergens"},
        "music_prefs": {"ko": "식사 음악 추천", "en": "Dining music"},
        "mood": {"ko": "무드", "en": "Mood"},
        "three_meals": {"ko": "3끼 식단 추천", "en": "Plan 3 meals"},
        "suggest_recipes_btn": {"ko": "레시피 추천", "en": "Suggest recipes"},
        "download_recipe_card": {"ko": "요리카드(.md) 다운로드", "en": "Download recipe card (.md)"},
        "toggle_favorite": {"ko": "즐겨찾기 추가/해제", "en": "Toggle favorite"},
        "favorites_tab": {"ko": "즐겨찾기", "en": "Favorites"},
        "export_favorites": {"ko": "즐겨찾기 내보내기(JSON)", "en": "Export favorites (JSON)"},
        "import_favorites": {"ko": "즐겨찾기 불러오기(JSON)", "en": "Import favorites (JSON)"},
        "import_success": {"ko": "가져왔습니다!", "en": "Imported!"},
        "import_fail": {"ko": "불러오기에 실패했습니다", "en": "Failed to import"},
        "shopping_list": {"ko": "장보기 리스트", "en": "Shopping list"},
        "missing_ingredients": {"ko": "부족한 재료", "en": "Missing ingredients"},
        "efficacy_label": {"ko": "효능/특징", "en": "Benefits"},
        "nutrition_label": {"ko": "영양(대략)", "en": "Nutrition (approx.)"},
        "allergen_legend": {"ko": "알레르기 기준", "en": "Allergen legend"},
        "music_reco": {"ko": "음악 추천", "en": "Music recommendations"},
        "share_hint": {"ko": "사이드바 링크 파라미터(공유용)", "en": "Sidebar link params (shareable)"},
        "download_shopping": {"ko": "장보기 JSON 다운로드", "en": "Download shopping JSON"}
    }
    return dicts.get(key, {}).get(lang, key)
