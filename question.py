class Question:
    def __init__(self):
        self.question = ""
        self.answers = {}
        self.num_answers = 0

    def __str__(self):
        result = f"\n{self.question}\nAnswers:"
        for key, value in self.answers.items():
            result += f"\n{key}: {value}"
        return result