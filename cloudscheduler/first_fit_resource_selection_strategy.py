from resource_selection_strategy import IResourceSelectionStrategy

log = None

class ResourceSelectionStrategy(IResourceSelectionStrategy):

    def __init__(self):
        global log
        log = logging.getLogger("cloudscheduler")

    def get_name(self):
        return "first fit"

    # Return the first resource that fits the passed in VM requirements. Does
    # not remove the element returned.
    # Built to support "First-fit" scheduling.
    # Parameters:
    #    network  - the network assoication required by the VM
    #    cpuarch  - the cpu architecture that the VM must run on
    #    memory   - the amount of memory (RAM) the VM requires
    #    cpucores  - the number of cores that a VM requires (dedicated? or general?)
    #    storage   - the amount of scratch space the VM requires
    # Return: returns a Cluster object if one is found that fits VM requirments
    #         Otherwise, returns the 'None' object
    def get_resourceFF(self, resource_pool, network, cpuarch, memory, cpucores, storage):
        if len(resource_pool.resources) == 0:
            log.debug("Pool is empty... Cannot return FF resource")
            return None,None

        for cluster in resource_pool.resources:
            # If the cluster has no open VM slots
            if (cluster.vm_slots <= 0):
                continue
            # If the cluster does not have the required CPU architecture
            if not (cpuarch in cluster.cpu_archs):
                continue
            # If required network is NOT in cluster's network associations
            if not (network in cluster.network_pools):
                continue
            # If the cluster has no sufficient memory entries for the VM
            if (cluster.find_mementry(memory) < 0):
                continue
            # If the cluster does not have sufficient CPU cores
            if (cpucores > cluster.cpu_cores):
                continue
            # If the cluster does not have sufficient storage capacity
            if (storage > cluster.storageGB):
                continue

            # Return the cluster as an available resource (meets all job reqs)
            return cluster,None

        # If no clusters are found (no clusters can host the required VM)
        return None,None
