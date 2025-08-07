## Lessonly

AI-powered app leveraging GPT technology to automatically create customized, engaging English lesson plans for students and teachers.

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
