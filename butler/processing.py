import os
import lsst.daf.persistence as dafPersist

#drp_path = os.getenv('DRPPATH')
drp_path = "/sps/lsst/data/clusters/workflow/weeklies/work/201749000/output"
butler = dafPersist.Butler(drp_path)
repoData = butler._repos.inputs()[0]  # output
mapper = repoData.repo.mappers()[0]   
root = repoData.cfgRoot               # output path (drp_path)
parentRepoData = repoData.getParentRepoDatas()[0]  # input
input_root = parentRepoData.cfgRoot                # input path -> ../input in this case

# list of keys for a given catalog
catalog = 'raw'
keys = butler.getKeys(catalog)

# all metadata for this catalog
metadata = butler.queryMetadata(catalog, format=sorted(keys.keys()))

# all available data ids
dataids = [dict(zip(sorted(keys.keys()), list(v) if not isinstance(v, list) else v)) for v in metadata]

# list of filters
filters = set([dataid['filter'] for dataid in dataids])

# all available vists
visits = {filt: list(set([dataid['visit']
                          for dataid in dataids if dataid['filter'] == filt]))
          for filt in filters}

# info on visits
for filt in visits:
    print(filt, len(visits[filt]))
    print("The total number of visits is", sum([len(visits[filt]) for filt in visits]))

# skymap
skymap = butler.get("deepCoadd_skyMap")
skymmap_config = skymap.config.toDict()
numtracts = skymap._numTracts
skymap_class = skymap.__class__
tract = skymap[0]

# how do I get the full list of avalaible dataType (raw, deepCoadd, etc)?
# how do I get the full list of data ID for a coadd in which we actually have data?