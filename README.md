# dandiarchive-bucket-top

Tools for managing the top-level content of the DANDI Archive S3 bucket
(`s3://dandiarchive/`), keeping it in sync with the AWS Open Data Registry
metadata.

## Overview

This repository maintains:

- **root/README.md** - The README displayed at the S3 bucket root, generated
  from the DANDI entry in the AWS Open Data Registry
- **root/index.html** - HTML version of the README for web browsers
- **sourcedata/open-data-registry/** - Git submodule containing the DANDI fork
  of the AWS Open Data Registry, with `datasets/dandiarchive.yaml` as the
  source of truth for metadata

## Workflow

```
dandiarchive.yaml  →  root/README.md  →  root/index.html  →  S3 bucket
    (source)           (generated)        (generated)         (deployed)
```

1. Metadata lives in `sourcedata/open-data-registry/datasets/dandiarchive.yaml`
2. `code/generate_readme.py` creates `root/README.md` from the YAML
3. `code/generate_html.py` converts the README to `root/index.html`
4. `code/sync_bucket.sh` syncs `root/` to/from the S3 bucket

## Quick Start

```bash
# Generate README and HTML from YAML
make generate

# Preview changes (dry-run sync to bucket)
make to_bucket DRY_RUN=1

# Sync from bucket to local
make from_bucket

# Sync to bucket (requires AWS credentials)
make to_bucket
```

## Dependencies

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Python package manager
- [datalad](https://www.datalad.org/) - For reproducible script execution
- AWS CLI - For S3 sync operations (must be configured with appropriate credentials)
- pandoc - For markdown to HTML conversion (or pypandoc-binary Python package)

Python packages (installed automatically via uv):
- pyyaml - YAML parsing
- pypandoc-binary - Pandoc wrapper with bundled pandoc (if system pandoc unavailable)

## Make Targets

| Target | Description |
|--------|-------------|
| `make generate` | Generate both README.md and index.html |
| `make readme` | Generate root/README.md from dandiarchive.yaml |
| `make html` | Generate root/index.html from root/README.md |
| `make from_bucket` | Sync top-level files from S3 bucket to root/ |
| `make to_bucket` | Sync root/ to S3 bucket (add `DRY_RUN=1` to preview) |
| `make validate` | Validate dandiarchive.yaml against schema |

## Proposing Changes to dandiarchive.yaml

The DANDI metadata in the AWS Open Data Registry is the source of truth.
To propose changes:

1. **Make changes locally**
   ```bash
   # Edit the YAML file
   $EDITOR sourcedata/open-data-registry/datasets/dandiarchive.yaml
   ```

2. **Validate and test**
   ```bash
   # Validate YAML against schema
   make validate

   # Regenerate README and HTML
   make generate

   # Review the changes
   git diff root/
   ```

3. **Commit to DANDI fork**
   ```bash
   cd sourcedata/open-data-registry
   git add datasets/dandiarchive.yaml
   git commit -m "Update dandiarchive.yaml: <description>"
   git push origin master
   ```

4. **Submit PR to upstream**
   - Go to https://github.com/dandi/open-data-registry
   - Create a pull request to https://github.com/awslabs/open-data-registry
   - Include clear description of what changed and why

5. **After upstream merge**
   ```bash
   # Update submodule to track upstream
   cd sourcedata/open-data-registry
   git fetch upstream
   git merge upstream/master
   git push origin master

   # Update submodule reference in parent repo
   cd ../..
   git add sourcedata/open-data-registry
   git commit -m "Update open-data-registry submodule"
   ```

## Repository Structure

```
dandiarchive-bucket-top/
├── README.md                 # This file
├── Makefile                  # Build orchestration
├── code/
│   ├── generate_readme.py    # YAML → README.md
│   ├── generate_html.py      # README.md → index.html
│   └── sync_bucket.sh        # S3 sync operations
├── docs/
│   └── spec-1.md             # Design specification
├── root/                     # Mirror of bucket top-level
│   ├── README.md             # Generated from dandiarchive.yaml
│   ├── index.html            # Generated from README.md
│   └── ...                   # Other bucket files
└── sourcedata/
    ├── open-data-registry/   # Submodule: AWS Open Data Registry fork
    └── dandi-docs/           # Submodule: DANDI documentation
```

## Related Resources

- [DANDI Archive](https://dandiarchive.org) - Main web interface
- [DANDI API](https://api.dandiarchive.org/swagger/) - REST API
- [DANDI Handbook](https://handbook.dandiarchive.org) - User documentation
- [AWS Open Data Registry](https://registry.opendata.aws/dandiarchive/) - DANDI entry
