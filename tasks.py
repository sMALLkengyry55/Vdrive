import os
import time
from collections import namedtuple

from invoke import task, run, exceptions


DUMP_PATH = ''  # TODO: fix it


def local(command, **kwargs):
    kwargs.update({'pty': True})
    return run(command, **kwargs)


def recreate_db():
    from django.conf import settings
    db_name = settings.DATABASES.get('default').get('NAME')
    local('dropdb -U postgres -h db --if-exists {0}'.format(db_name))
    local('createdb -U postgres -h db {0}'.format(db_name))
    local('cat {0} | psql -h db -U postgres {1}'.format(DUMP_PATH, db_name))


def get_env_vars():
    Env = namedtuple('Env', [
        'ENV',
        'PY_AUTORELOAD',
        'RECREATE_DB',
        'BASICAUTH'
    ])
    return Env(*[os.getenv(var, None) for var in Env._fields])


@task
def run_it(ctx):
    """
    Set env PGPASSWORD and DJANGO_SETTINGS_MODULE.
    """
    env = get_env_vars()

    # Wait till postgres is up
    while True:
        try:
            if env.RECREATE_DB and os.path.isfile('./{0}'.format(DUMP_PATH)):
                recreate_db()
            local('./manage.py migrate')
            # Create superuser for dev env
            if env.ENV == 'dev':
                local('./manage.py create_dev_superuser')
            break
        except exceptions.Failure:
            time.sleep(1)

    local('./manage.py collectstatic --noinput')
    local('./manage.py compilemessages')

    # settings for 1 core. If you need to scale the project, do it via docker interface
    cmd = ('uwsgi --http 0.0.0.0:9001 --master '
           '--module "django.core.wsgi:get_wsgi_application()" '
           '--processes 1 '
           '--offload-threads 2 '
           '--enable-threads')
    if env.PY_AUTORELOAD:
        cmd += ' --py-autoreload 1'
    if env.BASICAUTH:
        cmd += ' --route "^/ basicauth:SR,{0}"'.format(env.BASICAUTH)
    if env.ENV == 'dev':
        cmd += ' --honour-stdin'
    if not env.ENV == 'dev':
        cmd += ' --harakiri 30'
    local(cmd)
