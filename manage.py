#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals
import os
import sys

if __name__ == '__name__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 't.proj.settings')

    from django.core.manegement import execute_from_command_line

    execute_from_command_line(sys.argv)