from tornado import (
    gen,
    web,
)

from notebook.base.handlers import IPythonHandler
import os
import requests
import shutil


class UIHandler(IPythonHandler):
    @web.authenticated
    @gen.coroutine
    def get(self):
        app_env = os.getenv('URLPARAMS_APP', default='notebook')
        urlPath = (self.get_argument('urlpath', None) or
                   self.get_argument('urlPath', None))
        app = self.get_argument('app', app_env)

        if urlPath:
            path = urlPath
        elif app.lower() == 'lab':
            path = 'lab/tree'
        else:
            path = 'tree'

        downloads = self.get_query_arguments('download')
        unpacks = self.get_query_arguments("unpack")
        downloads.append(unpacks)
        for download in downloads:
            r = requests.get(download)
            with open(download.split("/")[-1], 'wb') as f:
                f.write(r.content)

        for archive in unpacks:
            shutil.unpack_archive(archive.split("/")[-1])

        self.redirect(path)