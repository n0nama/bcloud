from django.core.files.storage import FileSystemStorage
from django.core.files.storage import Storage
from django.conf import settings
from django.core.files import locks, File

import hashlib
import os
import errno


class FSS(FileSystemStorage):

    def get_available_name(self, name):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name