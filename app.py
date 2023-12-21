from flask import Flask, render_template
from game import Game

app = Flask(__name__)
g = Game()
teamOneName = 'Team A'
teamTwoName = 'Team B'

@app.route('/')
def index():
    g.reloadGame()
    return "Game loaded"

@app.route('/host/')
def host():
    return render_template('host.html')

@app.route('/no/<name>')
def renameOne(name):
    global teamOneName
    teamOneName = name
    return 'successfully renamed teamOne to ' + teamOneName

@app.route('/nt/<name>')
def reNameTwo(name):
    global teamTwoName
    teamTwoName = name
    return 'successfully renamed teamOne to ' + teamTwoName

@app.route('/gamestate/')
def gameState():
    return g.audienceState()

@app.route('/game/')
def game():
    print(teamOneName)
    print(teamTwoName)
    return render_template('game.html', teamOneName=teamOneName, teamTwoName=teamTwoName)

@app.route('/test/')
def test():
    return g.revealAnswer(0)

if __name__ == '__main__':
    app.run(debug=True)




