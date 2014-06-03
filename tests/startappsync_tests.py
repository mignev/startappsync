from __future__ import with_statement
from startappsync import Git
import os
import unittest
import mock
import re
import shutil

class StartAppSyncTest(unittest.TestCase):
    def setUp(self):

        if not re.search(r'/tests', os.getcwd()):
            cwd = '{0}/tests'.format(os.getcwd())
        else:
            cwd = os.getcwd()

        self.dummy_repo = 'fixtures/dummyrepo'

    @mock.patch('startappsync.os')
    def test_git_without_specify_path(self, mock_cwd):
        mock_cwd.getcwd.return_value = '/current/working/dir'
        git = Git()
        self.assertEqual(git.repo, '/current/working/dir')

    def test_git_with_specifyc_git_path(self):
        git = Git(repo='/some/custom/path')
        self.assertEqual(git.repo, '/some/custom/path')

    def test_git_has_repo(self):
        git = Git(repo=self.dummy_repo)
        self.assertTrue(git.has_repo())

    def test_get_appname_from_git(self):
        git = Git(repo=self.dummy_repo)
        result = git.app_name()
        self.assertEqual(result, 'appname')

    def test_get_namespace_from_git(self):
        git = Git(repo=self.dummy_repo)
        result = git.app_namespace()
        self.assertEqual(result, 'appnamespace')

    def test_get_app_id_from_git(self):
        git = Git(repo=self.dummy_repo)
        result = git.app_id()
        self.assertEqual(result, '535650470fe7e618ef000272')


if __name__ == "__main__":
    unittest.main()
