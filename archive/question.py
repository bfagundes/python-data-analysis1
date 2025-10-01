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
    
    def sort_answers(self):
        """
        Sorts the answers by the answer_count, descending
        """
        self.answers = dict(sorted(self.answers.items(), key=lambda item: item[1], reverse=True))

    def get_answers(self, threshold = 0, label = "Others"):
        """
        Returns a dictionary of answers sorted by value, with an optional threshold.

        If the number of answers exceeds the threshold, the remaining values are summed 
        and labeled under the specified category.

        Args:
            threshold (int, optional): The maximum number of individual answers to return. 
                                       Defaults to 0 (returns all answers).
            label (str, optional): The label for grouped remaining answers. Defaults to "Others".

        Returns:
            dict: A dictionary containing the top answers and a summed "Others" category if applicable.
        """
        self.sort_answers()

        if threshold <= 0 or len(self.answers) <= threshold:
            return self.answers
        
        else:
            threshold_items = list(self.answers.items())[:threshold]
            remaining_items_sum = sum(value for _, value in list(self.answers.items())[threshold:])
            threshold_items.append((label, remaining_items_sum))
            return dict(threshold_items)