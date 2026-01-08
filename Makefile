.PHONY: all from_bucket to_bucket generate readme html validate clean

# Default: generate README and HTML from YAML
all: generate

# Sync operations
from_bucket:
	./code/sync_bucket.sh from $(if $(DRY_RUN),--dry-run)

to_bucket:
	./code/sync_bucket.sh to $(if $(DRY_RUN),--dry-run)

# Generation pipeline
generate: readme html

readme:
	uvx --with pyyaml python code/generate_readme.py

html:
	uvx --with pypandoc-binary python code/generate_html.py

# Validate dandiarchive.yaml against schema
validate:
	cd sourcedata/open-data-registry && \
	uvx pykwalify -d datasets/dandiarchive.yaml -s schema.yaml

# Development helpers
clean:
	@echo "Nothing to clean"
