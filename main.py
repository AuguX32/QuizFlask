from flask import Flask, render_template, request, session, redirect # type: ignore
from questions import questions # type: ignore
from random import choice
from os import urandom
from resultat import resultats, noms

app = Flask(__name__)

app.secret_key = urandom(32)

@app.route('/')
def index () :
    session["numero_question"] = 0

    session["score"] = {"J":0, "R":0, "D":0, "G":0, "W":0}

    return render_template("index.html")


@app.route('/question')
def question():
    
    global question

    numero = session["numero_question"]
    
    if numero < len(questions):
            énoncé_question = questions[numero]["enonce"]

            symboles_et_reponses = questions[numero].copy()

            symboles_et_reponses.pop("enonce")
        
            reponses = list(symboles_et_reponses.values())

            symboles = list(symboles_et_reponses.keys())

            session["symboles"] = symboles
    
            return render_template("questions.html", enonce = énoncé_question, reponses = reponses, symboles = symboles)
    else :
         
         score_tries = sorted(session["score"], key = session["score"].get, reverse = True)

         gagnant = score_tries[0]

         nom_gagnant = noms[gagnant]

         resultat_description = resultats[gagnant]

         return render_template("resultats.html", resultat_description = resultat_description, nom_gagnant = nom_gagnant)
    
    

@app.route('/reponse/<numero>')
def reponse(numero):
     
     symbole = session["symboles"][int(numero)] 


     session["score"][symbole] += 1 # type: ignore

     session["numero_question"] +=1

     return redirect("/question")

     















app.run(host='0.0.0.0', port=81)