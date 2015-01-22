import urllib, mimetypes, pycurl
import sys
import os
import re


# Read .flockignore
# Read supplied Directory & subdirectories
# 	ignore all files listed in .flockignore 
# 	find MIME
#	Upload

# Usage: upload.py appId directory

IGNORE_FILE = ".flockignore"
DEFAULT_IGNORE = ['.git', '.flockignore', '*.DS_Store']

def readFlockIgnore(baseDirectory):
	ignore_filepath = '/'.join([directory, ".flockignore"])

	ignore_content = {}
	for ignore in DEFAULT_IGNORE:
		ignore_content[ignore] = pre_compile_regex(ignore)

	if os.path.isfile(ignore_filepath):
		with open(ignore_filepath) as f:
		    for line in f:
				l = line.rstrip('\n')

				if len(l) > 0:
					ignore_content[l] = pre_compile_regex(l)
	return ignore_content

def getFilesToUpload(working_path, ignore_content):
	# traverse root directory, and list directories as dirs and files as files
	uploadList = []
	for dirpath, dirnames, files in os.walk(working_path):
		relative_path = dirpath.split(working_path)[1]

		# Remove empty path part if there are any. 
		path_parts = relative_path.split("/")
		if '' in path_parts:
			path_parts.remove('')

		#Prune the subdirectories - they will not be walked into if they are pruned. 
		for dir in dirnames:
			tmp = path_parts[:]
			tmp.append(dir)
			dirpath = '/'.join(tmp)
			if should_prune(dirpath, ignore_content):
				dirnames.remove(dir)

		# Check files for inclusion!
		for file in files:
			tmp = path_parts[:]
			tmp.append(file)
			filepath = '/'.join(tmp)
			if not should_prune(filepath, ignore_content):
				uploadList.append(filepath)

	return uploadList

def pre_compile_regex(search):
	escapedre = re.escape(search)
	escapedre = escapedre.replace('\*', '.*') + '$'
	return re.compile(escapedre)

def should_prune(path, ignore_content):
	shouldIgnore = False
	for ignore, ignore_regex in ignore_content.items():
		if simplistic_regex(ignore_regex, path):
			print('matched regex,file: ', ignore, ', ', path)
			shouldIgnore = True
	return shouldIgnore

def simplistic_regex(compiledre, path):
    return compiledre.match(path) != None

def upload_files(app_id, base_directory, files):
	for f in files:
		curl_upload(app_id, '/'.join([base_directory,f]))

def curl_upload(app_id, file):
	mime = mimetypes.MimeTypes()

	filename = file.split('/')[-1]
	fileurl = urllib.pathname2url(file)
	mime_type, mime_encoding = mime.guess_type(fileurl)
	print filename, ' ', mime_type

	# with open(file) as f:
	c = pycurl.Curl()
	c.setopt(c.PUT, 1)
	c.setopt(c.URL, "http://127.0.0.1:8000/%s/%s" % (app_id, file))
	c.setopt(c.HTTPHEADER, ["Content-Type: %s" % (mime_type)])
	# c.setopt(c.READDATA, f)
	c.setopt(c.VERBOSE, 1)
	c.setopt(pycurl.UPLOAD, 1)
	c.setopt(pycurl.READFUNCTION, open(file, 'rb').read)
	filesize = os.path.getsize(filename)
	c.setopt(pycurl.INFILESIZE, filesize)
	c.perform()
	c.close()


def main(app_id, base_directory):
	ignore_content = readFlockIgnore(base_directory)
	upload_list = getFilesToUpload(base_directory, ignore_content)
	upload_files(app_id, base_directory, upload_list)
	

	# working_path = '/'.join([os.getcwd(), directory]) + '/'
	# print "working_path: " + working_path + " is_dir:" + str(os.path.isdir(working_path))


if __name__ == '__main__':
	appId = sys.argv[1]
	directory = sys.argv[2]
	main(appId, directory)

# print('uploadList: ' , uploadList)

	#cases
	#1: Just a filename/filepath
	#2: Something requiring regex


"""

"""