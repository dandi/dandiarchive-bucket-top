# DANDI: Distributed Archives for Neurophysiology Data Integration

DANDI is a public archive of neurophysiology datasets, including raw and
processed data, and associated software containers. Datasets are shared
according to Creative Commons CC0 or CC-BY licenses. This US BRAIN Initiative
supported archive provides a broad range of cellular neurophysiology data
including intracellular and extracellular electrophysiology, optophysiology,
calcium imaging, fiber photometry, behavioral time-series, and images from
immunostaining experiments, from over 20 species.

The data uses a set of community standards:
- NWB: Neurodata Without Borders
- BIDS: Brain Imaging Data Structure
- NGFF: Next Generation File Format
- NIDM: Neuro Imaging Data Model

Development of DANDI is supported by the National Institute of Mental Health.

## Dandisets

We define a DANDI dataset as a Dandiset. A Dandiset is an organized collection
of assets (files) with both file level and dataset level metadata generated from
an experiment or a project.

### Web resources

- Web interface: https://dandiarchive.org
- API: https://api.dandiarchive.org/swagger/
- Handbook: https://handbook.dandiarchive.org
- Helpdesk: https://github.com/dandi/helpdesk/issues/new/choose
- Github: https://github.com/dandi
- S3 Location: s3://dandiarchive/
- DANDI Hub (a JupyterHub instance): https://hub.dandiarchive.org/ (Requires
  registration via the Web interface)

### Organization of the S3 bucket

- **dandisets** - Metadata and manifests for each Dandiset version; manifests
  reference keys under blobs/ or zarrs/ for actual data. See DANDI schema for
  manifest format specifications.
- **blobs** - Deduplicated binary data (NWB files) indexed by content hash.
- **zarrs** - Zarr arrays for large imaging datasets.

Other prefixes in the bucket can be ignored. For example:

- _dandiarchive_ - This folder stores an inventory listing of all items in the
  bucket. This is generated automatically by the S3 Inventory service.

### Tools & Applications

- [DANDI Web Interface](https://dandiarchive.org/) - DANDI Project
- [DANDI CLI and Python API](https://github.com/dandi/dandi-cli) - DANDI Project
- [DANDI JupyterHub](https://hub.dandiarchive.org/) - DANDI Project
- [DANDI API](https://api.dandiarchive.org/swagger/) - DANDI Project
- [Neurosift - Interactive NWB Viewer](https://neurosift.app/) - Flatiron Institute
- [NWB Explorer](https://nwbexplorer.opensourcebrain.org/) - MetaCell
- [Neuroglancer](https://github.com/google/neuroglancer) - Google
- [ITK/VTK Viewer for OME-Zarr](https://kitware.github.io/itk-vtk-viewer/) - Kitware

### Tutorials

- [DANDI User Guide - Downloading and Using Data](https://docs.dandiarchive.org/user-guide-using/using/) - DANDI Project
- [DANDI Example Notebooks](https://dandi.github.io/example-notebooks/) - DANDI Project

### Publications

- [Neurosift: DANDI exploration and NWB visualization in the browser](https://joss.theoj.org/papers/10.21105/joss.06590) - Magland J, Soules J, Baker C, Dichter B
- [Facilitating analysis of open neurophysiology data on the DANDI Archive using large language model tools](https://www.nature.com/articles/s41597-025-06285-x) - Magland JF, Ly R, Rübel O, Dichter B
- [A comparison of neuroelectrophysiology databases](https://www.nature.com/articles/s41597-023-02614-0) - Subash P, Gray A, Bhattacharyya B, et al.

#### Keywords:

- biology
- calcium imaging
- cell imaging
- electrophysiology
- hdf5
- life sciences
- neuroimaging
- neurophysiology
- neuroscience
- zarr
