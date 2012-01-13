# -*- coding: utf-8 -*-

""" Monitor the status of virtual machines. """

from baseplugin import BasePlugin
from basejob import BaseJob
from importer import Importer, ImporterError

import urllib2
import urlparse


class Job(BaseJob):
    """ Virtual machine monitoring job. """

    def __init__(self, options, infos, params):
        """ Init method for virtmonitor job."""
        BaseJob.__init__(self, options, infos, params)
        self.importer = Importer()
        self.server_address = self.infos['object']['address']
        self.importer['distant_url'] = 'https://%s/exporter/' % (self.server_address)
        if 'importer_tcp_timeout' in params:
            self.importer['timeout'] = params['importer_tcp_timeout']
        self.params = params

    # Checks below are supposed to be run locally

    def restart_vm(self):
        """ Restart VM if it is currently shutdown. """

        imp = Importer()
        imp['distant_url'] = 'https://localhost/exporter/'
        if 'importer_tcp_timeout' in self.params:
            imp['timeout'] = self.params['importer_tcp_timeout']

        try:
            ret = imp.call('virtmanager.services', 'get_status')
            if ret[self.infos['object']['address']] == 'offline':
                ret = imp.call('virtmanager.services', 'domain_start', self.infos['object']['address'])

            if ret:
                return 'FINISHED', 'VM online'
            else:
                return 'ERROR', 'VM offline'
        except ImporterError, _exc:
            raise Job.BaseError('Importer error, please check local logs')

    def get_service_status(self):
        """ Get the status of a VM and whether its services are up or not. """

        imp = Importer()
        imp['distant_url'] = 'https://localhost/exporter/'
        if 'importer_tcp_timeout' in self.params:
            imp['timeout'] = self.params['importer_tcp_timeout']

        try:
            ret = imp.call('virtmanager.services', 'get_status')
            if ret[self.infos['object']['address']] == 'offline':
                return 'ERROR', 'VM offline'

        except ImporterError, exc:
            raise Job.BaseError('Importer error, please check local logs')

        url = self.infos['object']['object_infos']['service-url']
        if urlparse.urlparse(url)[0] == 'http':
            req = urllib2.Request(url)
            try:
                urllib2.urlopen(req, None, self.params.get('importer_tcp_timeout', 60))
            except urllib2.HTTPError, exc:
                return 'ERROR', 'HTTP server returned code: %d' % exc.code
            except urllib2.URLError, exc:
                return 'ERROR', 'Failed to reach server: %s' % exc.reason
        else:
            return 'ERROR', 'Unknown URL scheme'

        return 'FINISHED', 'VM service URL is up'

    # Checks below are supposed to be run from central supervision

    def get_status(self):
        """ Get the status of all defined VMs. """

        imp = Importer()
        imp['distant_url'] = 'https://%s/exporter/' % self.infos['object']['address']
        if 'importer_tcp_timeout' in self.params:
            imp['timeout'] = self.params['importer_tcp_timeout']

        try:
            vms_status = imp.call('virtmanager.services', 'get_status')
            svc_status = imp.call('spv.services', 'get_status', {
                'plugin_name' : 'virtmonitor',
                'plugin_check': 'get_service_status',
            })

            offline_vms = sum([vm_name for vm_name, vm_status in vms_status.iteritems()
                if vm_status == 'offline'])
            offline_svc = sum([1 for _, svc in svc_status['status'].iteritems()
                if svc['check_status'] != 'FINISHED'])

            if offline_vms > 0 or offline_svc > 0:
                return 'ERROR', '%s of %s VMs currently offline plus %s of %s VMs services down' % (
                    offline_vms, len(vms_status),
                    offline_svc, len(svc_status['status']),
                )
            else:
                return 'FINISHED', 'All VMs and services currently online'
        except ImporterError, _exc:
            raise Job.BaseError('Importer error, please check remote end')


class Plugin(BasePlugin):
    """ Virtual machine monitoring plugin. """

    require = { }

    optional = {
        'importer_tcp_timeout' : int
       }

    name = "virtmonitor"

    def __init__(self, options, event, url=None, params=None):
        """ Init method of the virtmonitor plugin.

        @params is a dictionary of optional parameters among:
        importer_tcp_timeout: maximum wait time before reporting importer failure
                              also used for regular http requests

        @see BasePlugin documentation
        """
        BasePlugin.__init__(self, options, event, url, params)

    def create_new_job(self, job):
        """ Create a new virtmonitor job. """
        return Job(self.options, job, self.params)

