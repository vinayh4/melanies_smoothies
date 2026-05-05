# Melanie's Smoothies (Demo Mode - No Snowflake)

This is a separate demo project that runs without Snowflake.

## What changed
- Fruit options are loaded from `data/fruit_options.csv` when available.
- If `data/fruit_options.csv` is missing or malformed, the app falls back to built-in demo fruits.
- Orders are saved locally to `data/orders.csv`.
- Nutrition details are fetched from `https://my.smoothiefroot.com/api/fruit/{search_on}` when network is available.

## Run locally
```bash
cd demo_mode_app
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Troubleshooting
- If `streamlit` is not found, always use: `python -m streamlit run streamlit_app.py`.
- If you are in a remote container/VM, `localhost` in your personal browser may not reach the app process. Use port forwarding for port `8501`.
- If nutrition API calls fail, the app still works for placing demo orders locally.
- If you see SSL certificate verification failures on Windows, run: `python -m pip install --upgrade certifi` and retry.

## Notes
- `data/orders.csv` is created automatically on first run.
- This is ideal for demos/development when Snowflake is unavailable.
