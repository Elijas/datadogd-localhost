import cherrypy
import tracing
import config

tracing.start_all()


class RootServer:
    @cherrypy.expose
    def status(self):
        return 'OK'

    @cherrypy.expose
    def chat_responded(self):
        tracing.increment_metric(tracing.Metrics.RESPONDED_CHATS, 1)
        return 'OK'


if __name__ == '__main__':
    server_config = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 26778
    }

    cherrypy.config.update(server_config)
    cherrypy.quickstart(RootServer())
