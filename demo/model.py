"""Demo view model"""


class Demo:
    """View model for demo item"""
    def __init__(self, section: str, name: str, view: str = None):
        self.section: str = section
        self.name: str = name
        self.view = view if view else f'{name.lower()}/view'
