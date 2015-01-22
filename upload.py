#!/usr/bin/env python
# pylint: disable=missing-docstring

import urllib, mimetypes, pycurl
import sys
import os
import re


# Read .flockignore
# Read supplied Directory & subdirectories
#   ignore all files listed in .flockignore
#   find MIME
#   Upload

# Usage: upload.py appId directory

IGNORE_FILE = ".flockignore"
DEFAULT_IGNORE = ['.git', '.flockignore', '*.DS_Store']

def read_flock_ignore(base_directory):
    ignore_filepath = '/'.join([base_directory, IGNORE_FILE])

    ignore_content = {}
    for ignore in DEFAULT_IGNORE:
        ignore_content[ignore] = pre_compile_regex(ignore)

    if os.path.isfile(ignore_filepath):
        with open(ignore_filepath) as ignore_file:
            for line in ignore_file:
                line = line.rstrip('\n')

                if len(line) > 0:
                    ignore_content[line] = pre_compile_regex(line)
    return ignore_content

def get_files_to_upload(working_path, ignore_content):
    # traverse root directory, and list directories as dirs and files as files
    upload_list = []
    for dirpath, dirnames, files in os.walk(working_path):
        relative_path = dirpath.split(working_path)[1]

        # Remove empty path part if there are any.
        path_parts = relative_path.split("/")
        if '' in path_parts:
            path_parts.remove('')

        #Prune the subdirectories - they will not be walked into if they are pruned.
        for dirname in dirnames:
            tmp = path_parts[:]
            tmp.append(dirname)
            dirpath = '/'.join(tmp)
            if should_prune(dirpath, ignore_content):
                dirnames.remove(dirname)

        # Check files for inclusion!
        for ul_file in files:
            tmp = path_parts[:]
            tmp.append(ul_file)
            filepath = '/'.join(tmp)
            if not should_prune(filepath, ignore_content):
                upload_list.append(filepath)

    return upload_list

def pre_compile_regex(search):
    escapedre = re.escape(search)
    escapedre = escapedre.replace(r"\*", '.*') + '$'
    return re.compile(escapedre)

def should_prune(path, ignore_content):
    should_ignore = False
    for ignore_regex in ignore_content.values():
        if simple_regex_check(ignore_regex, path):
            should_ignore = True
    return should_ignore

def simple_regex_check(compiledre, path):
    return compiledre.match(path) != None

def upload_files(app_id, base_directory, files):
    for filepath in files:
        curl_upload(app_id, '/'.join([base_directory, filepath]))

def curl_upload(app_id, filepath):
    mime = mimetypes.MimeTypes()

    fileurl = urllib.pathname2url(filepath)
    mime_type, _ = mime.guess_type(fileurl)

    # with open(file) as f:
    curl = pycurl.Curl()
    curl.setopt(curl.PUT, 1)
    curl.setopt(curl.URL, "http://127.0.0.1:8000/%s/%s" % (app_id, filepath))
    curl.setopt(curl.HTTPHEADER, ["Content-Type: %s" % (mime_type)])
    # curl.setopt(curl.READDATA, f)
    curl.setopt(curl.VERBOSE, 1)
    curl.setopt(curl.UPLOAD, 1)
    curl.setopt(curl.READFUNCTION, open(filepath, 'rb').read)
    filesize = os.path.getsize(filepath)
    curl.setopt(curl.INFILESIZE, filesize)
    curl.perform()
    curl.close()


def main(app_id, base_directory):
    ignore_content = read_flock_ignore(base_directory)
    upload_list = get_files_to_upload(base_directory, ignore_content)
    upload_files(app_id, base_directory, upload_list)


if __name__ == '__main__':
    APP_ID = sys.argv[1]
    BASE_DIRECTORY = sys.argv[2]
    main(APP_ID, BASE_DIRECTORY)
