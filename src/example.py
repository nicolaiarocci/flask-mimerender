from flask import Flask, request, jsonify
from flaskmimerender import mimerender

render_xml = lambda message: '<message>%s</message>' % message
render_json = jsonify
render_html = lambda message: '<html><body>%s</body></html>' % message
render_txt = lambda message: message

app = Flask(__name__)


@app.route('/')
@mimerender(default='html',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt
            )
def index():
    if request.method == 'GET':
        return {'message': 'Hello, World!'}

if __name__ == "__main__":
    app.run(debug=True)
