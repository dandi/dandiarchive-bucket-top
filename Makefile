all:
	@echo "nothing to be done by default ATM"

from_bucket:
	mkdir -p root/
	aws s3 sync s3://dandiarchive/ root/ --no-sign-request --exclude "*/*"
