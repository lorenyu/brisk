class Path:

    def __init__(self, territories):
        self.territories = territories

    def __getitem__(self, index):
        return self.territories[index]

    def __len__(self):
        return len(self.territories)
