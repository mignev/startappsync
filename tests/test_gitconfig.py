from __future__ import with_statement
import sys, os, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from io import BytesIO

from gitconfig.core import GitConfig, GitRepoNotFoundError
from tests import TestCase, unittest


class ConfigFileTests(TestCase):

    def config_with_many_remotes(self):
        return """[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
    [remote "origin"]
      url = ssh://repo-user@repo-host.sapp.io/~/git/repo.git/
      fetch = +refs/heads/*:refs/remotes/origin/*
    [remote "origin1"]
      url = ssh://repo-user1@repo-host1.sapp.io/~/git/repo1.git/
      fetch = +refs/heads/*:refs/remotes/origin1/*
    [remote "origin2"]
      url = ssh://repo-user2@repo-host2.sapp.io/~/git/repo2.git/
      fetch = +refs/heads/*:refs/remotes/origin2/*
    [rhc]
      app-id = 19192929
      app-name = myname
"""


    def setUp(self):

        if not re.search(r'/tests', os.getcwd()):
            cwd = '{0}/tests'.format(os.getcwd())
        else:
            cwd = os.getcwd()

        self.no_repo = '{0}/fixtures/'.format(cwd)
        self.dummy_repo_with_many_remotes = '{0}/fixtures/dummyrepo_with_many_remotes'.format(cwd)

        many_remotes_conf = self.config_with_many_remotes().encode("utf-8")
        self.git_config = GitConfig(file=BytesIO(many_remotes_conf))

    def test_gitconfig_has_remotes(self):
        has_repos = self.git_config.has_remotes()
        self.assertTrue(has_repos)

    def test_has_specific_remote(self):
        has_origin = self.git_config.has_remote('origin')
        self.assertTrue(has_origin)

    def test_not_existing_remote(self):
        has_origin = self.git_config.has_remote('not_existing_remote_name')
        self.assertFalse(has_origin)

    def test_has_section_with_name(self):
        has_section = self.git_config.has_section('rhc')
        self.assertTrue(has_section)

        has_section = self.git_config.has_section('remote')
        self.assertTrue(has_section)

    def test_not_existing_section(self):
        has_section = self.git_config.has_section('not_existing_section')
        self.assertFalse(has_section)

    def test_has_specific_section_with_not_existing_specific_name(self):
        has_section = self.git_config.has_section('remote', 'origin-test')
        self.assertFalse(has_section)

    def test_has_specific_section_with_specific_name(self):
        has_section = self.git_config.has_section('remote', 'origin')
        self.assertTrue(has_section)

        has_section = self.git_config.has_section('remote', 'origin1')
        self.assertTrue(has_section)

    def test_remotes(self):
        remotes = self.git_config.remotes
        remotes_count = len(remotes)
        self.assertEqual(remotes_count, 3)

    def test_get_remote_url(self):
        remotes = self.git_config.remotes
        origin_url = remotes['origin']['url']
        origin_fetch = remotes['origin']['fetch']

        self.assertEqual(origin_url, 'ssh://repo-user@repo-host.sapp.io/~/git/repo.git/')
        self.assertEqual(origin_fetch, '+refs/heads/*:refs/remotes/origin/*')

    def test_sections(self):
        sections = self.git_config.sections
        self.assertTrue('rhc' in sections)
        self.assertTrue('remote' in sections)
        self.assertFalse('not_existing' in sections)
        self.assertFalse('origin' in sections)
        self.assertFalse('master' in sections)


    def test_set_section_value(self):
        config = self.git_config
        section = 'section_name'
        property_name = 'property_name'
        property_value = 'property_value'

        config.set(section, property_name, property_value)

        self.assertTrue(config.has_section(section))

    def test_get_section_value(self):
        config = self.git_config
        section = 'section_name'
        property_name = 'property_name'
        property_value = 'property_value'
        config.set(section, property_name, property_value)

        self.assertEqual(config.get(section, property_name), property_value)
        self.assertNotEqual(config.get(section, property_name), property_name)

    def test_get_section_value_with_specific_type_and_name(self):
        config = self.git_config
        remote_url = 'ssh://repo-user@repo-host.sapp.io/~/git/repo.git/'
        fetch = '+refs/heads/*:refs/remotes/origin/*'

        self.assertEqual(config.get('remote.origin', 'url'), remote_url)
        self.assertEqual(config.get('remote.origin', 'fetch'), fetch)

    def test_save_config(self):
        old_repo_path = self.dummy_repo_with_many_remotes
        new_repo_path = "{0}repo_test_set_gitconfig_sections"\
            .format(self.no_repo)

        dublicate_repo_cmd = "cp -R {0} {1}"\
            .format(old_repo_path, new_repo_path)

        os.system("rm -rf {0}".format(new_repo_path))
        os.system(dublicate_repo_cmd)

        config = GitConfig(path=new_repo_path)
        section = 'section'
        property_name = 'key'
        property_value = '+refs/heads/*:refs/remotes/origin/*'
        config.set(section, property_name, property_value)

        config.save()
        config = GitConfig(path=new_repo_path)
        self.assertTrue(section in config.sections)

        os.system("rm -rf {0}".format(new_repo_path))

    def gitconfig_init_open_repo_paths_helper(self, path):
        config = GitConfig(path=path)

        self.assertTrue(config.has_section('core'))
        is_bare_test = config.get('core','bare')
        self.assertEqual(is_bare_test, 'false')

    def test_gitconfig_detect_config_file_from_repo_path(self):
        repo = self.dummy_repo_with_many_remotes
        self.gitconfig_init_open_repo_paths_helper(repo)

    def test_gitconfig_detect_config_file_from_dot_git_repo_path(self):
        repo = '{0}/.git'.format(self.dummy_repo_with_many_remotes)
        self.gitconfig_init_open_repo_paths_helper(repo)

    def test_gitconfig_detect_config_file_from_dot_git_repo_path(self):
        repo = '{0}/.git/config'.format(self.dummy_repo_with_many_remotes)
        self.gitconfig_init_open_repo_paths_helper(repo)

    def test_gitconfig_open_not_existing_path(self):
        repo = '/some/fake/path'
        with self.assertRaises(IOError):
            GitConfig(path=repo)

    def test_gitconfig_open_path_of_not_existing_repo(self):
        repo = self.no_repo
        with self.assertRaises(GitRepoNotFoundError):
            GitConfig(path=repo)



if __name__ == "__main__":
    unittest.main()
