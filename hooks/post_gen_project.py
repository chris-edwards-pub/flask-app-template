# Post-generation hook for flask-app-template.
#
# Runs inside the generated project directory. Cookiecutter renders this file
# with Jinja *before* executing it, so cookiecutter references below resolve
# to the values the user chose.

import os
import stat
import subprocess
from pathlib import Path

PROJECT_ROOT = Path.cwd()

# Values baked in at generation time.
IMAGE_NAME = "{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PROJECT_MODULE = "{{ cookiecutter.project_module }}"
AWS_REGION = "{{ cookiecutter.aws_region }}"
GITHUB_USERNAME = "{{ cookiecutter.github_username }}"


def substitute_workflow_placeholders() -> None:
    # Workflows are in _copy_without_render because GitHub Actions expression
    # syntax collides with Jinja. Replace __PLACEHOLDER__ tokens with real
    # values here.
    workflow_dir = PROJECT_ROOT / ".github" / "workflows"
    replacements = {
        "__IMAGE_NAME__": IMAGE_NAME,
        "__PROJECT_SLUG__": PROJECT_SLUG,
        "__PROJECT_MODULE__": PROJECT_MODULE,
        "__AWS_REGION__": AWS_REGION,
        "__GITHUB_USERNAME__": GITHUB_USERNAME,
    }
    for workflow in workflow_dir.glob("*.yml"):
        text = workflow.read_text()
        for placeholder, value in replacements.items():
            text = text.replace(placeholder, value)
        workflow.write_text(text)


def create_claude_symlink() -> None:
    """Create CLAUDE.md → AGENTS.md so Claude Code loads the same standards."""
    claude_path = PROJECT_ROOT / "CLAUDE.md"
    if claude_path.exists() or claude_path.is_symlink():
        claude_path.unlink()
    claude_path.symlink_to("AGENTS.md")


def make_scripts_executable() -> None:
    for script in ("dev.sh", "entrypoint.sh"):
        path = PROJECT_ROOT / script
        if path.exists():
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def git_init() -> None:
    """Initialize git and make the first commit. Skips silently if git is missing."""
    try:
        subprocess.run(["git", "init", "-q", "-b", "master"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            [
                "git",
                "commit",
                "-q",
                "-m",
                "Initial scaffold from flask-app-template",
            ],
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass


def print_next_steps() -> None:
    print()
    print(f"[OK] Generated {PROJECT_SLUG}")
    print()
    print("Next steps:")
    print(f"  cd {PROJECT_SLUG}")
    print("  cp .env.example .env    # then set SECRET_KEY, INIT_ADMIN_PASSWORD")
    print("  docker compose up --build")
    print()
    print("Then create the GitHub repo and push:")
    print(f"  gh repo create {GITHUB_USERNAME}/{PROJECT_SLUG} --public --source=. --push")
    print()
    print("See README.md for full instructions.")


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    substitute_workflow_placeholders()
    create_claude_symlink()
    make_scripts_executable()
    git_init()
    print_next_steps()
