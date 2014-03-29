# setup.py - standard distutils setup file for Cloud Scheduler Stats
import os
import os.path
import sys
try:
    from setuptools import setup
except:
    try:
        from distutils.core import setup
    except:
        print "Couldn't use either setuputils or distutils. Install one of those. :)"
        sys.exit(1)
import cloudschedulerstats.__version__ as version

if not os.geteuid() == 0:
    config_files_dir = os.path.expanduser("~/.cloudscheduler/")
    # note that you can't initd script as non root
    # but at least you can install the package
    initd_dir = config_files_dir
else:
    config_files_dir = "/etc/cloudscheduler/"
    initd_dir = "/etc/init.d/"
config_files = ["cloud_stats.conf"]

# check for preexisting config files
data_files = okay_files = []
for config_file in config_files:
    if not os.path.isfile(config_files_dir + os.path.basename(config_file)):
        okay_files.append(config_file)
if okay_files:
    data_files = [(config_files_dir, okay_files)]

# add init.d script
data_files.append((initd_dir,['scripts/cloud-scheduler-stats']))

setup(name = "cloud-scheduler-stats",
    version = version.version,
    license="'GPL3' or 'Apache 2'",
    install_requires=[
       "librato-metrics>=0.3.9"
        ],
    description = "A tool for publishing cloud scheduler metrics to librato",
    author = "Ian Gable",
    author_email = "igable@uvic.ca",
    url = "http://github.com/hep-gc/cloud-scheduler/monitoring",
    packages = ['cloudschedulerstats'],
    scripts = ["cloud-scheduler-stats"],
    data_files=data_files,
) 
