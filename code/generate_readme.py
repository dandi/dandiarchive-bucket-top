#!/usr/bin/env python3
"""Generate root/README.md from dandiarchive.yaml."""

import re
import sys
import textwrap
from pathlib import Path

import yaml

# Target width for text wrapping
WRAP_WIDTH = 80


def wrap_paragraph(text: str, width: int = WRAP_WIDTH) -> str:
    """Wrap a paragraph to specified width."""
    return textwrap.fill(text, width=width)


def wrap_list_item(text: str, width: int = WRAP_WIDTH) -> str:
    """Wrap a list item, indenting continuation lines."""
    if not text.startswith("- "):
        return text
    # Find the content after "- "
    prefix = "- "
    content = text[2:]
    # Wrap with subsequent indent of 2 spaces
    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent="",
        subsequent_indent="  ",
    )
    wrapped = wrapper.fill(content)
    return prefix + wrapped


def strip_markdown_links(text: str) -> str:
    """Convert [text](url) to just text."""
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)


def extract_url_from_markdown(text: str) -> str | None:
    """Extract URL from [text](url) format."""
    match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', text)
    if match:
        return match.group(2)
    return None


def parse_description(description: str) -> dict:
    """Parse the YAML description into sections."""
    result = {
        "intro": [],
        "standards": [],
        "bucket_org": [],
        "acknowledgment": "",
    }

    lines = description.strip().split('\n')
    current_section = "intro"

    for line in lines:
        stripped = line.strip()

        if "Data is organized using community standards:" in stripped:
            current_section = "standards"
            continue
        elif "The S3 bucket is organized as follows:" in stripped:
            current_section = "bucket_org"
            continue
        elif stripped.startswith("Development of DANDI"):
            result["acknowledgment"] = stripped
            current_section = None
            continue

        if current_section == "intro" and stripped:
            result["intro"].append(stripped)
        elif current_section == "standards":
            # Parse standard links: [Name](url)
            match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', stripped.lstrip('- ').rstrip(',').rstrip(' and'))
            if match:
                std_name = match.group(1).replace(" - ", ": ")
                result["standards"].append(std_name)
        elif current_section == "bucket_org":
            # Parse: - **key/** - description (may span multiple lines)
            match = re.match(r'- \*\*([^*]+)\*\*\s*-\s*(.+)', stripped)
            if match:
                key = match.group(1).rstrip('/')
                desc = strip_markdown_links(match.group(2))
                result["bucket_org"].append([key, desc])
            elif result["bucket_org"] and stripped and not stripped.startswith("-"):
                # Continuation of previous description
                result["bucket_org"][-1][1] += " " + strip_markdown_links(stripped)

    return result


def generate_readme(yaml_path: Path) -> str:
    """Generate README.md content from YAML."""
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    lines = []

    # Title - extract short name from full name
    name = data.get("Name", "DANDI")
    # Extract acronym if present (e.g., "Distributed Archives... (DANDI)" -> "DANDI")
    match = re.search(r'\(([A-Z]+)\)', name)
    if match:
        acronym = match.group(1)
        full_name = name.replace(f" ({acronym})", "")
        lines.append(f"# {acronym}: {full_name}")
    else:
        lines.append(f"# {name}")
    lines.append("")

    # Parse description
    description = data.get("Description", "").strip()
    desc = parse_description(description)

    # Introduction paragraph
    if desc["intro"]:
        lines.append(wrap_paragraph(' '.join(desc["intro"])))
        lines.append("")

    # Standards list
    if desc["standards"]:
        lines.append("The data uses a set of community standards:")
        for std in desc["standards"]:
            lines.append(f"- {std}")
        lines.append("")

    # Acknowledgment
    if desc["acknowledgment"]:
        lines.append(desc["acknowledgment"])
        lines.append("")

    # Dandisets section
    lines.append("## Dandisets")
    lines.append("")
    dandisets_text = (
        "We define a DANDI dataset as a Dandiset. A Dandiset is an organized "
        "collection of assets (files) with both file level and dataset level "
        "metadata generated from an experiment or a project."
    )
    lines.append(wrap_paragraph(dandisets_text))
    lines.append("")

    # Web resources section
    lines.append("### Web resources")
    lines.append("")

    # Documentation URL
    doc_url = data.get("Documentation", "")
    if doc_url:
        lines.append(f"- Web interface: {doc_url}")

    # Add API from Tools & Applications (look for "DANDI API" exactly)
    dataatwork = data.get("DataAtWork", {})
    tools = dataatwork.get("Tools & Applications", [])
    for tool in tools:
        title = tool.get("Title", "")
        if title == "DANDI API":
            lines.append(f"- API: {tool['URL']}")
            break

    # Handbook - hardcoded as it's not in YAML
    lines.append("- Handbook: https://handbook.dandiarchive.org")

    # Contact/Helpdesk
    contact = data.get("Contact", "")
    contact_url = extract_url_from_markdown(contact)
    if contact_url:
        lines.append(f"- Helpdesk: {contact_url}")

    # Github - hardcoded as it's not in YAML
    lines.append("- Github: https://github.com/dandi")

    # S3 Location from Resources
    resources = data.get("Resources", [])
    for res in resources:
        arn = res.get("ARN", "")
        if arn.startswith("arn:aws:s3:::"):
            bucket_name = arn.replace("arn:aws:s3:::", "")
            lines.append(f"- S3 Location: s3://{bucket_name}/")
            break

    # JupyterHub from Tools
    for tool in tools:
        if "JupyterHub" in tool.get("Title", ""):
            hub_line = (
                f"- DANDI Hub (a JupyterHub instance): {tool['URL']} "
                "(Requires registration via the Web interface)"
            )
            lines.append(wrap_list_item(hub_line))
            break

    lines.append("")

    # Organization of S3 bucket - use parsed data
    lines.append("### Organization of the S3 bucket")
    lines.append("")

    for key, description in desc["bucket_org"]:
        lines.append(wrap_list_item(f"- **{key}** - {description}"))

    lines.append("")

    # Other prefixes note
    lines.append("Other prefixes in the bucket can be ignored. For example:")
    lines.append("")
    lines.append(wrap_list_item(
        "- _dandiarchive_ - This folder stores an inventory listing of all items "
        "in the bucket. This is generated automatically by the S3 Inventory service."
    ))
    lines.append("")

    # Tools & Applications section
    lines.append("### Tools & Applications")
    lines.append("")
    for tool in tools:
        title = tool.get("Title", "")
        url = tool.get("URL", "")
        author = tool.get("AuthorName", "")
        if title and url:
            lines.append(f"- [{title}]({url}) - {author}")
    lines.append("")

    # Tutorials section
    tutorials = dataatwork.get("Tutorials", [])
    if tutorials:
        lines.append("### Tutorials")
        lines.append("")
        for tut in tutorials:
            title = tut.get("Title", "")
            url = tut.get("URL", "")
            author = tut.get("AuthorName", "")
            if title and url:
                lines.append(f"- [{title}]({url}) - {author}")
        lines.append("")

    # Publications section
    publications = dataatwork.get("Publications", [])
    if publications:
        lines.append("### Publications")
        lines.append("")
        for pub in publications:
            title = pub.get("Title", "")
            url = pub.get("URL", "")
            author = pub.get("AuthorName", "")
            if title and url:
                lines.append(f"- [{title}]({url}) - {author}")
        lines.append("")

    # Keywords section
    tags = data.get("Tags", [])
    # Filter out aws-pds tag
    tags = [t for t in tags if t != "aws-pds"]
    if tags:
        lines.append("#### Keywords:")
        lines.append("")
        for tag in sorted(tags):
            lines.append(f"- {tag}")
        lines.append("")

    return '\n'.join(lines)


def main():
    yaml_path = Path("sourcedata/open-data-registry/datasets/dandiarchive.yaml")
    output_path = Path("root/README.md")

    if not yaml_path.exists():
        print(f"Error: {yaml_path} not found", file=sys.stderr)
        sys.exit(1)

    readme_content = generate_readme(yaml_path)

    # If --dry-run, print to stdout instead of writing
    if "--dry-run" in sys.argv:
        print(readme_content)
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(readme_content)
        print(f"Generated {output_path}")


if __name__ == "__main__":
    main()
