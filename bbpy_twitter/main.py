import sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide.QtOpenGL import *

from .Twitter import Twitter

class App(QObject):
    def run(self):
        QApplication.setGraphicsSystem('opengl')

        self.app = QApplication(sys.argv)
        
        format = QGLFormat.defaultFormat()
        format.setSampleBuffers(False)
        format.setSwapInterval(1)
        glWidget = QGLWidget(format)
        glWidget.setAutoFillBackground(False)

        v = QDeclarativeView()
        self.twitter = Twitter()
        self.twitter.consumerKey = 'XIeqUJ941sRdsuPfbnvcFg'
        self.twitter.consumerSecret = '3WibMeldSeLN1BfSpjmUzHd5FGWjlRgwsQqZwcKitA'
        rc = v.engine().rootContext()
        rc.setContextProperty("twitter", self.twitter)
        self.twitter.userTimelineUpdated.connect(self.addUserTimeline)
        self.twitter.friendsTimelineUpdated.connect(self.addFriendsTimeline)

        v.setViewport(glWidget)
        v.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        v.setSource(QUrl.fromLocalFile('bbpy_twitter/main.qml'))
        v.show()

        self.root = v.rootObject()

        # Enter Qt application main loop
        sys.exit(self.app.exec_())

    def addUserTimeline(self):
        for s in self.twitter.UserTimeline._items:
            self.root.addUserElement(s)

    def addFriendsTimeline(self):
        for s in self.twitter.FriendsTimeline._items:
            self.root.addFriendsElement(s)

def main():
    try:
        global app
        app = App()
        app.run()
    finally:
        sys.stdout.flush()
        sys.stderr.flush()

if __name__ == '__main__':
    main()
