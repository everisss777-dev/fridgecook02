
import json, re
from pathlib import Path
from collections import Counter

def load_recipes(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def allergens_map():
    return {
        "gluten": ["wheat flour", "soy sauce", "barley", "bread", "noodles", "spaghetti"],
        "dairy": ["milk", "cheese", "butter", "yogurt", "cream"],
        "nuts": ["peanut", "almond", "walnut", "cashew", "pistachio"],
        "shellfish": ["shrimp", "crab", "lobster"],
        "eggs": ["egg", "mayonnaise"],
        "soy": ["tofu", "soybean", "soy sauce", "miso"]
    }

def normalize_name(name: str):
    return name.strip().lower()

def expand_ingredients(text: str, synonyms: dict):
    """
    Parse ingredient text lines. Recognize expiries like '(내일 만료)' or '(expires tomorrow)'.
    Return a set of normalized names and a set of expiring priority names.
    """
    if not text:
        return set(), set()
    names = set()
    expiring = set()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        # extract name (before parenthesis or quantities)
        base = re.split(r"\(|\d|g|kg|ml|개", line, maxsplit=1)[0].strip().lower()
        if not base:
            base = line.strip().lower()
        # map synonyms
        mapped = synonyms.get(base, base)
        names.add(mapped)
        # expiry detection
        if re.search(r"만료|유통기한|임박|tomorrow|expires", line, re.I):
            if "tomorrow" in line.lower() or "내일" in line:
                expiring.add(mapped)
            else:
                expiring.add(mapped)
    return names, expiring

def recipe_allergens(recipe):
    am = allergens_map()
    present = set()
    for ing in recipe["ingredients"]:
        n = normalize_name(ing["name"])
        for k, words in am.items():
            if any(w in n for w in words):
                present.add(k)
    return present

def score_recipe(recipe, have_set, expiring_set):
    # +2 if uses expiring items, +1 for any available ingredient match
    have_names = {normalize_name(i) for i in have_set}
    ing_names = {normalize_name(i["name"]) for i in recipe["ingredients"]}
    base = len(ing_names & have_names)
    exp = len(ing_names & expiring_set) * 2
    return base + exp

def suggest_recipes(recipes, have_set, expiring_set, excluded_allergens):
    # filter allergens
    candidates = []
    for r in recipes:
        if recipe_allergens(r) & set(excluded_allergens):
            continue
        candidates.append(r)
    # sort by score
    scored = sorted(candidates, key=lambda r: score_recipe(r, have_set, expiring_set), reverse=True)
    # pick top 3 diverse cuisines
    plan = []
    used_cuisines = set()
    for r in scored:
        if len(plan) == 3:
            break
        if r.get("cuisine") in used_cuisines:
            continue
        plan.append(r)
        used_cuisines.add(r.get("cuisine"))
    # fallback fill
    i = 0
    while len(plan) < 3 and i < len(scored):
        if scored[i] not in plan:
            plan.append(scored[i])
        i += 1
    return plan

def build_shopping_list(missing_list):
    # aggregate by name; in real life, sum amounts
    uniq = {}
    for m in missing_list:
        key = normalize_name(m["name"])
        if key not in uniq:
            uniq[key] = {"name": key, "count": 1}
        else:
            uniq[key]["count"] += 1
    return list(uniq.values())
