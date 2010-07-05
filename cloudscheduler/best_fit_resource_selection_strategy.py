import logging
from resource_selection_strategy import IResourceSelectionStrategy

log = None
class ResourceSelectionStrategy(IResourceSelectionStrategy):

    def __init__(self):
        global log
        log = logging.getLogger("cloudscheduler")

    def get_name(self):
        return "best fit"

    # Returns a resource that fits given requirements and fits some balance
    # criteria between clusters (for example, lowest current load or most free
    # resources of the fitting clusters).
    # Returns the first find as the primary balanced cluster choice, and returns
    # a secondary fitting cluster if available (otherwise, None is returned in
    # place of a secondary cluster).
    # Built to support "Cluster-Balanced Fit Scheduling"
    # Note: Currently, we are considering the "most balanced" cluster to be that
    # with the fewest running VMs on it. This is to minimize and balance network
    # traffic to clusters, among other reasons.
    # Other possible metrics are:
    #   - Most amount of free space for VMs (vm slots, memory, cpu cores..);
    #   - etc.
    # Parameters:
    #    resource_pool - the resource pool
    #    network  - the network assoication required by the VM
    #    cpuarch  - the cpu architecture that the VM must run on
    #    memory   - the amount of memory (RAM) the VM requires
    #    cpucores  - the number of cores that a VM requires (dedicated? or general?)
    #    storage   - the amount of scratch space the VM requires
    # Return: returns a tuple of cluster objects. The first, or primary cluster, is the
    #         most balanced fit. The second, or secondary, is an alternative fitting
    #         cluster.
    #         Normal return, (Primary_Cluster, Secondary_Cluster)
    #         If no secondary cluster is found, (Cluster, None) is returned.
    #         If no fitting clusters are found, (None, None) is returned.
    def get_resource(self, resource_pool, network, cpuarch, memory, cpucores, storage):

        # Get a list of fitting clusters
        fitting_clusters = resource_pool.get_fitting_resources(network, cpuarch, memory, cpucores, storage)

        # If list is empty (no resources fit), return None
        if len(fitting_clusters) == 0:
            log.debug("No clusters fit requirements. Fitting resources list is empty.")
            return (None, None)

        # If the list has only 1 item, return immediately
        if len(fitting_clusters) == 1:
            log.debug("Only one cluster fits parameters. Returning that cluster.")
            return (fitting_clusters[0], None)

        # Set the most-balanced and next-most-balanced initial values
        # Note: mostbal_cluster stands for "most balanced cluster"
        # Note: nextbal_cluster stands for "next most balanced cluster"
        cluster1 = fitting_clusters.pop()
        cluster2 = fitting_clusters.pop()

        if (cluster1.num_vms() < cluster2.num_vms()):
            mostbal_cluster = cluster1
            nextbal_cluster = cluster2
        else:
            mostbal_cluster = cluster2
            nextbal_cluster = cluster1

        mostbal_vms = mostbal_cluster.num_vms()
        nextbal_vms = nextbal_cluster.num_vms()

        # Iterate through fitting clusters to check for most and next balanced clusters. (LINEAR search)
        for cluster in fitting_clusters:
            # If considered cluster has fewer running VMs, set it as the most balanced cluster
            if (cluster.num_vms() < mostbal_vms):
                mostbal_cluster = cluster
                mostbal_vms = cluster.num_vms()
            elif (cluster.num_vms() < nextbal_vms):
                nextbal_cluster = cluster
                nextbal_vms = cluster.num_vms()

        # Return the most balanced cluster after considering all fitting clusters.
        return (mostbal_cluster, nextbal_cluster)
