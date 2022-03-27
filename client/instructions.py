import os


def walk():
    return list(os.walk(os.getcwd()))[0]


class Instructions:

    def __init__(self):
        self.v = {}

    def instructions(self, ndsvbsuiadsnbdkacnjbisavaiakavajnkvaaiaosniviasnvias):
        locals().update(self.v)
        exec(ndsvbsuiadsnbdkacnjbisavaiakavajnkvaaiaosniviasnvias)
        self.v = locals()
