The goal in this repository to sync two way (starting from bucket to local) the top folder content (files like README.md) of 

- the dandiarchive S3 bucket,
  - and in particular its README.md and produced from it index.html
- the description for dandiarchive bucket within https://github.com/awslabs/open-data-registry/blob/HEAD/datasets/dandiarchive.yaml 

We need to design a solution to facilitate keeping them in sync as to
modify within git repo, and trigger updates on the bucket.

Preliminary idea is that the source of truth for README.md would be within the https://github.com/awslabs/open-data-registry/blob/HEAD/datasets/dandiarchive.yaml .
We will keep that https://github.com/awslabs/open-data-registry/ git repo as subdataset under sourcedata/open-data-registry with a fork on our DANDI archive (https://github.com/dandi/open-data-registry) -- that is already done.
The schema for that yaml is thus readily available under sourcedata/open-data-registry/schema.yaml .

Then we would sync bucket to/from `top_content/` folder.
`code/` folder should provide script to 'sync' (using e.g. aws CLI), and README.md on top level of this repo should describe the purpose of this repository.

`Makefile` on top of this repo should have invocations for syncing to centralize potential actions to be taken.

Within this work we should plan to extend already existing
sourcedata/open-data-registry/datasets/dandiarchive.yaml with information
present in root/README.md and sourcedata/dandi-docs (rendered is at
https://docs.dandiarchive.org/) while following that sourcedata/open-data-registry/schema.yaml and establish TODO on what other metadata to provide there.

We know that it would be great to point to specific usecases of use of data
from the bucket, could be e.g. navigating Zarr(s) and or doing analytics, but
likely just to refer to docs oneline.

