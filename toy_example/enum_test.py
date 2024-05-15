class Color():
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

    def getName(self):
        return self.name

tmp = "red"

if tmp == Color.RED:
    print("Hi", Color.RED)
