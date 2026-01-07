# DANDI: Distributed Archives for Neurophysiology Data Integration

DANDI is a public archive of neurophysiology datasets, including raw and
processed data, and associated software containers. Datasets are shared according
to a Creative Commons CC0 or CC-BY licenses. This US BRAIN Initiative supported
data archive publishes and shares neurophysiology data including electrophysiology,
optophysiology, and behavioral time-series, and images from immunostaining
experiments.

The data uses a set of community standards:
- NWB: Neurodata Without Borders
- BIDS: Brain Imaging Data Structure
- NIDM: Neuro Imaging Data Model
- NGFF: Next Generation File Format

Development of DANDI is supported by the National Institute of Mental Health.

## Dandisets

We define a DANDI dataset as a Dandiset. A Dandiset is an organized collection of
assets (files) with both file level and dataset level metadata generated from an
experiment or a project.

### Web resources

- Web interface: https://dandiarchive.org/
- API: https://api.dandiarchive.org/swagger/
- Handbook: https://handbook.dandiarchive.org
- Helpdesk: https://github.com/dandi/helpdesk/issues/new/choose
- Github: https://github.com/dandi
- S3 Location: s3://dandiarchive/
- DANDI Hub (a Jupyterhub instance): https://hub.dandiarchive.org/ (Requires registration via the Web interface)

### Organization of the S3 bucket

- **blobs** - This key store houses the actual binary data indexed by unique keys. This
  is done to provide deduplication when publishing new datasets containing existing
  data.
- **dandisets** - Information about each Dandiset including metadata, a manifest of
  all assets contained in a Dandiset, and asset metadata. This information should
  allow anyone to access all the data relevant to a Dandiset

Other prefixes in the bucket can be ignored. For example:

- _dandiarchive_ - This folder stores an inventory listing of all items in the bucket.
  This is generated automatically by the S3 Inventory service.

#### Keywords:

- biology
- cell imaging
- electrophysiology
- infrastructure
- life sciences
- neuroimaging
- neurophysiology
- neuroscience
