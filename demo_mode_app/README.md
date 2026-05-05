# Melanie's Smoothies (Demo Mode - No Snowflake)

This is a separate demo project that runs without Snowflake.

## What changed
- Fruit options are loaded from `data/fruit_options.csv`.
- Orders are saved locally to `data/orders.csv`.
- Nutrition details are still fetched from `https://my.smoothiefroot.com/api/fruit/{search_on}`.

## Run locally
```bash
cd demo_mode_app
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Notes
- `data/orders.csv` is created automatically on first run.
- This is ideal for demos/development when Snowflake is unavailable.
