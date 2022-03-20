from sanic import Sanic

app = Sanic('treehole')
app.config['MODE'] = MODE = app.config.get('MODE', 'dev')
app.config['DEBUG'] = (app.config['MODE'] != 'production')
