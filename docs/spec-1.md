The goal in this repository to sync two way (starting from bucket to local) the top folder content (files like README.md) of 

- the dandiarchive S3 bucket,
  - and in particular its README.md and produced from it index.html
- the description for dandiarchive bucket within https://github.com/awslabs/open-data-registry/blob/HEAD/datasets/dandiarchive.yaml 

We need to design a solution to facilitate keeping them in sync as to
modify within git repo, and trigger updates on the bucket.

Preliminary idea is that the source of truth for README.md would be within the https://github.com/awslabs/open-data-registry/blob/HEAD/datasets/dandiarchive.yaml .
We will keep that https://github.com/awslabs/open-data-registry/ git repo as subdataset under sourcedata/open-data-registry with a fork on our DANDI archive (https://github.com/dandi/open-data-registry) -- that is already done.
The schema for that yaml is thus readily available under sourcedata/open-data-registry/schema.yaml .

Then we would sync bucket to/from `root/` folder.
`code/` folder should provide script to 'sync' (using e.g. aws CLI), and README.md on top level of this repo should describe the purpose of this repository.

`Makefile` on top of this repo should have invocations for syncing to centralize potential actions to be taken.

Within this work we should plan to extend already existing
sourcedata/open-data-registry/datasets/dandiarchive.yaml with information
present in root/README.md and sourcedata/dandi-docs (rendered is at
https://docs.dandiarchive.org/) while following that sourcedata/open-data-registry/schema.yaml and establish TODO on what other metadata to provide there.

We know that it would be great to point to specific usecases of use of data
from the bucket, could be e.g. navigating Zarr(s) and or doing analytics, but
likely just to refer to docs oneline.

---

## Implementation Plan

### Current State Analysis

The repository already has:
- `root/` containing synced bucket content: `README.md`, `index.html`, `ros3test.hdf5`, `ros3test.nwb`
- `sourcedata/open-data-registry/` submodule (DANDI fork)
- `sourcedata/dandi-docs/` submodule (rendered at docs.dandiarchive.org)
- Basic `Makefile` with `from_bucket` target for S3 sync
- Empty `code/` directory

### Architecture

```
dandiarchive-bucket-top/
├── Makefile                 # Central orchestration of all actions
├── README.md                # Repository documentation (to create)
├── code/
│   ├── sync_bucket.sh       # S3 sync operations (from/to bucket)
│   ├── generate_readme.py   # Generate root/README.md from dandiarchive.yaml
│   └── generate_html.py     # Convert README.md to index.html
├── docs/
│   └── spec-1.md            # This specification
├── root/                    # Mirror of bucket top-level content
│   ├── README.md            # Generated from dandiarchive.yaml
│   ├── index.html           # Generated from README.md
│   └── ...                  # Other bucket files (ros3test.*)
└── sourcedata/
    ├── open-data-registry/  # Submodule: source of truth for metadata
    │   └── datasets/dandiarchive.yaml
    └── dandi-docs/          # Submodule: additional documentation source
```

### Implementation Steps

**Note**: Each step must result in one or more git commits with clear descriptions
of what was achieved. Keep commits atomic and well-documented.

#### Step 1: Enhance dandiarchive.yaml

Extend `sourcedata/open-data-registry/datasets/dandiarchive.yaml` to include:

**First**: Incorporate content already present in `root/README.md` (synced from bucket)
that is missing from dandiarchive.yaml.

**Note**: `RegistryEntryAdded` and `RegistryEntryLastModified` fields are auto-populated
from git history by `sourcedata/open-data-registry/_scripts/add_metadata.sh` - no need
to maintain manually.

**Validation**: The open-data-registry uses `pykwalify` for schema validation. To validate:
```bash
cd sourcedata/open-data-registry
pykwalify -d datasets/dandiarchive.yaml -s schema.yaml
```
The schema.yaml references `ext.py` for custom validation functions (tags from `tags.yaml`,
resources from `resources.yaml`, ARN format, etc.). Validation must pass before committing.

**Important guidelines**:
- Do NOT modify `RegistryEntryAdded` or `RegistryEntryLastModified` fields - these are
  auto-populated from git history by upstream's `add_metadata.sh` script
- Do NOT include size estimates (e.g., "350+ TB") - these change frequently
- For dandi-cli, describe as "CLI and Python API" (not just CLI)

- [ ] Review other dataset records under `sourcedata/open-data-registry/datasets/`
  for inspiration, especially similar archives like `openneuro.yaml`, and improve
  the dandiarchive description accordingly
- [ ] Provide basic description of bucket organization:
  - `dandisets/` - where to find manifests per version of each dandiset, how to
    determine which keys under `blobs/` or `zarrs/` to access for actual data
  - Point to https://github.com/dandi/schema/ for serializations of schemas used
    in those manifests
- [ ] Add `Tutorials` section under `DataAtWork`:
  - Reference tutorials from dandi-docs (https://docs.dandiarchive.org/example-notebooks/dandi/DANDI%20User%20Guide%2C%20Part%20II/ and there on)
  - Link to example notebooks (https://dandi.github.io/example-notebooks/)
- [ ] Add `Publications` section under `DataAtWork`:
  - DANDI-related publications
- [ ] Review and add `Tools & Applications` from DANDI archive's integrated external services:
  - See https://github.com/dandi/dandi-archive/blob/master/web/src/utils/externalServices.ts
    (EXTERNAL_SERVICES constant)
  - Include: Neurosift, NWBExplorer, Neuroglancer, NeuroGlass, ITK/VTK Viewer, etc.
- [ ] Consider adding:
  - NGFF/Zarr access tutorial
  - Streaming NWB data examples
  - Analytics use cases (reference docs.dandiarchive.org)

#### Step 2: Create `code/generate_readme.py`

Python script to generate `root/README.md` from `sourcedata/open-data-registry/datasets/dandiarchive.yaml`:

- Parse the YAML file following the schema in `sourcedata/open-data-registry/schema.yaml`
- Extract and format:
  - Name → H1 title
  - Description → Introduction paragraph
  - Documentation, Contact, ManagedBy → Web resources section
  - Tags → Keywords section
  - Resources → S3 bucket details
  - DataAtWork → Tools & Applications section
- Enrich with content from `sourcedata/dandi-docs/` (introduction.md, etc.)
- Preserve structure matching current `root/README.md` format

#### Step 3: Create `code/generate_html.py`

Convert `root/README.md` to `root/index.html`:

- Use pandoc (via subprocess) for markdown to HTML conversion
- Add DANDI logo header (from current index.html)
- Apply minimal styling (matching current index.html)
- Keep it simple HTML (no external dependencies for S3 hosting)

#### Step 4: Create repository README.md

Document the purpose of this repository:
- What it does (sync bucket README with open-data-registry)
- How to use (make targets)
- Dependencies (aws-cli, python, pyyaml, pandoc)
- Workflow for making changes
- **Workflow for proposing changes to dandiarchive.yaml**:
  1. Make changes in local fork (`sourcedata/open-data-registry/`)
  2. Test locally (validate YAML, regenerate README/HTML, review)
  3. Commit changes to `dandi/open-data-registry` fork
  4. Submit PR to upstream `awslabs/open-data-registry` with proposed changes
  5. Once merged upstream, update submodule reference in this repo

#### Step 5: Create `code/sync_bucket.sh`

Script for bidirectional S3 sync with:
- `from_bucket`: Pull content from s3://dandiarchive/ to root/
- `to_bucket`: Push root/ content to s3://dandiarchive/
  - Relies on `aws` CLI being already configured with proper credentials
  - **Critical**: Must only upload files that exist locally in root/, never delete
    or modify other bucket contents
- **Note**: Cannot use `aws s3 sync --exclude "*/*"` because client-side filtering
  still requires listing the entire bucket (too large/slow). Instead:
  - Use `aws s3 ls s3://dandiarchive/ --no-sign-request` to list only top-level objects
  - Use `aws s3 cp` for each file individually
- Add `--dry-run` option that passes through to underlying `aws` command to preview changes

#### Step 6: Extend `Makefile`

```makefile
.PHONY: all from_bucket to_bucket generate readme html validate clean

all: generate

# Sync operations
from_bucket:
	./code/sync_bucket.sh from

to_bucket:
	./code/sync_bucket.sh to

# Generation pipeline
generate: readme html

readme:
	python code/generate_readme.py

html:
	python code/generate_html.py

# Validate dandiarchive.yaml against schema
validate:
	python code/validate_yaml.py

# Development helpers
clean:
	@echo "Nothing to clean"
```

### TODOs for Future Work

- [ ] **CI/CD integration**: GitHub Action to automatically:
  - Validate dandiarchive.yaml changes
  - Regenerate README.md and index.html
  - Create PR to upstream open-data-registry when local changes pass

- [ ] **Bucket sync automation**: Consider GitHub Action to:
  - Detect changes in root/
  - Sync to S3 bucket (requires AWS credentials setup)

- [ ] **Content enrichment**: Pull additional metadata from:
  - DANDI API (dataset counts, total size, etc.)
  - Generate dynamic statistics section

- [ ] **Validation wrapper**: Create `code/validate_yaml.sh` or Makefile target:
  - Wrapper around `pykwalify` validation (as done in open-data-registry)
  - Run from repo root for convenience
  - Could also add pre-commit hook

### Dependencies

For `code/` scripts:
- Python 3.11+
- `pyyaml` - YAML parsing
- `pykwalify` - YAML schema validation (used by open-data-registry)
- AWS CLI - S3 sync operations
- `pandoc` - Markdown to HTML conversion (system dependency)

Use `pyproject.toml` as single source of truth for Python dependencies.
Use `uv` for environment management (`uv venv`, `uv pip install`, `uv run`).
