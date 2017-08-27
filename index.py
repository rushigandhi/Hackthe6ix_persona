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
        final_tweet_data = []
        data = m.get_all_tweets(text)

        for tweet in data:
            final_tweet_data.append(list(tweet.split("*")))

        print data
        return render_template('index.html', form=request.form, data=final_tweet_data, user_handle=text)
    return render_template("index.html", user_handle="")

if __name__ == "__main__":
    app.secret_key = "TRIAL"
    app.debug = True
    app.run()
