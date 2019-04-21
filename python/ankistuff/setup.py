#! /usr/bin/python

from distutils.core import setup
from distutils.extension import Extension
import subprocess 

def pkgconfig(*packages, **kw):
	flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
	#for token in subprocess.run("pkg-config --libs --cflags %s" % ' '.join(packages), capture_output=True).split():
	for token in ["-I/usr/local/sword/include/sword","-L/usr/local/sword/lib","-lsword"]:
		if token[:2] in flag_map:
			kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
		else: # throw others to extra_link_args
			kw.setdefault('extra_link_args', []).append(token)
	for k, v in kw.items(): # remove duplicated
		kw[k] = list(set(v))
	return kw

setup (name = "sword",
	version = "1.6.2",
	maintainer = "Sword Developers",
	maintainer_email = "sword-devel@crosswire.org",
	url = "http://www.crosswire.org/sword",
	py_modules = ["Sword"],
	include_dirs=['..', '../..'],
	ext_modules = [Extension("_Sword", ["Sword.cxx"], **pkgconfig('sword')
	)], 
)
