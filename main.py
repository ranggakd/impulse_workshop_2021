from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def landing_page():
    return render_template('main.html')

@app.route('/service1')
def get_result_API1():
    return render_template('result.html')

@app.route('/service2')
def get_result_API2():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)