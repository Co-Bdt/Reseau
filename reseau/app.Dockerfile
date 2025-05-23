# This Dockerfile is used to deploy a single-container Reflex app instance
# to services like Render, Railway, Heroku, GCP, and others.

# It uses a reverse proxy to serve the frontend statically and proxy to backend
# from a single exposed port, expecting TLS termination to be handled at the
# edge by the given platform.

FROM python:3.11-slim

# If the service expects a different port, provide it here (f.e Render expects port 10000)
ARG PORT=3000
# Only set for local/direct access. When TLS is used, the API_URL is assumed to be the same as the frontend.
ARG API_URL
ENV PORT=$PORT API_URL=${API_URL:-http://localhost:$PORT}

# Install Caddy server inside image
RUN apt-get update -y && apt-get install -y caddy && rm -rf /var/lib/apt/lists/*

# Install unzip, curl packages for reflex init
RUN apt-get update && apt-get install -y unzip curl

WORKDIR /app

# Create a simple Caddyfile to serve as reverse proxy
RUN cat > Caddyfile <<EOF
:{\$PORT}

encode gzip

@backend_routes path /_event/* /ping /_upload /_upload/*
handle @backend_routes {
	reverse_proxy localhost:8000
}

root * /srv
route {
	try_files {path} {path}/ /404.html
	file_server
}
EOF

# Copy local context to `/app` inside container (see .dockerignore)
COPY . .

# Install app requirements and reflex in the container
RUN pip install -r requirements.txt

# Deploy templates and prepare app
RUN reflex init

# Download all npm dependencies and compile frontend
RUN reflex export --frontend-only --no-zip && mv .web/_static/* /srv/ && rm -rf .web

# Needed until Reflex properly passes SIGTERM on backend.
STOPSIGNAL SIGKILL

EXPOSE $PORT

# Initialize the database
RUN reflex db init

# Apply migrations before starting the backend.
CMD [ -d alembic ] && reflex db migrate; \
	caddy start && reflex run --env prod --backend-only --loglevel debug

# To ensure the image is associated with the correct repository
LABEL org.opencontainers.image.source="https://github.com/Co-Bdt/Reseau"