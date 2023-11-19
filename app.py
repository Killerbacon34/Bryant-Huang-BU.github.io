from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def post():
    return "recived: {}".format(request.form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


@app.route('/home')
def search_page():
    return "Will add search here:"


app.run(debug=True)
