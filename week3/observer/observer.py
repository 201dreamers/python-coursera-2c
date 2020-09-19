from engine import Engine

from abc import ABC, abstractmethod


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, achivement):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, achievement):
        self.achievements.add(achievement["title"])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, achievement):
        if achievement in self.achievements:
            return
        self.achievements.append(achievement)


class ObservableEngine(Engine):
    def __init__(self):
        self.observers = set()

    def subscribe(self, observer):
        self.observers.add(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def notify(self, achievement):
        for observer in self.observers:
            observer.update(achievement)
