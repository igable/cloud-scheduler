#!/usr/bin/env python
# vim: set expandtab ts=4 sw=4:

# Copyright (C) 2009 University of Victoria
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

## Auth.: Patrick Armstrong

import os
import sys
from urlparse import urlparse
import ConfigParser


# Cloud Scheduler Options Module.

# Set default values
info_server_hostname = "localhost"
info_server_port = "8111"
librato_user = None
librato_token = None
librato_prefix = None
polling_interval = 60

log_level = "INFO"
log_location = None
log_stdout = False
log_max_size = None
log_format = "%(asctime)s - %(levelname)s - %(threadName)s - %(message)s"




def setup(path=None):
    """Setup cloudscheduler using config file.
       setup will look for a configuration file specified on the command line,
       or in ~/.cloudscheduler.conf or /etc/cloudscheduler.conf
    """

    global info_server_hostname
    global info_server_port
    global librato_user
    global librato_token
    global librato_prefix
    global polling_interval

    global log_level
    global log_location
    global log_stdout
    global log_max_size
    global log_format

    homedir = os.path.expanduser('~')

    # Find config file
    if not path:
        if os.path.exists(homedir + "/.cloudscheduler/cloud_stats.conf"):
            path = homedir + "/.cloudscheduler/cloud_stats.conf"
        elif os.path.exists("/etc/cloudscheduler/cloud_stats.conf"):
            path = "/etc/cloudscheduler/cloud_stats.conf"
        else:
            print >> sys.stderr, "Configuration file problem: There doesn't " \
                  "seem to be a configuration file. " \
                  "You can specify one with the --config-file parameter, " \
                  "or put one in ~/.cloudscheduler/cloud_scheduler.conf or "\
                  "/etc/cloudscheduler/cloud_stats.conf"
            sys.exit(1)

    # Read config file
    config_file = ConfigParser.ConfigParser()
    try:
        config_file.read(path)
    except IOError:
        print >> sys.stderr, "Configuration file problem: There was a " \
              "problem reading %s. Check that it is readable," \
              "and that it exists. " % path
        raise
    except ConfigParser.ParsingError:
        print >> sys.stderr, "Configuration file problem: Couldn't " \
              "parse your file. Check for spaces before or after variables."
        raise
    except:
        print "Configuration file problem: There is something wrong with " \
              "your config file."
        raise

    if config_file.has_option("global", "info_server_hostname"):
        info_server_hostname = config_file.get("global",
                                                "info_server_hostname")

    if config_file.has_option("global", "info_server_port"):
        try:
            info_server_port = config_file.getint("global", "info_server_port")
        except ValueError:
            print "Configuration file problem: info_server_port must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "librato_user"):
        librato_user = config_file.get("global",
                                                "librato_user")

    if config_file.has_option("global", "librato_token"):
        librato_token = config_file.get("global",
                                                "librato_token")

    if config_file.has_option("global", "librato_prefix"):
        librato_prefix = config_file.get("global",
                                                "librato_prefix")

    if config_file.has_option("global", "polling_interval"):
        try:
            polling_interval = config_file.getint("global", "polling_interval")
        except ValueError:
            print "Configuration file problem: polling_interval must be an " \
                  "integer value."
            sys.exit(1)


#    if config_file.has_option("global", ""):

#    if config_file.has_option("global", ""):
#        try:
#            vm_lifetime = config_file.getint("global", "vm_lifetime")
#        except ValueError:
#            print "Configuration file problem: vm_lifetime must be an " \
#                  "integer value."
#            sys.exit(1)


    # Default Logging options
    if config_file.has_option("logging", "log_level"):
        log_level = config_file.get("logging", "log_level")

    if config_file.has_option("logging", "log_location"):
        log_location = os.path.expanduser(config_file.get("logging", "log_location"))

    if config_file.has_option("logging", "log_stdout"):
        try:
            log_stdout = config_file.getboolean("logging", "log_stdout")
        except ValueError:
            print "Configuration file problem: log_stdout must be a" \
                  " Boolean value."

    if config_file.has_option("logging", "log_max_size"):
        try:
            log_max_size = config_file.getint("logging", "log_max_size")
        except ValueError:
            print "Configuration file problem: log_max_size must be an " \
                  "integer value in bytes."
            sys.exit(1)

    if config_file.has_option("logging", "log_format"):
        log_format = config_file.get("logging", "log_format", raw=True)


