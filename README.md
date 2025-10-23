
# Fridge Meal Planner (냉장고 파먹기)

Streamlit app to suggest **3 meals** using the ingredients you already have.
Features:
- Ingredient free-text + multi-synonym support
- Allergen filters (gluten/dairy/nuts/shellfish/eggs/soy)
- 3-meal auto planner with priority for **expiring** items like “두부(내일 만료)”
- Recipe card **.md download**
- Favorites ⭐ (export/import JSON)
- Shareable links via query params (lang/theme/allergens/ingredients)
- Dual UI (한국어/English)
- Nutrition estimates per recipe (kcal/P/F/C)
- Basic shopping list for missing items
- Dining music recommendations with fixed Spotify/YouTube playlists + search links
- Theme toggle: light/dark/classic
- GitHub Actions CI (deps + lint)

> Demo data only. Replace `data/recipes.json` and `data/nutrition_db.json` with your own.

## Local dev

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to https://share.streamlit.io, pick the repo, set **Main file path** to `app.py`.
3. (Optional) Set **Python version** 3.11 in advanced settings; it will use `requirements.txt`.
4. Deploy.

## Data model

- `data/recipes.json`: list of recipes with fields: `slug, title, cuisine, tags, benefits, ingredients[{name, amount}], steps[]`
- `data/nutrition_db.json`: per-ingredient **approx** nutrition per recipe-use (demo-scale; replace with real per-100g and add gram parsing if desired).
- `data/ingredients_synonyms.json`: maps Korean ingredient names to English canonical names used in recipes.

## Favorites export/import

- Export: downloads `favorites.json`
- Import: upload `favorites.json` created by the app.

## Shareable links

The app reads and sets URL query parameters:
- `lang` (`ko` or `en`)
- `theme` (`light`, `dark`, `classic`)
- `allergens`: comma-separated list
- `ingredients`: free text

Example: `?lang=ko&theme=dark&allergens=gluten,soy&ingredients=두부(내일%20만료),양파`

## Notes

- **Nutrition** is a rough estimate for demo. For precise numbers, extend `utils/nutrition.py` to parse weights and sum per-100g values.
- The 3-meal selector prioritizes recipes that use your ingredients and **expiring** items, while honoring allergen filters.
- Add more playlists in `utils/music.py` for better coverage.
