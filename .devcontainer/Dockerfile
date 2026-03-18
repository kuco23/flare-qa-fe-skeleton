FROM mcr.microsoft.com/devcontainers/python:3.13

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Install Claude Code (requires Node, installed via devcontainer feature)
# Node is added via the devcontainer feature, so we install claude in postCreateCommand
