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

    def revealAnswer(self, answerNum):
        ans = self.questions[self.currentQuestion].boardAnswers[answerNum]
        if not ans.exposed:
            ans.exposed = True
            self.bank = self.bank + ans.count
            self.calcAudienceAnswerList()

    def addBankToTeamScore(self, team):
        if(team == 1):
            self.teamOneScore += self.bank
        else:
            self.teamTwoScore += self.bank
        self.bank = 0;

    def progressQuestion(self):
        self.currentQuestion += 1
        self.calcAudienceAnswerList()

    def audienceState(self):
        gameMap = {
            'teamOneScore': self.teamOneScore,
            'teamOneX': self.teamOneX,
            'teamTwoScore': self.teamTwoScore,
            'teamTwoX': self.teamTwoX,
            'bank': self.bank,
            'question': self.questions[self.currentQuestion].question,
            'answers': self.audienceAnswerList
        }
        return json.dumps(gameMap)
