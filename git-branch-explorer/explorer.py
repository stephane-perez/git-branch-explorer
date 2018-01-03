# !/usr/bin/python
# -*- coding: utf8 -*-

import argparse
import json
import logging
import os
import sys

from repository import *


def parse_args():
    parser = argparse.ArgumentParser(description='Explore GIT branches in all subdirs')

    parser.add_argument('--parent-dir', '-p', required=True, dest='parent_dir', help='the parent of directories'
                                                                                     'containing GIT repositories')
    parser.add_argument('--output', '-o', required=True, dest='output', help='output file')
    return parser.parse_args()


def init_logger():
    global logger

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "git-branch-explorer.log"))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def get_immediate_subdirectories(my_dir):
    return filter(os.path.isdir, [os.path.join(my_dir, f) for f in os.listdir(my_dir)])


def process_subdirectories():
    reps = []
    dirs = get_immediate_subdirectories(args.parent_dir)
    for _dir in dirs:
        logger.info('exploring %s', _dir)
        try:
            repository = Repository()
            repository.path = _dir
            repository.extract_local_branches_from_directory()
            repository.extract_remote_branches_from_directory()
            reps.append(repository)
        except (InvalidGitRepositoryError, GitCommandError) as git_err:
            logger.warn('Git error in directory %s (%s)', _dir, git_err)
        except Exception as err:
            raise ValueError('error in processing %s (%s)', _dir, err)
    return reps


def obj_dict(obj):
    return obj.__dict__


def export_to_output_file(reps):
    try:
        json_string = json.dumps([ob.__dict__ for ob in reps])
        logging.info(json_string)
        with open(args.output, 'w') as f:
            json.dump(reps, f, default=obj_dict)
    except Exception as err:
        raise ValueError('error when exporting to output file', err)


if __name__ == '__main__':
    global args
    args = parse_args()
    init_logger()
    try:
        repositories = process_subdirectories()
        export_to_output_file(repositories)
    except ValueError as e:
        logger.error(e)
        sys.exit(1)
    sys.exit(0)
