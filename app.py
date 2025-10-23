
import streamlit as st
import json
from datetime import datetime, timedelta
from utils.localization import t
from utils.recipes import load_recipes, suggest_recipes, build_shopping_list, allergens_map, expand_ingredients
from utils.nutrition import NutritionDB, estimate_recipe_nutrition, nutrition_table_to_md
from utils.music import recommend_playlists, fixed_playlist_collection
from utils.sharing import get_state_from_query, set_query_from_state
from pathlib import Path

st.set_page_config(page_title="Fridge Meal Planner • 냉장고 파먹기", page_icon="🥗", layout="wide")

# ---- Theming (light/dark/classic) ----
if "theme" not in st.session_state:
    st.session_state.theme = "light"
theme_choice = st.sidebar.radio("Theme", ["light", "dark", "classic"], index=["light", "dark", "classic"].index(st.session_state.theme))
st.session_state.theme = theme_choice
theme_css = """
:root { --card-bg: #ffffff; --text: #111; --muted: #555; }
[class*="stApp"] { background: #f6f8fa; }
.block-container { padding-top: 2rem; }
.stMarkdown a { text-decoration: none; }
"""
dark_css = """
:root { --card-bg: #0f172a; --text: #f1f5f9; --muted: #93a4b6; }
[class*="stApp"] { background: #0b1020; }
.block-container { padding-top: 2rem; }
.stMarkdown a { text-decoration: none; }
"""
classic_css = """
:root { --card-bg: #fffef8; --text: #222; --muted: #444; }
[class*="stApp"] { background: #faf5e6; }
.block-container { padding-top: 2rem; }
"""
css = theme_css if st.session_state.theme == "light" else dark_css if st.session_state.theme == "dark" else classic_css
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ---- Language ----
if "lang" not in st.session_state:
    st.session_state.lang = "ko"
lang_choice = st.sidebar.selectbox("Language / 언어", ["ko", "en"], index=["ko","en"].index(st.session_state.lang))
st.session_state.lang = lang_choice

# ---- Load data ----
recipes = load_recipes(Path("data/recipes.json"))
nutrition_db = NutritionDB(Path("data/nutrition_db.json"))
synonyms = json.loads(Path("data/ingredients_synonyms.json").read_text(encoding="utf-8"))
fixed_playlists = fixed_playlist_collection()

# ---- Query params (shareable link) ----
get_state_from_query(st.session_state)

st.title("🥗 " + t("app_title", st.session_state.lang))
st.caption(t("app_subtitle", st.session_state.lang))

# ---- Inputs ----
st.subheader(t("your_ingredients", st.session_state.lang))
ing_text = st.text_area(t("ingredient_text_placeholder", st.session_state.lang),
                        key="ingredient_text",
                        placeholder="예: 두부(내일 만료), 양파 1개, 시금치 100g\nex) tofu (expires tomorrow), onion, 100g spinach")
allergen_options = ["gluten","dairy","nuts","shellfish","eggs","soy"]
excluded_allergens = st.multiselect(t("exclude_allergens", st.session_state.lang),
                                    options=allergen_options, default=st.session_state.get("excluded_allergens", []))
st.session_state.excluded_allergens = excluded_allergens

# mood + time for music
st.sidebar.subheader(t("music_prefs", st.session_state.lang))
user_mood = st.sidebar.selectbox(t("mood", st.session_state.lang),
                                 ["relaxed","focus","party","comfort","energizing"], index=0)
# Favorite handling
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ---- Expand & parse ingredients ----
expanded_ings, expiring_ings = expand_ingredients(ing_text, synonyms)

# ---- 3-meal planner ----
st.subheader(t("three_meals", st.session_state.lang))
if st.button(t("suggest_recipes_btn", st.session_state.lang)):
    planned = suggest_recipes(recipes, expanded_ings, expiring_ings, excluded_allergens)
    st.session_state.planned = planned
    set_query_from_state(st.session_state)  # update share link

planned = st.session_state.get("planned", [])
cols = st.columns(3) if planned else [st.container()]
total_missing = []
for i, rec in enumerate(planned):
    with cols[i % len(cols)]:
        st.markdown(f"### {rec['title']} ({rec.get('cuisine','')})")
        st.markdown(", ".join(rec["tags"]))
        st.write(t("efficacy_label", st.session_state.lang) + ": " + ", ".join(rec.get("benefits", [])))
        # nutrition estimate
        nutr = estimate_recipe_nutrition(rec, nutrition_db)
        st.write(t("nutrition_label", st.session_state.lang) + f": {nutr['kcal']} kcal · P{nutr['protein']}g · F{nutr['fat']}g · C{nutr['carbs']}g")
        # missing
        missing = [ing for ing in rec["ingredients"] if ing["name"] not in expanded_ings]
        total_missing.extend(missing)
        if missing:
            st.warning(t("missing_ingredients", st.session_state.lang) + ": " + ", ".join({m['name'] for m in missing}))
        # recipe card MD + download
        md = f"# {rec['title']}\n\n" \
             f"**Tags:** {', '.join(rec['tags'])}\n\n" \
             f"**Ingredients:**\n" + "".join([f"- {i['name']} ({i.get('amount','')})\n" for i in rec['ingredients']]) + "\n" \
             f"**Steps:**\n" + "".join([f"{idx+1}. {s}\n" for idx, s in enumerate(rec['steps'])]) + "\n" \
             + nutrition_table_to_md(nutr)
        st.download_button(t("download_recipe_card", st.session_state.lang), data=md, file_name=f"{rec['slug']}.md")
        # favorites
        fav_key = rec["slug"]
        is_fav = fav_key in st.session_state.favorites
        if st.button(("⭐ " if not is_fav else "✖ ") + t("toggle_favorite", st.session_state.lang), key=f"fav_{fav_key}"):
            if is_fav:
                st.session_state.favorites.remove(fav_key)
            else:
                st.session_state.favorites.append(fav_key)

# Shopping list aggregate
if planned:
    st.subheader(t("shopping_list", st.session_state.lang))
    shopping = build_shopping_list(total_missing)
    if shopping:
        st.write(", ".join(sorted({i['name'] for i in shopping})))
        st.download_button(t("download_shopping", st.session_state.lang),
                           data=json.dumps(shopping, ensure_ascii=False, indent=2),
                           file_name="shopping_list.json")

# ---- Favorites tab ----
st.subheader("⭐ " + t("favorites_tab", st.session_state.lang))
fav_recipes = [r for r in recipes if r["slug"] in st.session_state.favorites]
if fav_recipes:
    st.write(", ".join([r["title"] for r in fav_recipes]))
# Import/Export
c1, c2 = st.columns(2)
with c1:
    export_json = json.dumps(st.session_state.favorites, ensure_ascii=False, indent=2)
    st.download_button(t("export_favorites", st.session_state.lang), data=export_json, file_name="favorites.json")
with c2:
    upl = st.file_uploader(t("import_favorites", st.session_state.lang), type=["json"])
    if upl is not None:
        try:
            st.session_state.favorites = json.loads(upl.read())
            st.success(t("import_success", st.session_state.lang))
        except Exception:
            st.error(t("import_fail", st.session_state.lang))

# ---- Music recommendations ----
st.subheader("🎵 " + t("music_reco", st.session_state.lang))
cuisine_mix = list({rec.get("cuisine","global") for rec in planned}) if planned else ["global"]
recs = recommend_playlists(cuisine_mix, user_mood, fixed_playlists)
for r in recs:
    st.markdown(f"- **{r['title']}** → [Spotify]({r['spotify']}) | [YouTube]({r['youtube']})")

# ---- Allergen legend ----
with st.expander(t("allergen_legend", st.session_state.lang)):
    from utils.recipes import allergens_map
    st.json(allergens_map())

st.sidebar.caption(t("share_hint", st.session_state.lang))
st.sidebar.code(st.experimental_get_query_params())

