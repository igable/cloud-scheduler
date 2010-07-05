import logging
import os
import imp

log = None

class ResourceSelector:
    resource_selection_strategy = None

    def __init__(self, config ):
        global log
        log = logging.getLogger("cloudscheduler")
        self.config = config
        log.debug("Resource selector instantiated.")

    # This is the method that clients will call to get the selected resources.
    def get_resource(self, resource_pool, network, cpuarch, memory, cpucores, storage):
        log.debug("In get_resource()")
        if(self.resource_selection_strategy == None):
            self.init_strategy()
        return self.resource_selection_strategy.get_resource(resource_pool, network, cpuarch, memory, cpucores, storage)

    def init_strategy(self, ):
        log.debug("In init_strategy()")
        class_inst = None
        expected_class = 'ResourceSelectionStrategy'
        filepath = self.config.resource_selection_strategy
        log.info("Loading resource selection strategy from %s" % filepath)
        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

        if file_ext.lower() == '.py':
            log.debug("Loading source from .py file...")
            py_mod = imp.load_source(mod_name, filepath)

        elif file_ext.lower() == '.pyc':
            log.debug("Loading source from .pyc file...")
            py_mod = imp.load_compiled(mod_name, filepath)

        if expected_class in dir(py_mod):
            class_inst = py_mod.ResourceSelectionStrategy() 

        resource_selection_strategy = class_inst
        log.info("resource selection strategy loaded: %s" % (resource_selection_strategy.get_name(),))

        return
        
        
