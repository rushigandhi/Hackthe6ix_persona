from flask import Flask, render_template, request, url_for, redirect, session, Session
import main as m

app = Flask(__name__)


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        data = m.get_all_tweets(text)
        all_tweets = data[0]
        analysis_data = data[1]
        return render_template('index.html', form=request.form, user_handle=text, loading_status="", tweets=all_tweets,
                               analysis = analysis_data)
    return render_template("index.html", user_handle="twitter-handle")

if __name__ == "__main__":
    app.secret_key = "TRIAL"
    app.debug = True
    app.run()
