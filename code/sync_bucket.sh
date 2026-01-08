#!/bin/bash
# Sync top-level files between S3 bucket and local root/ directory.
#
# Usage:
#   ./sync_bucket.sh from [--dry-run]    # Download from bucket to root/
#   ./sync_bucket.sh to [--dry-run]      # Upload from root/ to bucket
#
# Note: Cannot use `aws s3 sync --exclude "*/*"` because client-side filtering
# still requires listing the entire bucket (too large/slow). Instead, we list
# only top-level objects and copy files individually.

set -eu

BUCKET="s3://dandiarchive"
LOCAL_DIR="root"

# Parse arguments
DIRECTION="${1:-}"
DRY_RUN=""

shift || true
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN="--dryrun"
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
    shift
done

if [[ -z "$DIRECTION" ]]; then
    echo "Usage: $0 {from|to} [--dry-run]" >&2
    echo "" >&2
    echo "Commands:" >&2
    echo "  from    Download top-level files from bucket to $LOCAL_DIR/" >&2
    echo "  to      Upload files from $LOCAL_DIR/ to bucket" >&2
    echo "" >&2
    echo "Options:" >&2
    echo "  --dry-run    Show what would be done without making changes" >&2
    exit 1
fi

# Ensure local directory exists
mkdir -p "$LOCAL_DIR"

case "$DIRECTION" in
    from)
        echo "Syncing from $BUCKET to $LOCAL_DIR/"
        [[ -n "$DRY_RUN" ]] && echo "(dry-run mode)"
        echo ""

        # List only top-level objects (files, not directories)
        # Using --no-sign-request for public bucket access
        aws s3 ls "$BUCKET/" --no-sign-request | while read -r line; do
            # Parse the ls output: "2024-01-15 10:30:00     12345 filename"
            # Skip directories (lines ending with /)
            if [[ "$line" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}[[:space:]]+[0-9]{2}:[0-9]{2}:[0-9]{2}[[:space:]]+[0-9]+[[:space:]]+(.+)$ ]]; then
                filename="${BASH_REMATCH[1]}"
                # Skip if it's a directory (shouldn't happen but be safe)
                if [[ "$filename" != */ ]]; then
                    echo "Downloading: $filename"
                    if [[ -z "$DRY_RUN" ]]; then
                        aws s3 cp "$BUCKET/$filename" "$LOCAL_DIR/$filename" --no-sign-request
                    fi
                fi
            fi
        done
        echo ""
        echo "Done."
        ;;

    to)
        echo "Syncing from $LOCAL_DIR/ to $BUCKET"
        [[ -n "$DRY_RUN" ]] && echo "(dry-run mode)"
        echo ""

        # Upload only files that exist in root/
        # This NEVER deletes or modifies files that don't exist locally
        for filepath in "$LOCAL_DIR"/*; do
            if [[ -f "$filepath" ]]; then
                filename=$(basename "$filepath")
                echo "Uploading: $filename"
                if [[ -z "$DRY_RUN" ]]; then
                    aws s3 cp "$filepath" "$BUCKET/$filename" $DRY_RUN
                fi
            fi
        done
        echo ""
        echo "Done."
        ;;

    *)
        echo "Unknown direction: $DIRECTION" >&2
        echo "Use 'from' or 'to'" >&2
        exit 1
        ;;
esac
