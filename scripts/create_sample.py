#!/usr/bin/env python
import os
import sys

wd = os.path.join(os.path.dirname(sys.argv[0]), os.path.pardir)
sys.path.insert(0, os.path.abspath(wd))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

import django
django.setup()

from main.management.appcache import create_manifest
from ropeelements.factories import create_kinds, create_elements

create_kinds()
create_elements()
create_manifest()
