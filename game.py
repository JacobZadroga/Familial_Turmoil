import json
from classes import BoardAnswer, BoardQuestion

class Game:
    def __init__(self):
        self.teamOneScore = 0
        self.teamOneX = 0
        self.teamTwoScore = 0
        self.teamTwoX = 0
        self.bank = 0
        self.currentQuestion = 0
        self.questions = []
        self.audienceAnswerList = []

    def reloadGame(self):
        print("RELOADING GAME STATE")
        self.teamOneScore = 0
        self.teamOneX = 0
        self.teamTwoScore = 0
        self.teamTwoX = 0
        self.bank = 0
        self.currentQuestion = 0
        self.questions = self.readFromQuestions()
        self.audienceAnswerList = []

        self.calcAudienceAnswerList()

    def readFromQuestions(self):
        f = open("./data/questions.json", "r")
        jsonStr = f.read()
        jsonObj = json.loads(jsonStr)
        questions = []
        for question in jsonObj:
            ans = []
            for answer in question['answers']:
                ans.append(BoardAnswer(answer['answer'],answer['total']))
            questions.append(BoardQuestion(question['question'],ans))
        return questions

    def calcAudienceAnswerList(self):
        print(self.questions)
        lst = []
        for ans in self.questions[self.currentQuestion].boardAnswers:
            if ans.exposed:
                lst.append({
                    'answer': ans.answer,
                    'count': ans.count
                })
            else:
                lst.append({
                    'answer': None,
                    'count': 0
                })
        self.audienceAnswerList = lst

    def calcHostAnswerList(self):
        print(self.questions)
        lst = []
        for ans in self.questions[self.currentQuestion].boardAnswers:
            lst.append({
                'exposed': ans.exposed,
                'answer': ans.answer,
                'count': ans.count
            })
        return lst

    def revealAnswer(self, answerNum):
        if(int(answerNum) >= len(self.questions[self.currentQuestion].boardAnswers)):
            return
        ans = self.questions[self.currentQuestion].boardAnswers[int(answerNum)]
        if not ans.exposed:
            ans.exposed = True
            self.bank = self.bank + ans.count
            self.calcAudienceAnswerList()

    def addBankToTeamScore(self, team):
        if(int(team) == 0):
            self.teamOneScore += self.bank
        else:
            self.teamTwoScore += self.bank
        self.bank = 0
        self.teamTwoX = 0
        self.teamOneX = 0
        return json.dumps({
            'teamOneScore': self.teamOneScore,
            'teamTwoScore': self.teamTwoScore,
            'bank': self.bank
        })

    def changeTeamScore(self, team, score):
        if(int(team) == 0):
            self.teamOneScore = score
        else:
            self.teamTwoScore = score
        return json.dumps({
            'teamOneScore': self.teamOneScore,
            'teamTwoScore': self.teamTwoScore
        })


    def changeTeamX(self, team, add):
        if(int(team) == 0):
            if((add > 0 and self.teamOneX < 3) or (add < 0 and self.teamOneX > 0)):
                self.teamOneX += add
        else:
            if((add > 0 and self.teamTwoX < 3) or (add < 0 and self.teamTwoX > 0)):
                self.teamTwoX += add
        return json.dumps({
            'teamOneX': self.teamOneX,
            'teamTwoX': self.teamTwoX
        })


    def progressQuestion(self):
        if(self.currentQuestion < len(self.questions)-1):
            self.bank = 0
            self.currentQuestion += 1
            self.calcAudienceAnswerList()

    def regressQuestion(self):
        if(self.currentQuestion > 0):
            self.currentQuestion -= 1
            self.calcAudienceAnswerList()


    def setBank(self, bank):
        self.bank = int(bank);
        return json.dumps({
            'bank': self.bank
        })

    def audienceState(self):
        gameMap = {
            'teamOneScore': self.teamOneScore,
            'teamOneX': self.teamOneX,
            'teamTwoScore': self.teamTwoScore,
            'teamTwoX': self.teamTwoX,
            'bank': self.bank,
            'answers': self.audienceAnswerList
        }
        return json.dumps(gameMap)

    def hostState(self):
        gameMap = {
            'teamOneScore': self.teamOneScore,
            'teamOneX': self.teamOneX,
            'teamTwoScore': self.teamTwoScore,
            'teamTwoX': self.teamTwoX,
            'bank': self.bank,
            'question': self.questions[self.currentQuestion].question,
            'answers': self.calcHostAnswerList()
        }
        return json.dumps(gameMap)
