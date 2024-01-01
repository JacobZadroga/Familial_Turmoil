from flask import Flask, render_template, request
from game import Game

# EB looks for an 'application' callable by default.
application = Flask(__name__)
g = Game()
g.reloadGame()
teamNames = ['teamOne', 'teamTwo']
buzzin = -1

@application.route('/')
def index():
    return "Game loaded"

@application.route('/host/')
def host():
    return render_template('host.html')

@application.route('/cBuzzIn/')
def cBuzzIn():
    team = request.args.get('t')
    if(team != None):
        return render_template('buzzin.html', team=team)
    else:
        return "pass team"

@application.route('/hostBuzzIn/')
def buzzInControlls():
    return render_template('buzzInHost.html')

@application.route('/teamName')
def renameOne():
    global teamNames
    team = request.args.get('team')
    name = request.args.get('name')
    if(name != None and (team == '0' or team == '1')):
        teamNames[int(team)] = name
        return 'successfully renamed team ' + team + ' to ' + teamNames[int(team)]
    else:
        return 'No name or team supplied'

@application.route('/reload')
def reload():
    g.reloadGame()
    return "reloaded Game"

@application.route('/buzzInMethod')
def buzzInMethod():
    global buzzin
    team = request.args.get('t')
    if(team != None):
        if(buzzin == -1):
            buzzin = team;
        else:
            return "too late"
    else:
        return "no team supplied"

@application.route('/resetBuzz')
def resetBuzz():
    global buzzin
    buzzin = -1
    return "success"

@application.route('/curBuzz')
def curBuzz():
    global buzzin
    return str(buzzin)


@application.route('/gamestate/')
def gameState():
    return g.audienceState()

@application.route('/hoststate/')
def hostState():
    return g.hostState()

@application.route('/game/')
def game():
    global teamNames
    return render_template('game.html', teamOneName=teamNames[0], teamTwoName=teamNames[1])

@application.route('/revealAnswer')
def revealAnswer():
    answer = request.args.get('a')
    if(answer != None):
        g.revealAnswer(int(answer))
        return "success"
    else:
        return "failed to reveal answer " + answer

@application.route('/addBankToScore')
def addBankToTeamScore():
    team = request.args.get('team')
    if(team != None):
        return g.addBankToTeamScore(int(team))
    else:
        return "ERROR"

@application.route('/setBank')
def setBank():
    bank = request.args.get('bank')
    if(bank != None):
        return g.setBank(bank)
    else:
        return "ERROR"

@application.route('/setTeamScore')
def setTeamScore():
    team = request.args.get('team')
    score = request.args.get('score')
    if(score != None and (team == '0' or team == '1')):
        g.changeTeamScore(int(team), int(score))
        return 'successfully set team ' + team + '\'s score to ' + score
    else:
        return 'No score or team supplied'

@application.route('/addX')
def addX():
    team = request.args.get('team')
    type = request.args.get('type')
    print(team + " | " + type)
    if(team != None and (type == 'add' or type == 'subtract')):
        if(type == 'add'):
            g.changeTeamX(int(team), 1)
        else:
            g.changeTeamX(int(team), -1)
        return "success"
    else:
        return "Team or type not supplied"

@application.route('/progressQ')
def progressQ():
    g.progressQuestion()
    return "success"

@application.route('/regressQ')
def regressQ():
    g.regressQuestion()
    return "success"

# run the app.
if __name__ == "__main__":
    application.run()
