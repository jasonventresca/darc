# DARC — Diagrams as Rendered Code

A lightweight toolkit for rendering PlantUML diagrams to PNG and SVG images
via a local PlantUML server. Zero dependencies beyond Python 3 and Docker.

## Why this exists

Modern development workflows with LLMs make it easy to generate PlantUML
diagrams from your codebase — just ask your AI assistant to read the code and
produce a `.puml` file. DARC gives you a simple, repeatable way to turn
those `.puml` source files into images you can check into version control,
embed in docs, or share with your team.

**Workflow:**

1. Chat with an LLM and ask it to generate a PlantUML diagram of your
   codebase (architecture, flows, ERDs, etc.).
2. Save the output as a `.puml` file in this directory.
3. Run `make` to render PNG and SVG images.
4. Commit the `.puml` source (and optionally the images) to your repo.

## Quick start

```bash
# 1. Install dependencies (pulls the PlantUML Docker image)
make setup

# 2. Start the PlantUML server
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty

# 3. Drop your .puml files into this directory, then:
make
```

That's it. Every `.puml` file gets rendered to both PNG and SVG.

## Environment setup

The only prerequisite is a PlantUML server running in Docker.
These instructions are adapted from https://plantuml.com/starting.

### 1. Pull the PlantUML Docker image

```bash
docker pull plantuml/plantuml-server:jetty
```

### 2. Start the server

```bash
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
```

- `-d` runs the container in detached mode.
- `-p 8080:8080` maps container port 8080 to your host.

Once running, you can also visit http://localhost:8080/ in your browser to use
the interactive editor (paste PlantUML code and see the diagram update live).

### 3. Stop the server (when done)

```bash
docker ps                    # find the container ID
docker stop <CONTAINER_ID>   # stop it
docker rm <CONTAINER_ID>     # optionally remove it
```

## Rendering images

### Generate all images

From this directory:

```bash
make              # renders every .puml to both PNG and SVG
make images       # same as above
make png          # PNG only
make svg          # SVG only
```

To use a different server address:

```bash
make PLANTUML_SERVER=http://myhost:9999
```

### Render a single file

Use `render_puml.py` directly:

```bash
python3 render_puml.py my-diagram.puml              # PNG (default)
python3 render_puml.py my-diagram.puml -f svg       # SVG
python3 render_puml.py my-diagram.puml -o out.png   # custom output path
python3 render_puml.py *.puml                       # all files at once
```

### Clean generated images

```bash
make clean        # removes all .png and .svg files
```

## Editing diagrams

Edit the `.puml` source files, then re-run `make`. The Makefile tracks
dependencies so only changed diagrams are re-rendered.

For PlantUML syntax reference, see: https://plantuml.com/

## What's included

| File | Purpose |
|------|---------|
| `install.sh` | One-time setup: checks prerequisites (Docker, Python 3, make) and pulls the PlantUML Docker image. Run via `make setup`. |
| `render_puml.py` | Python script that encodes `.puml` source and fetches rendered images from the PlantUML server. Uses only the standard library (no pip install needed). |
| `Makefile` | Dependency-tracked build: renders all `.puml` files to PNG + SVG, with incremental rebuilds. Also provides `make setup`. |
| `*.puml` | Your PlantUML diagram source files (add your own here). |
