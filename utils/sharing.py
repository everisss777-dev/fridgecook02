
import streamlit as st

def get_state_from_query(state):
    params = st.experimental_get_query_params()
    if "lang" in params: state.lang = params["lang"][0]
    if "theme" in params: state.theme = params["theme"][0]
    if "allergens" in params: state.excluded_allergens = params["allergens"][0].split(",") if params["allergens"][0] else []
    if "ingredients" in params: state.ingredient_text = params["ingredients"][0]

def set_query_from_state(state):
    q = {
        "lang": state.lang,
        "theme": state.theme,
        "allergens": ",".join(state.excluded_allergens) if state.get("excluded_allergens") else "",
        "ingredients": state.get("ingredient_text","")
    }
    st.experimental_set_query_params(**q)
