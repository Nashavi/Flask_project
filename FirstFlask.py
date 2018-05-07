from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask'

# @app.route('/hello')
# def hello():
#     return 'Hello World'

@app.route('/hello/<name>')
def hello(name):
    return 'Hello World'

@app.route('/double/<int:num>')
def double(num):
    return '%d'%(2*num)


if __name__ == '__main__':
    app.run(debug=True)