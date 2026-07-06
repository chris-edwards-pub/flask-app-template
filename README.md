# flask-app-template

Cookiecutter template for Flask apps with Docker, AWS Lightsail deploy, and [AGENTS.md](https://agents.md) conventions.

## Usage

```bash
pip install cookiecutter
cookiecutter gh:chris-edwards-pub/flask-app-template
```

You'll be prompted for:

| Variable | Default | Purpose |
| --- | --- | --- |
| `project_name` | `Flask App` | Human-readable name (used in README, page titles) |
| `project_slug` | derived from name | Repo/dir/Docker image name (kebab-case) |
| `project_module` | `app` | Python package name |
| `project_description` | `A Flask web application` | Short description |
| `db_name` | derived from slug | MySQL database name (snake_case) |
| `author_name` | `Chris Edwards` | |
| `author_email` | `chris@edwards.pub` | |
| `github_username` | `chris-edwards-pub` | Used in Docker image name for GHCR |
| `aws_region` | `us-east-1` | Lightsail region |
| `python_version` | `3.13` | |
| `initial_admin_email` | `admin@<slug>.local` | Bootstrap admin user's email |
| `initial_version` | `0.1.0` | Starting semver in `VERSIONS.md` |

## What's included

- Flask app factory pattern (`{{project_module}}/__init__.py`)
- SQLAlchemy + Flask-Migrate with a clean initial `users` migration
- Auth blueprint: login, register-via-invite, logout, forgot/reset password, profile
- Bootstrap 5 responsive base template + login/register/profile pages
- 3-container Docker Compose stack: web (Flask/Gunicorn), db (MySQL 8), local dev only
- Production deploy: GitHub Actions → GHCR → AWS Lightsail Container Service
- Trivy daily vulnerability scan + weekly GHCR cleanup
- pytest with in-memory SQLite fixtures (`admin_user`, `logged_in_client`)
- `AGENTS.md` project standards + `CLAUDE.md` symlink for Claude Code
- Code style: Black (88), isort, flake8 (120)

## What's NOT included

Deliberately left out — add if you need them:

- S3 / object storage (starter uses local `uploads/` volume)
- Email / SES / notification framework
- Profile pictures / avatars
- Terraform IaC
- Any domain-specific models beyond `User`

## After generation

The post-gen hook automatically:

1. Runs `git init` and creates an initial commit
2. Creates the `CLAUDE.md` symlink to `AGENTS.md`

You still need to:

1. Create the empty repo on GitHub and add the remote
2. Copy `.env.example` → `.env` and set `SECRET_KEY`, `INIT_ADMIN_PASSWORD`
3. `docker compose up --build` to run locally, or `./dev.sh start` for host-mode Flask
