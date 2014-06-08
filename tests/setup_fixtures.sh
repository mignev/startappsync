#!/usr/bin/env bash

pushd fixtures
  rm -rf dummyrepo empty_dir dummyrepo_with_many_remotes dummyrepo_with_one_remote dummyrepo_without_rhc_conf

  mkdir empty_dir
  mkdir dummyrepo

  cd dummyrepo
  git init
  touch dummy_file
  git add .
  git commit -am "Initial Commit"
  cd ..

  cp -R dummyrepo dummyrepo_with_many_remotes
  cp -R dummyrepo dummyrepo_with_one_remote
  cp -R dummyrepo dummyrepo_without_rhc_conf

  cd dummyrepo
  git config rhc.app-id "535650470fe7e618ef000272"
  git config rhc.app-name "appname"
  git config rhc.domain-name "appnamespace"
  cd ..

  cd dummyrepo_with_one_remote
  git remote add origin ssh://repo-user@repo-host.sapp.io/~/git/repo.git/
  cd ..

  cd dummyrepo_with_many_remotes
  git remote add origin ssh://repo-user@repo-host.sapp.io/~/git/repo.git/
  git remote add origin1 ssh://repo-user1@repo-host1.sapp.io/~/git/repo1.git/
  git remote add origin2 ssh://repo-user2@repo-host2.sapp.io/~/git/repo2.git/
popd
