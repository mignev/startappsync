import subprocess
import os
import logging

from watchdog.events import FileSystemEventHandler

version = "0.0.1"
version_info = (0, 0, 1)

class Git():
    def __init__(self, **kwargs):
        current_working_dir = os.getcwd()
        self.repo = kwargs.get('repo', current_working_dir)

    def _set_git_config(self):
        os.environ['GIT_CONFIG'] = "{0}/.git/config".format(self.repo)

    def cmd(self, *args):
        self._set_git_config()
        process = subprocess.Popen(*args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.communicate()[0]

    def get_conf(self, param):
        cmd = self.cmd(['git', 'config', '--get', param])
        cmd = cmd.strip()
        if cmd == '':
            cmd = None
        return cmd

    def has_repo(self):
        git_repo = "{0}/.git".format(self.repo)
        return os.path.isdir(git_repo)

    def app_name(self):
        result = self.get_conf('rhc.app-name')
        return result

    def app_namespace(self):
        result = self.get_conf('rhc.domain-name')
        return result

    def app_id(self):
        result = self.get_conf('rhc.app-id')
        return result

class App():
    def __init__(self, **kwargs):
        self.repo = kwargs.get('repo', '.')
        git = Git(repo=self.repo)
        self.app_name = git.app_name()
        self.app_namespace = git.app_namespace()
        self.app_id = git.app_id()

    def is_app(self):
        return self.app_id

    def src(self):
        return self.repo

    def dest(self):
        url = "{0}@{1}-{2}.sapp.io:~/app-root/repo" \
            .format(self.app_id, self.app_name, self.app_namespace)
        return url

def rsync(source, destination):
    _cmd = 'rsync -ahz --rsh="ssh" --delete ' + source + ' ' + destination
    cmd(_cmd)

def cmd(cmd):
    process = subprocess.Popen(cmd,
      shell=True,
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
    )
    return process

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
