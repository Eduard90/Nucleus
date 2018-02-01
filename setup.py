from setuptools import setup

setup(name='Nucleus',
      version='0.1',
      description='Nucleus - core for webapp on Sanic+Gino',
      author='Eduard90',
      author_email='ytko90@gmail.com',
      license='GPL2',
      install_requires=[
          'sanic', 'sanic-jwt', 'gino', 'alembic', 'click', 'psycopg2', 'pytest'
      ],
      extras_require={
          'kafka': ['aiokafka']
      },
      packages=['nucleus', 'nucleus.boilerplate', 'nucleus.boilerplate.migrations',
                'nucleus.boilerplate.migrations.versions', 'nucleus.commands', 'nucleus.conf',
                'nucleus.system', 'nucleus.tests', 'nucleus.utils', 'nucleus.urls', 'nucleus.exceptions',
                'nucleus.kafka'],
      scripts=['bin/nucleus'],
      include_package_data=True,
      zip_safe=False)
