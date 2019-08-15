from .AssetsManager import AssetsManager
# preperation for FMOD / pyfmodex which requires those files in PATH
import os
import platform

if platform.architecture()[0] == "32bit":
	os.environ['PATH'] += f";{os.path.join(os.path.dirname(__file__), *['external', 'FMOD', 'x32'])}"
else:
	os.environ['PATH'] += f";{os.path.join(os.path.dirname(__file__), *['external', 'FMOD', 'x64'])}"


