#!/usr/bin/env python
import os
import sys

wd = os.path.join(os.path.dirname(sys.argv[0]), os.path.pardir)
sys.path.insert(0, os.path.abspath(wd))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings.development')

import django
django.setup()

from ropeelements.factories import create_kinds, create_elements

create_kinds()
create_elements()
