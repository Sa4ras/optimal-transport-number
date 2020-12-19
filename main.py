from flask import Flask, redirect, url_for, request, session, render_template, flash

app = Flask(__name__)
app.secret_key = 'development-key'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

