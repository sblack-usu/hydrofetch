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
        messages = []
        try:
            downloads = self.get_query_arguments('download')
            unpacks = self.get_query_arguments("unpack")
            downloads = downloads + unpacks
            for download in downloads:
                try:
                    r = requests.get(download)
                    with open(download.split("/")[-1], 'wb') as f:
                        f.write(r.content)
                except:
                    messages.append("Failed to download file {}".format(download.split("/")[-1]))

            for archive in unpacks:
                try:
                    shutil.unpack_archive(archive.split("/")[-1])
                except:
                    messages.append("Failed to unpack file {}".format(archive.split("/")[-1]))
        except Exception as e:
            messages.append(str(e))

        if len(messages) > 0:
            with open("launch_notes.txt", 'w') as f:
                for message in messages:
                    f.write(message)

        self.redirect(path)