class BoardAnswer:
    def __init__(self, answer, count):
        self.answer = answer
        self.count = count
        self.exposed = False

    def __str__(self):
        return '{Answer: ' + self.answer + ', Count: ' + str(self.count) + ', Exposed: ' + str(self.exposed) + '}'

    def __repr__(self):
        return self.__str__()

class BoardQuestion:
    def __init__(self, question, boardAnswers):
        self.question = question
        self.boardAnswers = boardAnswers

    def __str__(self):
        return '{Question: ' + self.question + ",\nAnswers: " + str(self.boardAnswers)

    def __repr__(self):
        return self.__str__()
