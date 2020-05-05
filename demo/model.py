class Demo:
    def __init__(self, section: str, name: str):
        self.section: str = section
        self.name: str = name
        self.view = f'{name.lower()}/view'
