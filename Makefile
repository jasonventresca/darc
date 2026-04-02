# DARC — Diagrams as Rendered Code
#
# Render all PlantUML diagrams to PNG and SVG.
#
# Prerequisites:
#   PlantUML server running at PLANTUML_SERVER (default: http://localhost:8080).
#   Start one with:  docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
#
# Usage:
#   make              # render all .puml files to PNG + SVG
#   make images       # same as above
#   make png          # PNG only
#   make svg          # SVG only
#   make clean        # remove generated images

PLANTUML_SERVER ?= http://localhost:8080
RENDER = python3 render_puml.py -s $(PLANTUML_SERVER)

PUML_FILES := $(wildcard *.puml)
PNG_FILES  := $(PUML_FILES:.puml=.png)
SVG_FILES  := $(PUML_FILES:.puml=.svg)

.PHONY: all images png svg clean

all: images

images: png svg

png: $(PNG_FILES)

svg: $(SVG_FILES)

%.png: %.puml render_puml.py
	$(RENDER) -f png $<

%.svg: %.puml render_puml.py
	$(RENDER) -f svg $<

clean:
	rm -f $(PNG_FILES) $(SVG_FILES)
