# blvcksyxx API & Pastebin

**Open‑source personal API platform** – a tiny FastAPI service exposing a few useful utilities (IP checker, placeholder image generator, mock user generator, User‑Agent parser) and a minimalist Pastebin.  The whole thing runs on **Python 3.11** and is completely self‑contained.

---

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Running locally (tmux)](#running-locally-tmux)
- [Deploying to a VPS (Nginx + Certbot)](#deploying-to-a-vps-nginx--certbot)
- [API Endpoints](#api-endpoints)
- [Pastebin UI](#pastebin-ui)
- [Development & Testing](#development--testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **FastAPI** powered JSON API on `api.blvcksyxx.xyz`
- **Scalar** UI for OpenAPI docs, with all Scalar AI buttons removed
- **Placeholder image** generator (`/image`)
- **Mock user** generator (`/mock/users`) – emails are always `@gmail.com`
- **IP address** endpoint (`/ip`)
- **User‑Agent** parser (`/ua`)
- **Pastebin** service on `dev.blvcksyxx.xyz` – raw snippet view, black‑and‑white brutalist UI
- **Zero‑dependency deployment** – just `uvicorn` + `nginx`
- **Tmux‑friendly** – keep services alive without systemd daemons
- **Ready for GitHub** – `.gitignore`, `requirements.txt`, CI workflow, MIT licence

---

## Demo
```
# API docs (Scalar) – live at:
https://api.blvcksyxx.xyz/docs

# Pastebin – raw snippet example:
https://dev.blvcksyxx.xyz/abcd1234
```
*(Replace the domain with your own when you deploy.)*

---

## Installation
```bash
# 1. Clone the repo
git clone https://github.com/your‑user/blvcksyxx-api.git
cd blvcksyxx-api

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running locally (tmux)
```bash
# Start a tmux session (optional but recommended)
tmux new-session -s blvcksyxx

# Inside tmux – activate venv and start the API
source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8028

# Open a new tmux window for Pastebin (Ctrl‑B then C)
source venv/bin/activate
uvicorn pastebin:app --host 127.0.0.1 --port 8023

# Detach from tmux (Ctrl‑B then D) – both services keep running
```
Both services stay up 24/7 as long as the tmux session lives.

---

## Deploying to a VPS (Nginx + Certbot)
1. **Install system packages** (run once on a fresh Ubuntu/Debian VPS)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx
```
2. **Copy the project** to a directory, e.g. `~/blvcksyxx-api` and repeat the *Installation* steps above.
3. **Create tmux services** as described in *Running locally (tmux)* – they will survive reboots if you add them to `~/.bashrc` or a simple `@reboot` cron entry.
4. **Configure Nginx** (replace `YOUR_IP` with your server’s IP):
```bash
# /etc/nginx/sites-available/api.blvcksyxx.xyz
server {
    listen 80;
    server_name api.blvcksyxx.xyz;
    location / { proxy_pass http://127.0.0.1:8028; }
}
# /etc/nginx/sites-available/dev.blvcksyxx.xyz
server {
    listen 80;
    server_name dev.blvcksyxx.xyz;
    location / { proxy_pass http://127.0.0.1:8023; }
}
```
Enable the sites and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/api.blvcksyxx.xyz /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/dev.blvcksyxx.xyz /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```
5. **Obtain free TLS certificates** (you’ll be asked for an email address):
```bash
sudo certbot --nginx -d api.blvcksyxx.xyz
sudo certbot --nginx -d dev.blvcksyxx.xyz
```
Certbot will automatically add the HTTPS blocks and enable HTTP→HTTPS redirects.

Your services are now reachable over **HTTPS** at the two sub‑domains.

---

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/ip` | Returns the caller’s IP address (checks `X‑Forwarded‑For`). |
| GET | `/image` | Generates a placeholder PNG. Query params: `width`, `height`, `bg_color`, `text_color`, `text`, `font_size`. |
| GET | `/mock/users` | Returns an array of mock users (1‑50). Emails always end with `@gmail.com`. |
| GET | `/ua` | Parses a User‑Agent string (optional `ua` query). |
| GET | `/about` | Static info about the author. |
| GET | `/status` | Simple health‑check JSON. |
| GET | `/docs` | Scalar UI – all UI text is forced to **lowercase**, AI buttons are hidden. |

---

## Pastebin UI
* **Create** – paste code at `POST /new` (HTML form). 
* **View** – `GET /{paste_id}` returns **plain‑text** (no HTML). 
* **UI** – black background, white monospace text, all labels are lowercase, lightning icon replaced by an arrow (`fa-arrow-turn-down`).

---

## Development & Testing
```bash
# Run tests (if you add them later)
pytest
```
A minimal CI workflow is included (see `.github/workflows/ci.yml`). It installs dependencies, runs lint (`ruff`) and, if you add tests, runs `pytest`.

---

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome‑thing`).
3. Make your changes, ensure `ruff format` and `ruff check` pass.
4. Open a Pull Request – CI will run automatically.

---

## License
MIT – see the `LICENSE` file.
