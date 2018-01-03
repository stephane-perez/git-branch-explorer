Git branch explorer
===================

What is it?
-----------

It exports all information about branches (local and remote) from the parent
directory where Git repositories are.

Requirements
------------

- GitPython
see http://gitpython.readthedocs.io/en/stable/
installation :
$ sudo pip install gitpython

Usage
-----

$ python explorer.py --parent-dir /my_parent_dir/all_projects --output /tmp/all_projects.json

or

$ python explorer.py -p /my_parent_dir/all_projects -o /tmp/all_projects.json
