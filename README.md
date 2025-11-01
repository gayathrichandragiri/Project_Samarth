# Project Samarth — Prototype Q&A over data.gov.in (Sample)

This is a small runnable prototype for the Project Samarth challenge.
It includes:
- Flask backend (app.py) with a simple `/api/ask` endpoint.
- Data fetcher & normalizer stubs (data_fetcher.py, normalizer.py).
- QA engine (qa_engine.py) that runs queries over included sample CSVs.
- Simple frontend (templates/demo.html + static/main.js).
- Sample mock datasets in `data_files/` so the app runs offline.

## Run (local)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
# open http://127.0.0.1:5000
```

Or run (production):
```
pip install -r requirements.txt
gunicorn app:app
```

## Notes
- The included datasets of real data.gov.in datasets for demo purposes.
- The QA engine implements simple heuristics to answer comparisons and top-k queries and always returns citations pointing to the sample CSV files.
- Replace dataset URLs in `dataset_registry.json` with real data.gov.in CSV URLs when moving to live mode.
