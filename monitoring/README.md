cloud-scheduler-stats monitoring
================================

The cloud-scheduler-stats daemon can be used to monitor the heath and status
of cloud scheduler using the cloud-scheduler xmlrpc interface. This deamon 
will publish data about jobs and running VMs to [Librato Metrics][1] (more types
of publishing may be supported later).

Installation
------------

Using pip:

    pip install cloud-scheduler-stats


Using git:

    git clone https://github.com/hep-gc/cloud-scheduler.git
    cd cloud-scheduler/monitoring
    python setup.py install

Configuration
-------------

cloud-scheduler-stats must be configured to use your Librato Metrics account
and be pointed at the cloud-scheduler instance you wish to monitor. Edit the
configuration file.

    vim /etc/cloudscheduler/cloud_stats.conf

You MUST replace the values for `librato_user` and `librato_token` (look at the 
examples). You also need to replace `info_server_hostname` with the hostname
of your cloud scheduler instance. 

It order for the cloud-scheduler-stats to talk to the xmlrpc interface of 
cloud-scheduler the xmlrpc port must be open on you cloud-scheduler instance 
(default port 8111)


[1]: https://metrics.librato.com