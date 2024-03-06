#!/usr/bin/env python

import os
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent / "src"))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
