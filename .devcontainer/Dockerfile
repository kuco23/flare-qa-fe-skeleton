FROM mcr.microsoft.com/devcontainers/python:3.13

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Place venv outside workspace so it exists before the mount overlays /workspaces
ENV UV_PROJECT_ENVIRONMENT=/home/vscode/.venv

# Pre-install Python dependencies so the interpreter is available on attach
COPY pyproject.toml uv.lock /tmp/build/
RUN cd /tmp/build && uv sync --no-install-project && rm -rf /tmp/build \
    && chown -R vscode:vscode /home/vscode/.venv

# Install Playwright browsers and their OS dependencies
RUN /home/vscode/.venv/bin/playwright install-deps \
    && su vscode -c "/home/vscode/.venv/bin/playwright install"
