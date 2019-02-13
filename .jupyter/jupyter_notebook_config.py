try:
    import os
    import json
    import traceback
    import IPython.lib
    import pgcontents
    from pgcontents.pgmanager import PostgresContentsManager
    from pgcontents.hybridmanager import HybridContentsManager
    from IPython.html.services.contents.filemanager import FileContentsManager


    c = get_config()

    ### Password protection ###
    # http://jupyter-notebook.readthedocs.io/en/latest/security.html
    if os.environ.get('JUPYTER_NOTEBOOK_PASSWORD_DISABLED') != 'DangerZone!':
        passwd = os.environ['JUPYTER_NOTEBOOK_PASSWORD']
        c.NotebookApp.password = IPython.lib.passwd(passwd)
    else:
        c.NotebookApp.token = ''
        c.NotebookApp.password = ''

    ### PostresContentsManager ###
    database_url = os.getenv('DATABASE_URL', None)
    if database_url:
        c.NotebookApp.contents_manager_class = HybridContentsManager
        c.HybridContentsManager.manager_classes = {
            # Associate the root directory with a PostgresContentsManager.
            # This manager will receive all requests that don't fall under any of the
            # other managers.
            '': PostgresContentsManager,
            # Associate /directory with a FileContentsManager.
            'notebooks': FileContentsManager,
        }
        c.HybridContentsManager.manager_kwargs = {
            # Args for root PostgresContentsManager.
            '': {
                'db_url': database_url,
                'user_id': 'heroku',
            },
            # Args for the FileContentsManager mapped to /directory
            'directory': {
                'root_dir': '/app',
            }
        }
except Exception:
    traceback.print_exc()
    # if an exception occues, notebook normally would get started
    # without password set. For security reasons, execution is stopped.
    exit(-1)
