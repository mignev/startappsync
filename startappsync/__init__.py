import subprocess
import os
import logging

from re import search
from watchdog.events import FileSystemEventHandler
from gitconfig.core import GitConfig, GitRepoNotFoundError

version = "0.0.6"
version_info = (0, 0, 6)

def cmd(cmd):
    process = subprocess.Popen(cmd,
      shell=True,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
    )
    return process

def rsync(source, destination):
    _cmd = 'rsync -ahz --rsh="ssh" --exclude-from ".startappexclude" ' + source + ' ' + destination
    cmd(_cmd)

class App():
    def __init__(self, **kwargs):
        current_working_dir = os.getcwd()
        self.repo = kwargs.get('repo', current_working_dir)

        self._git_config = GitConfig(path=self.repo)

    def _git_config_get(self, params):
        conf = self._git_config
        try:
            secion, param = params.split('.')
            result = conf.get(secion, param)
        except:
            result = None
        return result

    def has_remotes(self):
        remotes = self.remotes()
        has_remotes = len(remotes)
        result = False
        if has_remotes > 0:
            for remote in remotes:
                remote_url = remote['url']
                if search('sapp.io', remote_url):
                    result = True
                    break

        return result

    def remotes(self):
        result = []
        remotes = self._git_config.remotes
        for remote in remotes:
            remote_url = remotes[remote]['url']
            if search('sapp.io', remote_url):
                the_remote = remotes[remote]
                the_remote['name'] = remote
                result.append(the_remote)

        return result

    def details_from_url(self, url):
        details = search('//(.*)@(.*)-(.*).sapp', url)
        app_id, app_name, app_namespace = details.groups()
        result = {
            'app-id': app_id,
            'app-name': app_name,
            'domain-name': app_namespace
        }
        return result

    def set_rhc(self, app_details):
        config = self._git_config

        for detail in app_details:
            config.set('rhc', detail, app_details[detail])

        config.save()

    def set_remote(self, remote_name):
        remotes = self.remotes()

        for remote in remotes:
            if remote['name'] == remote_name:
                details = self.details_from_url(remote['url'])
                self.set_rhc(details)
                return True

        return False

    def is_app(self):
        return self.app_id()

    def app_name(self):
        return self._git_config_get('rhc.app-name')

    def app_namespace(self):
        return self._git_config_get('rhc.domain-name')

    def app_id(self):
        return self._git_config_get('rhc.app-id')

    def src(self):
        return self.repo

    def dest(self):
        url = "{0}@{1}-{2}.sapp.io:~/app-root/repo" \
            .format(self.app_id(), self.app_name(), self.app_namespace())
        return url


class StatappSyncHandler(FileSystemEventHandler):

    """Rsync on every file change"""

    def __init__(self, **kwargs):

        logging.basicConfig(level=logging.INFO, \
            format='%(asctime)s - %(message)s', \
            datefmt='%Y-%m-%d %H:%M:%S')

        self.source = kwargs.get('src', None)
        self.dest = kwargs.get('dest', None)

    def on_moved(self, event):
        super(StatappSyncHandler, self).on_moved(event)
        rsync(self.source, self.dest)
        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        super(StatappSyncHandler, self).on_created(event)
        rsync(self.source, self.dest)
        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(StatappSyncHandler, self).on_deleted(event)
        rsync(self.source, self.dest)
        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(StatappSyncHandler, self).on_modified(event)
        what = 'directory' if event.is_directory else 'file'

        if what == 'file':
            rsync(self.source, self.dest)

        logging.info("Modified %s: %s", what, event.src_path)
