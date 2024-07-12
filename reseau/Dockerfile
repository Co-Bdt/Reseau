# This Dockerfile is used to deploy a simple single-container Reflex app instance.

FROM python:3.10-slim

# Copy local context to `/app` inside container (see .dockerignore)
WORKDIR /app
COPY . .

# Install app requirements and reflex in the container
RUN pip install -r requirements.txt

# Install unzip, curl packages for reflex init
RUN apt-get update && apt-get install -y unzip curl

# Deploy templates and prepare app
RUN reflex init

# Download all npm dependencies and compile frontend
RUN reflex export --frontend-only --no-zip

# Needed until Reflex properly passes SIGTERM on backend.
STOPSIGNAL SIGKILL

# Always apply migrations before starting the backend.
CMD [ -d alembic ] && reflex db migrate; reflex run --env prod

# To ensure the image is associated with the correct repository
LABEL org.opencontainers.image.source="https://github.com/Co-Bdt/Reseau"