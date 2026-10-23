# TrustVault starter (Flask)

## Run on Acer Chromebook (Linux Terminal)
1. Extract this ZIP in your Linux files.
2. In Terminal, `cd` into the extracted `TrustVault_starter` folder.
3. Run:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install -r requirements.txt
   python3 app.py
   ```
4. Open `http://127.0.0.1:5000/` in Chrome.

## Create an admin locally
Stop the app (Ctrl+C), then in the same Terminal run:
```bash
export ADMIN_EMAIL="your-admin-email@example.com"
export ADMIN_PASSWORD="Choose-A-Long-Unique-Password"
python3 app.py
```
This creates the admin account on first startup if it does not already exist. Register ordinary users through the website. Never publish passwords or `.env` files.

## Deployment notes
- Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` as private environment variables in Render. Use a new strong password.
- This starter stores uploads and SQLite in `instance/`. On Render, the default filesystem may be ephemeral; local data/files will not automatically migrate and may disappear on redeploy. For reliable production use, configure a persistent disk and/or managed PostgreSQL plus persistent object storage. Do not claim data persistence until configured and tested.
- Set `SECRET_KEY` to a strong random value in deployment.
- Do not use real confidential documents for a demo.
- This is an educational starter, not a security-audited production service. Add CSRF protection, rate limiting, stronger admin provisioning, and managed persistent storage before real use.
