from __future__ import with_statement
from startappsync import App

import os
import unittest
import re
import subprocess
import sys

class TestCaseBase(unittest.TestCase):

    # HACK: Backport for Python 2.6.
    def assertRegexpMatches(self, value, regexp):
        self.assertTrue(re.search(regexp, value))

    # HACK: Backport for Python 2.6.
    def assertNotIn(self, value, container):
        self.assertFalse(value in container)


class StartAppSyncTest(TestCaseBase):
    def setUp(self):

        if not re.search(r'/tests', os.getcwd()):
            cwd = '{0}/tests'.format(os.getcwd())
        else:
            cwd = os.getcwd()

        self.no_repo = '{0}/fixtures/'.format(cwd)
        self.empty_dir = '{0}empty_dir_with_no_git_repo'.format(self.no_repo)
        self.dummy_repo = '{0}/fixtures/dummyrepo'.format(cwd)
        self.dummy_repo_without_rhc_conf = '{0}/fixtures/dummyrepo_without_rhc_conf'.format(cwd)
        self.dummy_repo_with_one_remote = '{0}/fixtures/dummyrepo_with_one_remote'.format(cwd)
        self.dummy_repo_with_many_remotes = '{0}/fixtures/dummyrepo_with_many_remotes'.format(cwd)

        os.system("mkdir {0}".format(self.empty_dir))

    def tearDown(self):
        os.system("rm -rf {0}".format(self.empty_dir))

    def cmd(self, *args):
        os.environ['STARTAPPSYNC_TEST_ENV'] = 'true'
        process = subprocess.Popen(*args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        output = out + err
        return_code = process.wait()
        result = { "output": output, "return_code": return_code }
        return result

    def test_app_has_remotes_with_repo_without_remotes(self):
        app = App(repo=self.dummy_repo)
        self.assertFalse(app.has_remotes())

    def test_app_has_remotes_with_repo_with_one_remote(self):
        app = App(repo=self.dummy_repo_with_one_remote)
        self.assertTrue(app.has_remotes())

    def test_app_has_remotes_with_repo_with_many_remote(self):
        app = App(repo=self.dummy_repo_with_many_remotes)
        self.assertTrue(app.has_remotes())

    def test_app_appname_from_git(self):
        app = App(repo=self.dummy_repo)
        result = app.app_name()
        self.assertEqual(result, 'appname')

    def test_app_namespace_from_git(self):
        app = App(repo=self.dummy_repo)
        result = app.app_namespace()
        self.assertEqual(result, 'appnamespace')

    def test_app_app_id_from_git(self):
        app = App(repo=self.dummy_repo)
        result = app.app_id()
        self.assertEqual(result, '535650470fe7e618ef000272')

    def test_get_app_details_from_ssh_url(self):
        app = App(repo=self.dummy_repo_with_many_remotes)

        remote_url = app.remotes()[0]['url']
        app_details = app.details_from_url(remote_url)
        self.assertEqual('repo-user', app_details['app-id'])
        self.assertEqual('repo', app_details['app-name'])
        self.assertEqual('host', app_details['domain-name'])


    def test_set_rhc_details_in_gitconfig(self):
        old_repo_path = self.dummy_repo_with_many_remotes
        new_repo_path = "{0}repo_test_set_rhc_in_gitconfig"\
            .format(self.no_repo)

        dublicate_repo_cmd = "cp -R {0} {1}"\
            .format(old_repo_path, new_repo_path)

        os.system("rm -rf {0}".format(new_repo_path))
        os.system(dublicate_repo_cmd)

        app = App(repo=new_repo_path)
        remote_url = app.remotes()[0]['url']
        app_details = app.details_from_url(remote_url)
        app.set_rhc(app_details)

        self.assertEqual('repo-user', app.app_id())
        self.assertEqual('repo', app.app_name())
        self.assertEqual('host', app.app_namespace())

        os.system("rm -rf {0}".format(new_repo_path))

    def test_run_startappsync_with_non_existing_dir(self):
        os.environ['STARTAPPSYNC_TEST_CWD'] = '/some/not/existing/dir'
        result = self.cmd(['bin/startappsync'])
        self.assertRegexpMatches(result['output'], "Uuuups ... the directory you are looking for is not exist!")
        self.assertEqual(result['return_code'], 1)

    def test_run_startappsync_in_dir_without_gitrepo(self):
        os.environ['STARTAPPSYNC_TEST_CWD'] = self.empty_dir
        result = self.cmd(['bin/startappsync'])
        print result['output']
        self.assertRegexpMatches(result['output'], "Uuuups ... I can't find Git repo here!")
        self.assertEqual(result['return_code'], 1)

    def test_run_startappsync_in_dir_with_gitrepo(self):
        os.environ['STARTAPPSYNC_TEST_CWD'] = self.dummy_repo
        result = self.cmd(['bin/startappsync'])

        self.assertRegexpMatches(result['output'], 'Hi Dude!')
        self.assertRegexpMatches(result['output'], self.dummy_repo)
        self.assertRegexpMatches(result['output'], '535650470fe7e618ef000272@appname-appnamespace.sapp.io:~/app-root/repo')
        self.assertEqual(result['return_code'], 0)

    def test_run_startappsync_in_dir_with_gitrepo_but_without_rhc_in_conf(self):
        os.environ['STARTAPPSYNC_TEST_CWD'] = self.dummy_repo_without_rhc_conf
        result = self.cmd(['bin/startappsync'])

        self.assertRegexpMatches(result['output'], 'Sorry Dude')
        # self.assertRegexpMatches(result['output'], '535650470fe7e618ef000272@appname-appnamespace.sapp.io:~/app-root/repo')
        self.assertEqual(result['return_code'], 1)

    def test_run_startappsync_in_dir_with_gitrepo_but_without_rhc_in_conf_and_with_startapp_repos(self):
        os.environ['STARTAPPSYNC_TEST_CWD'] = self.dummy_repo_with_many_remotes
        result = self.cmd(['bin/startappsync'])

        self.assertRegexpMatches(result['output'], 'Sorry Dude')
        self.assertRegexpMatches(result['output'], '- ssh://repo-user@repo-host.sapp.io/~/git/repo.git/\n')
        self.assertRegexpMatches(result['output'], 'If you want to use some of them you have to type:')
        self.assertEqual(result['return_code'], 1)

    def test_set_rhc_details_in_gitconfig_from_cli(self):
        old_repo_path = self.dummy_repo_with_many_remotes
        new_repo_path = "{0}repo_test_set_rhc_in_gitconfig"\
            .format(self.no_repo)

        os.system("rm -rf {0}".format(new_repo_path))
        dublicate_repo_cmd = "cp -R {0} {1}"\
            .format(old_repo_path, new_repo_path)

        os.system(dublicate_repo_cmd)

        os.environ['STARTAPPSYNC_TEST_CWD'] = new_repo_path
        result = self.cmd(['bin/startappsync', '--set-remote', 'origin'])
        self.assertRegexpMatches(result['output'], "Remote with name 'origin' was successfuly added!")

        app = App(repo=new_repo_path)
        self.assertEqual('repo-user', app.app_id())
        self.assertEqual('repo', app.app_name())
        self.assertEqual('host', app.app_namespace())

        os.system("rm -rf {0}".format(new_repo_path))


    # def test_run_startappsync_with_repo_argument_with_nonexisting_repo(self):
    #     pass

    # def test_run_startappsync_with_repo_argument_with_existing_repo(self):
    #     pass

    # def test_run_startappsync_with_from_argument_but_without_to_argument(self):
    #     pass

    # def test_run_startappsync_with_from_and_to_arguments(self):
    #     pass

if __name__ == "__main__":
    unittest.main()
