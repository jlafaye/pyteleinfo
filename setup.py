from distutils.core import setup

setup(name='Teleinfo',
      version='1.0',
      description='Teleinfo tools',
      author='Julien Lafaye',
      packages=['teleinfo'],
      package_dir={'': 'packages'},
      entry_points={
          'console_scripts': [
              'teleinfo-daemon = teleinfo.daemon:run_daemon'
          ]
      }
)
