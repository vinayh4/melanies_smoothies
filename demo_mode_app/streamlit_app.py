import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Melanie's Smoothies (Demo)", page_icon="🥤")

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    }
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    p, label, li, [data-testid="stMarkdownContainer"] {
        font-size: 1rem;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FRUIT_OPTIONS_PATH = DATA_DIR / "fruit_options.csv"
ORDERS_PATH = DATA_DIR / "orders.csv"


def ensure_orders_file() -> None:
    if not ORDERS_PATH.exists():
        pd.DataFrame(columns=["ordered_at_utc", "name_on_order", "ingredients"]).to_csv(
            ORDERS_PATH, index=False
        )


def load_fruit_options() -> pd.DataFrame:
    return pd.read_csv(FRUIT_OPTIONS_PATH)


def fetch_nutrition(search_on: str) -> dict:
    response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}", timeout=10)
    response.raise_for_status()
    return response.json()


def save_order(name_on_order: str, ingredients_list: list[str]) -> None:
    ensure_orders_file()
    new_row = {
        "ordered_at_utc": datetime.now(timezone.utc).isoformat(),
        "name_on_order": name_on_order,
        "ingredients": json.dumps(ingredients_list),
    }
    existing = pd.read_csv(ORDERS_PATH)
    updated = pd.concat([existing, pd.DataFrame([new_row])], ignore_index=True)
    updated.to_csv(ORDERS_PATH, index=False)


st.title("Customize Your Smoothie (Demo Mode)")
st.caption("This version runs with local CSV files and does not require Snowflake.")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on Smoothie will be:", name_on_order)

fruit_df = load_fruit_options()
fruit_options = fruit_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose your ingredients (more than 5 allowed):",
    fruit_options,
)

if ingredients_list:
    st.subheader("Nutrition Information")
    for fruit_chosen in ingredients_list:
        search_on = fruit_df.loc[
            fruit_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON",
        ].iloc[0]
        st.write("The search value for", fruit_chosen, "is", search_on, ".")
        try:
            nutrition = fetch_nutrition(search_on)
            st.dataframe(data=nutrition, use_container_width=True)
        except requests.RequestException as exc:
            st.error(f"Could not fetch nutrition for {fruit_chosen}: {exc}")

    if st.button("Submit Order"):
        save_order(name_on_order=name_on_order, ingredients_list=ingredients_list)
        st.success(f"Your Smoothie is ordered, {name_on_order}", icon="✅")

st.divider()
st.subheader("Recent Demo Orders")
ensure_orders_file()
orders_df = pd.read_csv(ORDERS_PATH)
if orders_df.empty:
    st.info("No demo orders yet. Submit one above!")
else:
    st.dataframe(orders_df.tail(20), use_container_width=True)
