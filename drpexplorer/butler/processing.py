import os
import re
import glob
import lsst.daf.persistence as dafPersist


DRPPATH = os.getenv('DRPPATH')


class Butler(object):
    
    def __init__(self, drp_path=None):
        
        # Make sure we have data to load
        if drp_path is None and DRPPATH is None:
            raise IOError("You must give a path a DRP output directory.)

        # Load the bulter
        self.drp_path = drp_path if drp_path is not None else DRPPATH
        self.butler = dafPersist.Butler(self.drp_path)
        self.mapper = self.butler._getDefaultMapper()
        self.repoData = self.butler._repos.outputs()[0]
        
        # Load some basic info on the current DRP
        self.repo_input = self._get_repo("input")
        self.repo_output = self._get_repo("output")

        # Load some dataids
        self.datasetTypes = self._get_datasetTypes()
        self.dataIds = {'raw': self.get_dataIds('raw'),
                        'deepCoadd_meas': self.get_dataIds('deepCoadd_meas'),
                        'deepCoadd_forced_src': self.get_dataIds('deepCoadd_forced_src')
                       }
                     
        # Load filter and visits
        self.filters = self.get_filter_list()
        self.visits = self.get_visit_list()
        
        # Skymap
        self.skymap = self.butler.get("deepCoadd_skyMap")
        self.skymap_name = self.skymap.__class__.__name__
        self.skymap_doc = self.skymap.__doc__
        self.skymap_config = self.skymap.config.toDict()
        self.skymap_numtracts = self.skymap._numTracts
        self.skymap_numpatches = self.skymap[0].getNumPatches()
        
        # Mapper info
        self.mapper_name = self.mapper.__name__
        self.mapper_package = self.mapper.packageName 
        self.mapper_camera = self.mapper.getCameraName()
        

        # Packages
        self.packages = self.butler.get('packages')
        
        # Other
        self.configs = self._load_configs()
        self.schemas = self._load_schemas()
            
    def _get_repo(self, repo):
        """Get the full path of the input/output repository."""
        if repo == 'output':
            return self.repoData.cfgRoot               # output path (drp_path)
        elif repo == 'input':
            parentRepoData = self.repoData.getParentRepoDatas()[0]  # input
            return os.path.realpath(parentRepoData.cfgRoot)                # input path -> ../input in this case
        else:
            raise IOError("Wrong repo name. You should not be calling this internal method anyway.")
            
    def _get_datasetTypes(self):
        return sorted(self.repoData.repo._mapper.mappings.keys())
    
#    def _get_visit_datasetTypes(self):
#        vds = []
#        for dataset in but.datasetTypes:
#        try:
#            if but.butler.datasetExists(dataset, dataId=but.dataIds['raw'][0]):
#                vds.append(dataset)
#        except:
#            continue

    def get_catIdKeys(self, datasetType):
        """Get the list of ID keys for a given catalog."""
        if datasetType not in self.datasetTypes:
            raise IOError("%s is not a valid datasetType. Check self.datasetTypes to get the valid list." % datasetType) 
        return self.butler.getKeys(datasetType)
    
    def get_dataIds(self, datasetType):
        """Get all available data id for a given dataType."""
        keys = self.get_catIdKeys(datasetType)
        try:
            metadata = self.butler.queryMetadata(datasetType, format=sorted(keys.keys()))
        except:
            metadata = None
        if metadata is not None:
            return [dict(zip(sorted(keys.keys()), list(v) if not isinstance(v, list) else v)) for v in metadata]
        else:
            if datasetType not in self.repoData.repo._mapper.datasets:
                raise Error("This datasetType is not mappable")
            template = self.repoData.repo._mapper.datasets[datasetType]._template
            path = os.path.join(self.repoData.cfgRoot, os.path.dirname(template))
            basepath = "/".join([p for p in path.split('/') if not p.startswith('%')]) + "/"
            keys = [p[2:-2] for p in path.split('/') if p.startswith('%')]
            gpath = "/".join([p if not p.startswith('%') else '*' for p in path.split('/')])
            paths = [p for p in glob.glob(gpath) if 'merged' not in p]
            return [{k: v for k, v in zip(keys, p.split(basepath)[1].split('/'))} for p in paths]

    def get_filter_list(self):
        """Get the list of filters."""
        return set([dataid['filter'] for dataid in self.dataIds['raw']])
        
    def get_visit_list(self):
        """"All available vists."""
        visits = {filt: list(set([dataid['visit'] 
                                  for dataid in self.dataIds['raw'] if dataid['filter'] == filt]))
                  for filt in self.filters}
        return visits
    
    def _load_configs(self):
        """Load configs for the main tasks."""
        configs = self._load_generic_dataset("config")
        return {cfg: configs[cfg].toDict() for cfg in configs}
        
    def _load_schemas(self):
        """Load the schemas for all catalogs."""
        schemas = self._load_generic_dataset("schema")
        for schema in schemas:
            sch = schemas[schema].asAstropy()
            schemas[schema] = {col: {'description': sch[col].description, 
                                     'unit': sch[col].unit, 
                                     'dtype': sch[col].dtype} 
                               for col in sch.colnames}
        return schemas
        
    def _load_generic_dataset(self, datatype):
        """Load the schema or config datasets."""
        if datatype not in ['config', 'schema']:
            raise IOError("`datatype` must be either `config` or `schema`.")
        datatypes = {}
        for dataset in self.datasetTypes:
            if not dataset.endswith('_%s' % datatype):
                continue 
            for dataId in [{}, self.dataIds['raw'][0], self.dataIds['deepCoadd_meas'][0]]:
                try:
                    datatypes[dataset] = self.butler.get(dataset, dataId=dataId)
                    break
                except:
                    pass
        return datatypes
