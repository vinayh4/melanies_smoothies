# Import python packages
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Melanie's Smoothies", page_icon="🥤")
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

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on Smoothie will be:", name_on_order)

st.title("Customize Your Smoothie")
st.write(
    """
  Choose the fruits you want in your custom smoothie
  """
)

fruit_records = [
    {"FRUIT_NAME": "Apple", "SEARCH_ON": "apple"},
    {"FRUIT_NAME": "Banana", "SEARCH_ON": "banana"},
    {"FRUIT_NAME": "Blueberry", "SEARCH_ON": "blueberry"},
    {"FRUIT_NAME": "Mango", "SEARCH_ON": "mango"},
    {"FRUIT_NAME": "Orange", "SEARCH_ON": "orange"},
    {"FRUIT_NAME": "Pineapple", "SEARCH_ON": "pineapple"},
    {"FRUIT_NAME": "Raspberry", "SEARCH_ON": "raspberry"},
    {"FRUIT_NAME": "Strawberry", "SEARCH_ON": "strawberry"},
]
pd_df = pd.DataFrame(fruit_records)
fruit_options = pd_df["FRUIT_NAME"].tolist()

ingredients_list = st.multiselect(
    "Choose your ingredients (more than 5 allowed):",
    fruit_options,
)
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"].iloc[0]
        st.write("The search value for", fruit_chosen, "is", search_on, ".")
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}", timeout=10
        )
        smoothiefroot_response.raise_for_status()
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        ingredients_sql = ingredients_string.replace("'", "''")
        name_sql = name_on_order.replace("'", "''")
        my_insert_stmt = f"""
            insert into smoothies.public.orders(ingredients, name_on_order)
            values ('{ingredients_sql}', '{name_sql}')
        """
        cnx = st.connection("snowflake")
        session = cnx.session()
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}", icon="✅")
