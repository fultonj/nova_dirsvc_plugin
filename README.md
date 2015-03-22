# nova_dirsvc_plugin

## I. Overview

This plugin implements Nova Hooks to populate a database external to
OpenStack (e.g. an LDAP directory server) with data about a launched 
instance. It also cleans up data in the same external database about
that instance when the instance is terminated. An example of this
plugin using Red Hat's Directory Server may also be provided later 
(time permitting). 

This plugin supports the following usecase: 

1. Boot an instance FOO
2. nova_dirsvc_plugin will collect a DICT from FOO
3. nova_dirsvc_plugin can then pass DICT to DIRSVC 
4. FOO fulfills its purpose 
5. FOO is shutdown
6. nova_dirsvc_plugin can then pass FOO's UUID to DIRSVC

In the usecase above DIRSVC can be an external RESTful service and 
the DICT will be sent via a simple HTTP Post. A more complicated 
example where DIRSVC is Red Hat's Directory Server may also be
provided in a future release. This plugin is based on from Lars
Kellogg-Stedman's demo_nova_hooks [1][2]. 

After this plugin is installed a log file containing the following 
two types of entries can be seen in nova_dirsvc_plugin.log within 
/var/log/nova containing the values of DICT on creation and deletion 
of an instance. 

```
'Registering instance with directory service at 2015-03-22 06:53:00.510936'
{   'image_uuid': u'035c2bc7-f2be-4607-afcf-c3b6237e9fe5',
    'instance_uuid': '2cb805cf-debe-43ae-a555-28a4a5d84694',
    'mac_address': u'fa:16:3e:56:50:29',
    'project_name': u'admin',
    'user_name': u'admin',
    'user_remote_address': '192.168.122.97'}
'Unregistering instance from directory service at 2015-03-22 06:53:45.064330'
{   'instance_uuid': '2cb805cf-debe-43ae-a555-28a4a5d84694'}
```

## II. Installation

Nova was packaged using Setuptools, which gives Nova the ability to
trigger plugins through entry points [3]. This plugin should also be
triggered by entry points. To get his plugin working on your OpenStack 
do the following (this was only tested on Red Hat Enterprise Linux
OpenStack Platform). 

1. Get the plugin
  ```
  git clone https://github.com/fultonj/nova_dirsvc_plugin.git
  ```

2. Build an egg file of the plugin
   ```
   cd nova_dirsvc_plugin/
   python setup.py bdist_egg 
   ```
   You should then have a file like dist/nova_dirsvc_plugin-1-py2.7.egg

3. Install the plugin

   Install the egg file in /usr/lib/python2.7/site-packages
   ```
   sudo python setup.py install --verbose 
   ```
   Restart the relevant Nova service so that it can load the new plugin. 
   ```
   sudo service openstack-nova-api restart
   sudo service openstack-nova-compute restart
   ```

4. Test the Package

   Start an instance and then verify that you can see a file like: 
   ```
   /var/log/nova/nova_dirsvc_plugin.log
   ```

Footnotes

1. http://blog.oddbit.com/2014/09/27/integrating-custom-code-with-n/ 
2. https://github.com/larsks/demo_nova_hooks
3. https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins
