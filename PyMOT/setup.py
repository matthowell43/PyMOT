# py2exe

from distutils.core import setup

setup(
        windows=['core.py', 'analysis.py', 'gui.py', 'apigui.py', 'graphics.py'],
        options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
                        "excludes": ["email"]
                }
        }
)