import flask

import lemsplc_parser


app = flask.Flask(__name__)


@app.route('/')
def index():
    articles = sorted(lemsplc_parser.front_page(), key=lambda a: -a.comments)
    return flask.render_template('index.html', articles=articles)
