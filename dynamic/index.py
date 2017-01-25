from apphost import application

class Index(application.Application):
    pass


def main(**kwargs):
    return (Index().html(), [])