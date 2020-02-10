# -*- coding: utf-8 -*-

# This file is part of Fereda.

# Fereda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License 3 as published by
# the Free Software Foundation.

# Fereda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Fereda.  If not, see <https://www.gnu.org/licenses/>.


# Copyright (c) 2020 January mkbeh


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
