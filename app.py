from flask import Flask, render_template

app = Flask(__name__)
teamOneName = 'Team A'
teamOneScore = 0

teamTwoName = 'Team B'
teamTwoScore = 0


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/host/')
def host():
    teamOneName = 'Hail Mary Hussars'
    teamTwoName = 'Skynet'
    return render_template('host.html')

@app.route('/game/')
def game():
    return render_template('game.html', teamOneName=teamOneName, teamTwoName=teamTwoName)

if __name__ == '__main__':
    app.run(debug=True)
