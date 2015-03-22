#!/usr/bin/env python
# Filename:                hooks.py
# Description:             Sends instance info the dir svc
# Supported Langauge(s):   Python 2.7.x
# Time-stamp:              <2015-03-22 11:16:37 jfulton> 
# -------------------------------------------------------
# Uses nova hook example from Lars Kellogg-Stedman: 
#   http://blog.oddbit.com/2014/09/27/integrating-custom-code-with-n
# To extract desired information from passed arguments
# and save them to a logfile. This code could be modified
# to send the data to a real directory service instead of
# just logging. 
# -------------------------------------------------------
# Disclaimer: I work for Red Hat but this is not official
# Red Hat code. Take it or leave it. No support is guaranteed.
# Author: John Fulton <https://github.com/fultonj> 
# -------------------------------------------------------

class SaveToDirSvc(object): 
    logfile = '/var/log/nova/nova_dirsvc_plugin.log'

    def pre(self, *args, **kwargs):
        pass
    
    def post(self, *args, **kwargs):
        from datetime import datetime
        from pprint import pprint
        with open(self.logfile, 'a') as fd:
            pprint('Registering instance with directory service at ' + str(datetime.now()), fd)
            try:
                # Object from /usr/lib/python2.7/site-packages/nova/objects/instance.py 
                instance = args[0][0][0] # nova.objects.instance.Instance object (un-tupled)
                instance_uuid = instance['uuid'] # without this we can't get mac_address from neutron
            except TypeError:
                instance_uuid = ''
                pprint("Not able to un-tuple nova.objects.instance.Instance object", fd)
            # Object from /usr/lib/python2.7/site-packages/nova/compute/api.py
            api = args[1]      # nova.compute.api.API object
            # Object from /usr/lib/python2.7/site-packages/nova/openstack/common/context.py
            context = args[2]  # nova.context.RequestContext object
            context_dict = context.to_dict()
            auth_token = context_dict['auth_token'] # we could reuse this token
            user_name  = context_dict['user_name']  # who is using this service?
            remote_address = context_dict['remote_address'] # what is his/her IP?
            project_name = context_dict['project_name'] # what project is it under?
            flavor = args[3]     # dictionary containing information about the selected flavor
            image_uuid = args[4] # what image did the user boot? 
            try:
                mac_address = '' # assume we do not have it, and then populate it
                import time
                i = 1 
                while len(mac_address) == 0 and len(instance_uuid) > 0: 
                    time.sleep(0.5)  # give port time to get ready
                    # api contains a 'network_api': <nova.network.neutronv2.api.API object
                    ports = api.network_api.list_ports(context)
                    for j in range(0, len(ports['ports'])):
                        port = ports['ports'][j]
                        if port['device_id'] == instance_uuid:
                            mac_address = port['mac_address']
                    # pprint("Waiting for MAC address %i time(s)" % (i), fd)
                    i = i+1
                    if i > 60: # cannot wait forever
                        break
                # information to save
                payload = {
                    'instance_uuid':instance_uuid,
                    'mac_address':mac_address, 
                    'project_name':project_name,
                    'image_uuid':image_uuid,
                    'user_name':user_name,
                    'user_remote_address':remote_address,
                    }
                pprint(payload, fd, indent=4)
                # HERE ^^^^^
                # So rather than just log the payload, you could post it to
                # a web service OR you could connect to an LDAP directory 
                # server and create an entry for it. 
            except: 
                import traceback
                pprint(traceback.format_exc(), fd)

class DeleteFromDirSvc(object):
    logfile = '/var/log/nova/nova_dirsvc_plugin.log'

    def pre(self, *args, **kwargs):
        # Log instance UUID for symmetric delete operation
        from datetime import datetime
        from pprint import pprint
        with open(self.logfile, 'a') as fd:
            pprint('Unregistering instance from directory service at ' + str(datetime.now()), fd)
            try:
                instance_uuid = args[2]['uuid']
            except TypeError:
                instance_uuid = ''
                pprint("Not able to un-tuple nova.objects.instance.Instance object", fd)
            payload = {
                'instance_uuid':instance_uuid,
                }
            pprint(payload, fd, indent=4)

    def post(self, *args, **kwargs):
        pass
