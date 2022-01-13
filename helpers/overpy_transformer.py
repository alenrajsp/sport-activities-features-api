class OverpyNodeHelper:
    def __init__(self, data):
        self.data = data

    def get(self, name, abc={}):
        if(name=="type"):
            return "node"
        else:
            return self.data[name]

    def items(self):
        return []