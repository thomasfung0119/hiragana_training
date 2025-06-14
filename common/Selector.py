import random

class BiasedRandomSelector:
    selected_char = None
    def __init__(self, items):
        self.items = list(items)
        self.selection_counts = {item: 0 for item in self.items}

    def random_hiragana(self):
        # Normalize probabilities
        probabilities = [1 / (self.selection_counts[item] + 1) for item in self.items]
        total_probability = sum(probabilities)
        normalized_probabilities = [p / total_probability for p in probabilities]

        # Choose an item based on the calculated probabilities
        self.selected_item = random.choices(self.items, weights=normalized_probabilities, k=1)[0]
        self.selection_counts[self.selected_item] += 1
        
        return self.selected_item