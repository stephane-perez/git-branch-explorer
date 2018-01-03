# -*- coding: utf8 -*-

from git import Repo
from git.exc import InvalidGitRepositoryError
from git.exc import GitCommandError


class Repository(object):

    def __init__(self):
        self.path = ''
        self.localBranches = []
        self.remoteBranches = []

    @staticmethod
    def __fetch_from_repository__(self, repository):
        for remote in repository.remotes:
            try:
                remote.fetch()
            except (InvalidGitRepositoryError, GitCommandError) as err:
                raise err

    def extract_local_branches_from_directory(self):
        """ Extract all local branches from the given Git directory
        >>> repository = Repository()
        >>> repository.path = ".."
        >>> branches = repository.extract_local_branches_from_directory()
        >>> len(repository.localBranches) > 0
        True
        """
        branches = []
        git_repo = Repo(self.path)
        self.__fetch_from_repository__(self, git_repo)
        heads = git_repo.heads
        for branch in heads:
            if branch == git_repo.active_branch:
                branches.append('* ' + branch.name)
            else:
                branches.append(branch.name)
        self.localBranches = branches

    def extract_remote_branches_from_directory(self):
        """ Extract all remote branches from the given directory
        >>> repository = Repository()
        >>> repository.path = ".."
        >>> branches = repository.extract_remote_branches_from_directory()
        >>> len(repository.remoteBranches) > 0
        True
        """
        branches = []
        git_repo = Repo(self.path)
        self.__fetch_from_repository__(self, git_repo)
        refs = git_repo.references
        for branch in refs:
            if branch.is_remote():
                branches.append(branch.name)
        self.remoteBranches = branches
