#!/usr/bin/env python3
"""Generate root/index.html from root/README.md using pandoc.

Requires either:
- pandoc installed system-wide, OR
- pypandoc Python package (will use bundled pandoc or download if needed)
"""

import shutil
import subprocess
import sys
from pathlib import Path

# DANDI logo URL (from GitHub organization avatar)
DANDI_LOGO_URL = (
    "https://avatars.githubusercontent.com/u/53260526"
    "?s=400&u=9fd82f767e66beeb3959efaf11be707dd4209c96&v=4"
)

# Minimal CSS styling
CSS_STYLE = """body {
    color: black;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}
a {
    color: #0366d6;
}
h1, h2, h3, h4 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}
ul {
    padding-left: 2em;
}
code {
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
}
"""

# HTML template
HTML_TEMPLATE = """<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DANDI Archive</title>
<style>
{css}
</style>
</head>
<body>
<p><img src="{logo_url}" width="200px" alt="DANDI Logo"></p>
{content}
</body>
</html>
"""


def convert_markdown_to_html(markdown_path: Path) -> str:
    """Convert markdown file to HTML body using pandoc.

    Tries system pandoc first, falls back to pypandoc if available.
    """
    # Pandoc format with autolink extension to make bare URLs clickable
    pandoc_format = "markdown+autolink_bare_uris"

    # Try system pandoc first
    if shutil.which("pandoc"):
        try:
            result = subprocess.run(
                ["pandoc", "-f", pandoc_format, "-t", "html", str(markdown_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running pandoc: {e.stderr}", file=sys.stderr)
            sys.exit(1)

    # Fall back to pypandoc
    try:
        import pypandoc
    except ImportError:
        print(
            "Error: pandoc not found and pypandoc not installed.\n"
            "Please either:\n"
            "  - Install pandoc: https://pandoc.org/installing.html\n"
            "  - Or install pypandoc: pip install pypandoc",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        return pypandoc.convert_file(str(markdown_path), "html", format=pandoc_format)
    except OSError as e:
        if "No pandoc was found" in str(e):
            print(
                "pypandoc found but pandoc binary missing.\n"
                "Run: python -c \"import pypandoc; pypandoc.download_pandoc()\"",
                file=sys.stderr,
            )
            sys.exit(1)
        raise


def generate_html(readme_path: Path, output_path: Path) -> None:
    """Generate index.html from README.md."""
    html_body = convert_markdown_to_html(readme_path)

    full_html = HTML_TEMPLATE.format(
        css=CSS_STYLE,
        logo_url=DANDI_LOGO_URL,
        content=html_body,
    )

    with open(output_path, "w") as f:
        f.write(full_html)


def main():
    readme_path = Path("root/README.md")
    output_path = Path("root/index.html")

    if not readme_path.exists():
        print(f"Error: {readme_path} not found", file=sys.stderr)
        sys.exit(1)

    generate_html(readme_path, output_path)

    # If --dry-run, print to stdout instead of message
    if "--dry-run" not in sys.argv:
        print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
