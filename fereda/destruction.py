# -*- coding: utf-8 -*-
import os
import subprocess

from . import __version__
from .displayinfo import DisplayInfo


class SelfDestruction:
    _operation_system = subprocess.check_output(['uname', '-o']).decode('utf-8')

    @staticmethod
    def destruction():
        file_bin = '~/.local/bin/fereda'
        egg = f'~/.local/lib/python3.7/site-packages/Fereda-{__version__}-py3.7.egg'

        if os.path.isfile(file_bin) and os.path.isfile(egg):
            os.remove(file_bin)
            os.remove(egg)
            DisplayInfo.show_info(DisplayInfo.self_destruction_ok.value)

    def destruction_handler(self):
        if self._operation_system != 'GNU/Linux':
            return

        if self._operation_system == 'GNU/Linux':
            self.destruction()
