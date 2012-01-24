## About ##
This module allows, with the use of python decorators, to transparently select a render function for an HTTP request handler's result. It uses mimeparse to parse the HTTP Accept header and select the best available representation.

## Author ##
[Nicola Iarocci](mailto:nicola@nicolaiarocci.com)

## License ##
[MIT License](http://www.opensource.org/licenses/mit-license.php)

## Attribution ##
This is a Flask port from the excellent [mimerender](http://code.google.com/p/mimerender/) v0.2.3 by Martin Blech

## Usage ##
This is an example from the included src/example.py script:
	from flask import Flask, request, jsonify
	from mimerender_flask import mimerender

	from flask import Flask, request, jsonify
	from mimerender_flask import mimerender

	render_xml = lambda message: '<message>%s</message>' % message
	render_json = jsonify
	render_html = lambda message: '<html><body>%s</body></html>' % message
	render_txt = lambda message: message

	app = Flask(__name__)

	@app.route('/')
	@mimerender(
	    default = 'html',
	    html = render_html,
	    xml  = render_xml,
	    json = render_json,
	    txt  = render_txt
	)
	def index():
		if request.method == 'GET':
			return {'message': 'Hello, World!'}

	if __name__ == "__main__":
	    app.run(debug=True)