from setuptools import setup, find_packages

setup(
  name = 'radox',
  packages = find_packages(),
  version = '0.0.4',
  description = 'A WSGI based Python web framework inspired from flask',
  author = 'Palani',
  author_email = 'palanioffcl@gmail.com',
  install_requires=['wsgiref'],
  keywords = ['web', 'python', 'framework', 'libraries', 'webapps'],
  classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP"
    ]
)
