#!/usr/bin/env python3
"""Render PlantUML diagrams to PNG or SVG via a local PlantUML server.

Part of DARC (Diagrams as Rendered Code).

Usage:
    python render_puml.py diagram.puml                     # PNG (default)
    python render_puml.py diagram.puml --format svg        # SVG
    python render_puml.py diagram.puml -o output.png       # custom output path
    python render_puml.py *.puml                           # multiple files
    python render_puml.py diagram.puml --server http://host:9999
"""

from __future__ import annotations

import argparse
import sys
import zlib
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

DEFAULT_SERVER = "http://localhost:8080"
SUPPORTED_FORMATS = ("png", "svg")

# PlantUML's custom base64 alphabet (different from standard base64)
_PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def _encode_6bit(value: int) -> str:
    """Encode a 6-bit value to a PlantUML base64 character."""
    return _PLANTUML_ALPHABET[value & 0x3F]


def _encode_3bytes(b0: int, b1: int, b2: int) -> str:
    """Encode 3 bytes into 4 PlantUML base64 characters."""
    return (
        _encode_6bit(b0 >> 2)
        + _encode_6bit(((b0 & 0x3) << 4) | (b1 >> 4))
        + _encode_6bit(((b1 & 0xF) << 2) | (b2 >> 6))
        + _encode_6bit(b2 & 0x3F)
    )


def plantuml_encode(text: str) -> str:
    """Encode PlantUML source text using the server's URL-safe encoding.

    The PlantUML server expects: deflate(utf-8 bytes) -> custom base64.
    """
    compressed = zlib.compress(text.encode("utf-8"))[2:-4]  # raw deflate (strip zlib header/checksum)

    encoded = []
    for i in range(0, len(compressed), 3):
        if i + 2 < len(compressed):
            encoded.append(_encode_3bytes(compressed[i], compressed[i + 1], compressed[i + 2]))
        elif i + 1 < len(compressed):
            encoded.append(_encode_3bytes(compressed[i], compressed[i + 1], 0))
        else:
            encoded.append(_encode_3bytes(compressed[i], 0, 0))

    return "".join(encoded)


def render(puml_path: Path, server_url: str, fmt: str, output_path: Path | None = None) -> Path:
    """Encode a .puml file and fetch the rendered image from the PlantUML server."""
    source = puml_path.read_text(encoding="utf-8")
    encoded = plantuml_encode(source)

    url = f"{server_url.rstrip('/')}/{fmt}/{encoded}"
    req = Request(url)

    try:
        with urlopen(req, timeout=30) as resp:
            data = resp.read()
    except URLError as exc:
        print(f"Error: Could not connect to PlantUML server at {url}\n  {exc}", file=sys.stderr)
        sys.exit(1)

    if output_path is None:
        output_path = puml_path.with_suffix(f".{fmt}")

    output_path.write_bytes(data)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render .puml files via a PlantUML server.")
    parser.add_argument("files", nargs="+", type=Path, help=".puml file(s) to render")
    parser.add_argument("-f", "--format", choices=SUPPORTED_FORMATS, default="png", help="output format (default: png)")
    parser.add_argument("-o", "--output", type=Path, default=None, help="output file path (only valid with a single input file)")
    parser.add_argument("-s", "--server", default=DEFAULT_SERVER, help=f"PlantUML server URL (default: {DEFAULT_SERVER})")
    args = parser.parse_args()

    if args.output and len(args.files) > 1:
        parser.error("--output can only be used with a single input file")

    for puml_path in args.files:
        if not puml_path.exists():
            print(f"Error: {puml_path} not found", file=sys.stderr)
            sys.exit(1)

        out = render(puml_path, args.server, args.format, args.output)
        print(f"{puml_path} -> {out}")


if __name__ == "__main__":
    main()
