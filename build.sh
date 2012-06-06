source /opt/bbndk-2.0.0/bbndk-env.sh

blackberry-pythonpackager -devMode -debugToken ~/debugtoken.bar -package BB-Py_Twitter.bar bar-descriptor.xml main.py bbpy_twitter/ PythonTwitter/__init__.py PythonTwitter/twitter.py cli.py assets/icon.png assets/background.png assets/titlebar.png assets/titlebar.sci assets/toolbutton.png assets/toolbutton.sci urllib/
