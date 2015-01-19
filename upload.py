#7751e2923d2fb1c807881f0421b07df6cf93a4d8
import urllib, mimetypes, pycurl
import sys
import os

# Read .flockignore
# Read supplied Directory & subdirectories
# 	ignore all files listed in .flockignore 
# 	find MIME
#	Upload

# Usage: upload.py appId directory
print sys.argv

appId = sys.argv[1]
directory = sys.argv[2]

IGNORE_FILE = ".flockignore"
ignore_filepath = "%s/%s" % (directory, ".flockignore")

print "isfile? : " + str(os.path.isfile(ignore_filepath))

ignore_content = {}
if os.path.isfile(ignore_filepath):
	with open(ignore_filepath) as f:
	    for line in f:
			l = line.rstrip('\n')
			if len(l) > 0:
				ignore_content[l] = True

print ignore_content

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("."):
    path = root.split('/')
    print (len(path) - 1) *'---' , os.path.basename(root)       
    for file in files:
        print len(path)*'---', file, '    ', dirs, '   ', root

"""
mime = MimeTypes()
url = urllib.pathname2url('Upload.xml')
mime_type = mime.guess_type(url)

c = pycurl.Curl()
c.setopt(c.PUT, 1)
c.setopt(c.URL, "http://127.0.0.1:8000/%s/%s")
c.setopt(c.HTTPPOST, [("file1", (c.FORM_FILE, "c:\\tmp\\download\\test.jpg"))])
c.setopt(c.HTTPHEADER, ["Content-Type: %s" % (mime_type)])
#c.setopt(c.VERBOSE, 1)
c.perform()
c.close()
"""