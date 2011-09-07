# -*- coding: utf-8 -*-

""" Monitor the status of virtual machines. """

from baseplugin import BasePlugin
from basejob import BaseJob
from importer import Importer, ImporterError

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
        except ImporterError, exc:
            raise Job.BaseError('Importer error, please check local logs')

    def get_status(self):
        """ Get the status of all defined VMs. """

        imp = Importer()
        imp['distant_url'] = 'https://%s/exporter/' % self.infos['object']['address']
        if 'importer_tcp_timeout' in self.params:
            imp['timeout'] = self.params['importer_tcp_timeout']

        try:
            status = imp.call('virtmanager.services', 'get_status')
            offline_vms = sum([vm for vm in status if vm[status] == 'offline'])

            if offline_vms > 0:
                return 'ERROR', '%s over %s VMs currently offline' % (offline_vms, len(status))
            else:
                return 'FINISHED', 'All VMs currently online'
        except ImporterError, exc:
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

        @see BasePlugin documentation
        """
        BasePlugin.__init__(self, options, event, url, params)

    def create_new_job(self, job):
        """ Create a new virtmonitor job. """
        return Job(self.options, job, self.params)

