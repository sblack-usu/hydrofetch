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
        filePath = (self.get_argument('filepath', None)
        app = self.get_argument('app', app_env)

        if filePath:
            path = filePath
        elif app.lower() == 'lab':
            path = 'lab/tree'
        else:
            path = 'tree'
        messages = []
        try:
            downloads = self.get_query_arguments('download')
            for download in downloads:
                try:
                    r = requests.get(download)
                    filename = r.url.split("/")[-1]
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                except:
                    messages.append("Failed to download file {}".format(r.url.split("/")[-1]))

            unpacks = self.get_query_arguments("unpack")
            for download in unpacks:
                try:
                    r = requests.get(download)
                except:
                    messages.append("Failed to download file {}".format(filename))

                filename = r.url.split("/")[-1]
                with open(filename, 'wb') as f:
                    f.write(r.content)
                unpacked = False
                try:
                    shutil.unpack_archive(filename)
                    unpacked = True
                except:
                    messages.append("Failed to unpack file {}".format(filename))
                if unpacked:
                    os.remove(filename)


        except Exception as e:
            messages.append(str(e))

        if len(messages) > 0:
            with open("launch_notes.txt", 'w') as f:
                for message in messages:
                    f.write(message)

        self.redirect(path)
