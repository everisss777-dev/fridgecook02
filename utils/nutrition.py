
import json
from pathlib import Path

class NutritionDB:
    def __init__(self, path: Path):
        self.db = json.loads(path.read_text(encoding="utf-8"))
    def get(self, name: str):
        name = name.lower()
        return self.db.get(name, {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0, "sodium": 0})

def estimate_recipe_nutrition(recipe: dict, ndb: "NutritionDB"):
    # simple sum over ingredients, assuming per-serving split already approximate
    total = {"kcal":0,"protein":0,"fat":0,"carbs":0,"sodium":0}
    for ing in recipe["ingredients"]:
        info = ndb.get(ing["name"])
        total = {k: total[k] + info.get(k,0) for k in total}
    # assume 2 servings default
    per = {k: round(v/2) for k,v in total.items()}
    return per

def nutrition_table_to_md(n: dict) -> str:
    return (
        "\n**Nutrition (per serving)**\n\n"
        "| kcal | protein(g) | fat(g) | carbs(g) | sodium(mg) |\n"
        "|---:|---:|---:|---:|---:|\n"
        f"| {n['kcal']} | {n['protein']} | {n['fat']} | {n['carbs']} | {n['sodium']} |\n"
    )
