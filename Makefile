all:
	@echo "nothing to be done by default ATM"

from_bucket:
	mkdir -p root/
	aws s3 ls --no-sign-request s3://dandiarchive/ | awk '{print $$NF}' | grep -v '/$$' \
		| xargs -I{} aws s3 cp s3://dandiarchive/{} root/ --no-sign-request
