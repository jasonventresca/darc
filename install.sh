#!/usr/bin/env bash
#
# DARC install script
#
# Pulls the PlantUML Docker image and verifies that required tools are present.
# Assumes Python 3 is already installed.

set -euo pipefail

info()  { printf '==> %s\n' "$*"; }
err()   { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# --- Check prerequisites ---------------------------------------------------

command -v docker >/dev/null 2>&1 || err "Docker is not installed. Please install Docker first: https://docs.docker.com/get-docker/"
command -v python3 >/dev/null 2>&1 || err "Python 3 is not installed."
command -v make >/dev/null 2>&1 || err "make is not installed."

# --- Pull the PlantUML Docker image -----------------------------------------

IMAGE="plantuml/plantuml-server:jetty"

info "Pulling Docker image: $IMAGE"
docker pull "$IMAGE"

# --- Done -------------------------------------------------------------------

info "Installation complete."
info ""
info "To start the PlantUML server:"
info "  docker run -d -p 8080:8080 $IMAGE"
info ""
info "Then render diagrams with:"
info "  make"
