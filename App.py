import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from services.HandlingDataBase import get_vote_cards, update_google_sheet
from utils.utils import get_ip_address, voting
from waitress import serve

load_dotenv()
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = os.environ.get('SECRET_KEY')

@app.errorhandler(404)
def page_not_found(e):

    return render_template('./pages/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):

    return render_template('./pages/500.html'), 500

@app.route('/votecard/<vote>/<index>', methods=['GET','POST'])
def votingpage(vote:str, index:str):
    id = int(index)
    votecards_list = get_vote_cards()
    try: 
        session[f"has_{get_ip_address()}_voted_in_{id}"]
        return redirect('/')
    except KeyError:
        session[f"has_{get_ip_address()}_voted_in_{id}"] = True
        for votecard in votecards_list:
            if votecard.index == id:
                voting(votecard, vote)
                update_google_sheet(
                        ['Índices','Livros','Pontuação','Imagens'], 
                        [[vc.index,vc.title, vc.score, vc.image] 
                         for vc in votecards_list])
                return redirect('/')
        return redirect('/')

@app.route('/', methods=['GET','POST'])
def index() -> str:

    votecards_list = get_vote_cards()
    return render_template('./pages/index.html', 
                           ip_address = get_ip_address(),
                           votecards = votecards_list)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80)
