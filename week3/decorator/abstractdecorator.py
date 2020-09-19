from abc import ABC, abstractmethod


class Hero:
    """Represents main hero of ... game with positive/negative effects on it"""

    def __init__(self):
        """Initializes Hero with it's stats such as luck, agility and others"""
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1,  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    """Realises decorator pattern for effects that can be imposed on hero"""

    def __init__(self, base):
        super().__init__()
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        return self.base.get_stats()


class AbstractPositive(AbstractEffect):
    """Abstract decorator, represents positive effects that can be imposed
    on hero"""

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class Berserk(AbstractPositive):
    """Decorator that realizes positive berserk effect.

    Increases Strength, Endurance, Agility, luck by 7.
    Decreases Perception, Charisma, Intelligence by 3.
    Increases Health Points by 50.
    """

    def get_stats(self):
        stats_copy = self.base.get_stats()

        for stat_name in ("Strength", "Endurance", "Agility", "Luck"):
            stats_copy[stat_name] += 7
        for stat_name in ("Perception", "Charisma", "Intelligence"):
            stats_copy[stat_name] -= 3

        stats_copy["HP"] += 50

        return stats_copy

    def get_positive_effects(self):
        positive_effects_copy = self.base.get_positive_effects()
        positive_effects_copy.append("Berserk")

        return positive_effects_copy


class Blessing(AbstractPositive):
    """Decorator that realizes positive blessing effect.

    Increases all basic stats by 2.
    """

    def get_stats(self):
        stats_copy = self.base.get_stats()

        for stat_name in stats_copy.keys():
            if stat_name in ('HP', 'SP', 'MP'):
                continue
            stats_copy[stat_name] += 2

        return stats_copy

    def get_positive_effects(self):
        positive_effects_copy = self.base.get_positive_effects()
        positive_effects_copy.append("Blessing")

        return positive_effects_copy


class AbstractNegative(AbstractEffect):
    """Abstract decorator, represents negative effects that can be imposed
    on hero"""

    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Weakness(AbstractNegative):
    """Decorator that realizes negative weakness effect.

    Decreases stats: Strength, Endurance, Agility by 4.
    """

    def get_stats(self):
        stats_copy = self.base.get_stats()

        for stat_name in ("Strength", "Endurance", "Agility"):
            stats_copy[stat_name] -= 4

        return stats_copy

    def get_negative_effects(self):
        negative_effects_copy = self.base.get_negative_effects()
        negative_effects_copy.append("Weakness")

        return negative_effects_copy


class Curse(AbstractNegative):
    """Decorator that realizes negative curse effect.

    Decreases all stats by 2 except HP, MP, SP
    """

    def get_stats(self):
        stats_copy = self.base.get_stats()

        for stat_name in stats_copy.keys():
            if stat_name in ('HP', 'MP', 'SP'):
                continue
            stats_copy[stat_name] -= 2

        return stats_copy

    def get_negative_effects(self):
        negative_effects_copy = self.base.get_negative_effects()
        negative_effects_copy.append("Curse")

        return negative_effects_copy


class EvilEye(AbstractNegative):
    """Decorator that realizes negative evil eye effect

    Decreases Luck by 10
    """

    def get_stats(self):
        stats_copy = self.base.get_stats()
        stats_copy["Luck"] -= 10

        return stats_copy

    def get_negative_effects(self):
        negative_effects_copy = self.base.get_negative_effects()
        negative_effects_copy.append("EvilEye")

        return negative_effects_copy
