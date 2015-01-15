"""Custom static file finders."""
from fnmatch import fnmatch

from django.conf import settings
from django.contrib.staticfiles import finders


class FileSystemFinder(finders.FileSystemFinder):

    def list(self, ignore_patterns):
        """List only files matching glob patterns defined by
        ``COLLECT_STATIC_FILES`` setting.
        """
        iterator = super(FileSystemFinder, self).list(ignore_patterns)
        for path, storage in iterator:
            for pattern in settings.COLLECT_STATIC_FILES:
                if fnmatch(path, pattern):
                    yield path, storage


class AppDirectoriesFinder(finders.AppDirectoriesFinder):

    def list(self, ignore_patterns):
        """List only files matching glob patterns defined by
        ``COLLECT_STATIC_APP_FILES`` setting.
        """
        iterator = super(AppDirectoriesFinder, self).list(ignore_patterns)
        for path, storage in iterator:
            for pattern in settings.COLLECT_STATIC_APP_FILES:
                if fnmatch(path, pattern):
                    yield path, storage
