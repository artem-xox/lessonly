## Lessonly

AI-powered app leveraging GPT technology to automatically create customized, engaging English lesson plans for students and teachers.

---

### Streamlit app pages

- **Block**: Generate a single lesson block (e.g., vocabulary, grammar, activity, reading, homework). Choose block type, level, and topic, optionally add a comment, then create a focused block ready to use.
- **Lesson**: Generate a complete lesson composed of multiple blocks tailored to a level and theme.
- **Dialog**: Chat with an AI lesson manager to refine, expand, or regenerate parts of a lesson interactively.

### Quickstart

1. **Set API key**
   - Export `OPENAI_API_KEY` (or `LESSONLY_OPENAI_API_KEY`).
2. **Install dependencies**
   - Using `uv`: `uv sync` (or `uv sync --dev` for development)
3. **Run the app**
   - `make run-app`
   - Or: `uv run streamlit run src/lessonly/interfaces/app/main.py`

### Documentation

- Product overview: [`docs/product.md`](docs/product.md)
- MVP design and modules: [`docs/mvp/design.md`](docs/mvp/design.md)
- Roadmap: [`docs/roadmap.md`](docs/roadmap.md)

---

### Deploy to Heroku (Docker)

This repository includes a Docker-based setup for deploying the Streamlit app to Heroku using GitHub integration.

Prerequisites:
- Heroku app connected to this GitHub repo
- Set the app stack to `container` in Heroku Settings
- Configure required config vars (e.g., `OPENAI_API_KEY` or `LESSONLY_OPENAI_API_KEY`)

Files added for container deploy:
- `Dockerfile`: builds the app image
- `entrypoint.sh`: starts Streamlit binding to `$PORT`
- `heroku.yml`: instructs Heroku to build and run the Docker image

Local test run (optional):

```bash
docker build -t lessonly:latest .
docker run -p 8501:8501 --env PORT=8501 lessonly:latest
```

Heroku notes:
- Ensure stack is set to `container`.
- With GitHub integration enabled, trigger a manual deploy or enable automatic deploys. Heroku will build using `heroku.yml`.
- The app listens on `$PORT` as required by Heroku.
