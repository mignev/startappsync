import os
from re import search

from gitconfig.config import (
    ConfigDict,
    ConfigFile,
    )

class GitRepoNotFoundError(Exception): pass

class GitConfig():

    def __init__(self,**kwargs):
        self.path = kwargs.get('path', None)
        self.file = kwargs.get('file', None)

        if self.path:
            if os.path.exists(self.path):

                config_path = self.detect_git_config(self.path)
                if os.path.exists(config_path):
                    self.config_path = config_path
                    self.config = ConfigFile.from_path(config_path)
                else:
                    raise GitRepoNotFoundError(self.path)
            else:
                raise IOError(self.path)

        else:
            self.config = ConfigFile.from_file(self.file)

    def detect_git_config(self, path):
        config_path = ""
        if search(r'\.git/config', path):
            config_path = path
        elif search(r'\.git', path):
            config_path = "{0}/config".format(path)
        else:
            config_path = "{0}/.git/config".format(path)

        return config_path

    def has_remotes(self):
        return self.has_section('remote')

    def has_remote(self, remote_name):
        return self.has_section('remote', remote_name)

    def has_section(self, section_type, section_name = ''):
        config_sections = self.config.itersections()

        """
            These variables are used in return statements only
            They are used to experiment with readability
        """
        yes_there_is_section_with_this_name = yes_this_section_exists = True
        sorry_search_section_doest_not_exist = False


        for section in config_sections:
            this_section_type = section[0]
            search_for_section_with_spcific_name = (section_name != '')

            if not search_for_section_with_spcific_name:

                if this_section_type == section_type:
                    return yes_this_section_exists # True
            else:
                try:
                    this_section_name = section[1]
                    if this_section_name == section_name:
                        return yes_there_is_section_with_this_name # True
                except IndexError:
                    """ These type of sections are like [core], [alias], [user]"""
                    continue

        return sorry_search_section_doest_not_exist # False

    @property
    def remotes(self):
        config_sections = self.config.items()
        remotes = {}

        for section in config_sections:
            section_type = section[0][0]
            if section_type == 'remote':

                remote_name = section[0][1]
                remote_properties = section[1]

                remotes[remote_name] = remote_properties

        return remotes

    @property
    def sections(self):
        config_sections = self.config.items()
        return [section[0][0] for section in config_sections]

    def set(self, section, key, value):
        return self.config.set((section,), key, value)

    def get(self, section, key):
        section_details = section.split('.')

        if len(section_details) == 2:
            section_type, section_name = section_details
        else:
            section_type, section_name = (section, '')

        return self.config.get((section_type, section_name), key)

    def save(self):
        return self.config.write_to_path(self.config_path)

