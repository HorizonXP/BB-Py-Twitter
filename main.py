import os
import sys

if __name__ == '__main__':
    # add "-arg -shared" to pythonpackager command to run from shared
    if '-shared' in sys.argv:
        ENVDIR = 'shared/misc'
    else:
        ENVDIR = os.path.dirname(__file__)

    # launch telnet-based command line interface (CLI)
    try:
        import cli
    except ImportError:
        pass
    else:
        import threading
        t = threading.Thread(target=cli.run)
        t.daemon = True
        t.start()

    BBPY = os.path.join(ENVDIR, 'blackberry-py')
    sys.path.append(BBPY)

    os.environ['LD_LIBRARY_PATH'] = os.path.join(BBPY, 'lib')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(BBPY, 'plugins/platforms')
    os.environ['QT_QPA_PLATFORM'] = 'blackberry'
    os.environ['QML_IMPORT_PATH'] = os.path.join(BBPY, 'imports')
    os.environ['QT_PLUGIN_PATH'] = os.path.join(BBPY, 'plugins')

    from bbpy_twitter.main import main
    main()

