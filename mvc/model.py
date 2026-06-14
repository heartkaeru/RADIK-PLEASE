import random
import re
from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional, Tuple, Union

import config


class ShuffleBag:
    """
    Класс для реализации алгоритма "Shuffle Bag" ("Мешок с номерками").
    Суть: мы кладем в "мешок" все возможные варианты (например, типы ошибок в документах).
    И достаем их по одному. Так мы гарантируем, что пока не достанем все разные ошибки,
    они не начнут повторяться. Это делает рандом менее "раздражающим" для игрока.
    """
    def __init__(self, items, random_source=None):
        if len(items) == 0:
            raise ValueError("ShuffleBag не может быть пустым")

        self.items = list(items)
        self.random = random_source or random.Random()
        self.bag = []

    def get(self):
        if len(self.bag) == 0:
            self.bag = self.items.copy()
            self.shuffle(self.bag)

        return self.bag.pop()

    def shuffle(self, items):
        for i in range(len(items) - 1, 0, -1):
            j = self.random.randint(0, i)
            items[i], items[j] = items[j], items[i]


class PseudoRandomChance:
    """
    Реализует механизм псевдорандомного распределения (Pseudo-Random Distribution).
    Часто используется в играх (например, криты в Dota 2).
    Идея: изначально шанс события мал, но с каждой неудачной попыткой шанс увеличивается.
    Как только событие происходит, шанс сбрасывается обратно.
    Так мы избегаем ситуаций, когда игроку 10 раз подряд "не везет".
    """
    def __init__(self, base_chance, step, max_chance, random_source=None):
        self.base_chance = base_chance
        self.step = step
        self.max_chance = max_chance
        self.random = random_source or random.Random()
        self.current_chance = base_chance

    def roll(self):
        if self.random.random() < self.current_chance:
            self.current_chance = self.base_chance
            return True

        self.current_chance += self.step
        if self.current_chance > self.max_chance:
            self.current_chance = self.max_chance

        return False


def weighted_choice(variants, random_source):
    if isinstance(variants, dict):
        variants = list(variants.items())

    total_weight = 0
    for item, weight in variants:
        total_weight += weight

    roll = random_source.uniform(0, total_weight)
    current_weight = 0

    for item, weight in variants:
        current_weight += weight
        if roll <= current_weight:
            return item

    return variants[-1][0]


class GeneticDayPlanner:
    """
    Генетический алгоритм для планирования дня.
    Создает последовательность: кто придет следующим (True - нарушитель, False - нормальный).
    Использует эволюцию: создает кучу случайных планов, выбирает лучшие (где нарушители
    распределены равномерно, нет долгих серий из одних нарушителей), "скрещивает" их
    и получает идеальный план на день.
    """
    def __init__(
        self,
        visitors_count,
        min_bad_visitors,
        max_bad_visitors,
        population_size,
        generations,
        mutation_chance,
        random_source=None,
    ):
        self.visitors_count = visitors_count
        self.min_bad_visitors = min_bad_visitors
        self.max_bad_visitors = max_bad_visitors
        self.population_size = population_size
        self.generations = generations
        self.mutation_chance = mutation_chance
        self.random = random_source or random.Random()

    def make_plan(self, day_number):
        visitor_count = self.visitors_count
        target_bad = self.get_target_bad_count(day_number, visitor_count)
        population = []

        for _ in range(self.population_size):
            population.append(self.make_random_plan(visitor_count))

        for _ in range(self.generations):
            population.sort(key=lambda plan: self.score_plan(plan, target_bad))
            survivors = population[: max(2, self.population_size // 4)]
            new_population = survivors.copy()

            while len(new_population) < self.population_size:
                parent_a = self.random.choice(survivors)
                parent_b = self.random.choice(survivors)
                child = self.cross(parent_a, parent_b)
                self.mutate(child)
                new_population.append(child)

            population = new_population

        population.sort(key=lambda plan: self.score_plan(plan, target_bad))
        return population[0]

    def get_target_bad_count(self, day_number, visitor_count):
        target = self.min_bad_visitors + day_number - 1

        if target > self.max_bad_visitors:
            target = self.max_bad_visitors
        if target > visitor_count:
            target = visitor_count

        return target

    def make_random_plan(self, visitor_count):
        plan = []

        for _ in range(visitor_count):
            plan.append(self.random.choice((True, False)))

        return plan

    def score_plan(self, plan, target_bad):
        bad_count = 0
        streak_penalty = 0
        last_value = None
        streak = 0

        for value in plan:
            if value:
                bad_count += 1

            if value == last_value:
                streak += 1
            else:
                streak = 1
                last_value = value

            if streak > 2:
                streak_penalty += streak

        return abs(bad_count - target_bad) * 10 + streak_penalty

    def cross(self, parent_a, parent_b):
        if len(parent_a) < 2:
            return parent_a.copy()

        cut = self.random.randint(1, len(parent_a) - 1)
        return parent_a[:cut] + parent_b[cut:]

    def mutate(self, plan):
        for i in range(len(plan)):
            if self.random.random() < self.mutation_chance:
                plan[i] = not plan[i]


def display_date(value: Optional[date]) -> str:
    if value is None:
        return config.NO_DATE_TEXT

    return value.strftime(config.DATE_FORMAT)


def get_active_checks(day_number: int) -> Tuple[str, ...]:
    if day_number in config.CHECKS_BY_DAY:
        return config.CHECKS_BY_DAY[day_number]

    return config.ALL_CHECKS


def get_error_reasons_for_checks(
    active_checks: Tuple[str, ...],
) -> Tuple[str, ...]:
    reasons = []

    for check_name in active_checks:
        for reason in config.CHECK_ERROR_REASONS[check_name]:
            reasons.append(reason)

    return tuple(reasons)


def date_to_save(value: Optional[date]) -> Optional[str]:
    if value is None:
        return None

    return value.strftime(config.DATE_FORMAT)


def date_from_save(value) -> Optional[date]:
    if not isinstance(value, str):
        return None

    try:
        return datetime.strptime(value, config.DATE_FORMAT).date()
    except ValueError:
        return None


class Decision(Enum):
    ALLOW = config.DECISION_ALLOW
    DENY = config.DECISION_DENY


class GameRules:
    """
    Хранит правила игры (какие формы обучения валидны, какие года рождения разрешены).
    Также умеет генерировать тексты инструкций для книги на столе, в зависимости от того,
    какой сейчас игровой день.
    """
    def __init__(
        self,
        max_valid_birth_year: int = config.MAX_VALID_BIRTH_YEAR,
        group_pattern: str = config.GROUP_PATTERN,
        valid_group_prefixes: Tuple[str, ...] = config.VALID_GROUP_PREFIXES,
        institute_group_prefixes: Optional[dict] = None,
        valid_education_forms: Tuple[str, ...] = config.EDUCATION_FORMS,
        valid_education_levels: Tuple[str, ...] = config.EDUCATION_LEVELS,
        valid_institutes: Tuple[str, ...] = config.INSTITUTES,
        reward_for_correct_decision: int = config.DEFAULT_REWARD,
        fine_for_mistake: int = config.DEFAULT_FINE,
        dismissal_balance_limit: int = config.DEFAULT_DISMISSAL_BALANCE,
        current_date: Optional[date] = None,
    ):
        self.max_valid_birth_year = max_valid_birth_year
        self.group_pattern = group_pattern
        self.valid_group_prefixes = valid_group_prefixes
        self.institute_group_prefixes = institute_group_prefixes or getattr(
            config, "INSTITUTE_GROUP_PREFIXES", {}
        )
        self.valid_education_forms = valid_education_forms
        self.valid_education_levels = valid_education_levels
        self.valid_institutes = valid_institutes
        self.reward_for_correct_decision = reward_for_correct_decision
        self.fine_for_mistake = fine_for_mistake
        self.dismissal_balance_limit = dismissal_balance_limit
        self.current_date = current_date or date(2026, 9, 1)

    def instruction_lines(self, day_number: int = 1) -> dict:
        forms = ", ".join(self.valid_education_forms)
        levels = ", ".join(self.valid_education_levels)
        institutes = ", ".join(self.valid_institutes)
        group_rules = self.get_group_rules_text()

        day_instructions = config.INSTRUCTIONS_BY_DAY.get(
            day_number, config.INSTRUCTIONS_BY_DAY[1]
        )

        result = {"students": [], "teachers": []}

        for key in ["students", "teachers"]:
            lines = day_instructions.get(key, [])
            for line in lines:
                formatted_line = line.format(
                    max_year=self.max_valid_birth_year,
                    forms=forms,
                    levels=levels,
                    institutes=institutes,
                    group_rules=group_rules,
                    teacher_positions=", ".join(config.TEACHER_POSITIONS),
                    teacher_departments=", ".join(config.TEACHER_DEPARTMENTS),
                    teacher_degrees=", ".join(config.TEACHER_DEGREES),
                )
                result[key].append(formatted_line)

        return result

    def get_group_rules_text(self) -> str:
        rules = []

        for institute in self.valid_institutes:
            prefixes = "/".join(self.institute_group_prefixes[institute])
            rules.append(f"{institute}={prefixes}")

        return "; ".join(rules)


class Economy:
    """
    Управляет игровой экономикой: текущим балансом игрока,
    начислением наград (+10) за правильные решения и штрафов (-5) за ошибки.
    """
    def __init__(
        self,
        money: int = config.DEFAULT_MONEY,
        reward: int = config.DEFAULT_REWARD,
        fine_amount: int = config.DEFAULT_FINE,
    ):
        self.money = money
        self.reward = reward
        self.fine_amount = fine_amount

    def add_money(self, amount: Optional[int] = None) -> int:
        value = self.reward if amount is None else amount
        self.money += value
        return value

    def fine(self, amount: Optional[int] = None) -> int:
        value = self.fine_amount if amount is None else amount
        self.money -= value
        return -value

    def apply_result(self, is_correct: bool) -> int:
        if is_correct:
            return self.add_money()

        return self.fine()


class Document:
    """
    Базовый класс для документов (студенческий билет или пропуск).
    Содержит общие личные данные.
    """

    document_type = "Base"

    def __init__(
        self,
        full_name: str = "",
        birth_date=None,
        institute: str = "",
        issue_date=None,
        seed: int | None = None,
    ):
        self.full_name = full_name
        self.birth_date = birth_date
        self.institute = institute
        self.issue_date = issue_date
        import random as rnd

        self.seed = seed if seed is not None else rnd.randint(1, 2000000000)

    def display_birth_date(self) -> str:
        return display_date(self.birth_date)

    def display_issue_date(self) -> str:
        return display_date(self.issue_date)

    def get_display_data(self) -> list[str]:
        raise NotImplementedError

    def apply_random_error(self, reason: str, random_source, rules) -> None:
        raise NotImplementedError

    def check_birth_date(self, rules, errors: list[str]) -> None:
        raise NotImplementedError

    def check_group(self, rules, errors: list[str]) -> None:
        raise NotImplementedError

    def check_education_form(self, rules, errors: list[str]) -> None:
        raise NotImplementedError

    def check_education_level(self, rules, errors: list[str]) -> None:
        raise NotImplementedError

    def to_save_data(self) -> dict:
        raise NotImplementedError

    @staticmethod
    def from_save_data(data) -> "Document | None":
        if not isinstance(data, dict):
            return None

        import config

        doc_type = str(
            data.get(config.SAVE_DOCUMENT_TYPE, config.DOCUMENT_TYPE_STUDENT)
        )
        if doc_type == config.DOCUMENT_TYPE_VIP:
            return VipDocument.from_save_data(data)

        return StudentDocument.from_save_data(data)


class StudentDocument(Document):
    import config

    document_type = config.DOCUMENT_TYPE_STUDENT

    def __init__(
        self,
        full_name: str = "",
        group: str = "",
        birth_date=None,
        education_form: str = "",
        education_level: str = "",
        institute: str = "",
        issue_date=None,
        seed: int | None = None,
    ):
        super().__init__(full_name, birth_date, institute, issue_date, seed)
        self.group = group
        self.education_form = education_form
        self.education_level = education_level

    def get_display_data(self) -> list[str]:
        import config

        return [
            self.document_type,
            f"{config.PERSON_FULL_NAME_TEXT}: {self.full_name}",
            f"{config.PERSON_GROUP_TEXT}: {self.group}",
            f"{config.PERSON_BIRTH_DATE_TEXT}: {self.display_birth_date()}",
            f"{config.EDUCATION_FORM_TEXT}: {self.education_form}",
            f"{config.EDUCATION_LEVEL_TEXT}: {self.education_level}",
            f"{config.INSTITUTE_TEXT}: {self.institute}",
            f"{config.ISSUE_DATE_TEXT}: {self.display_issue_date()}",
        ]

    def apply_random_error(self, reason: str, random_source, rules) -> None:
        import config

        if reason == config.BAD_GROUP_FORMAT:
            self.group = random_source.choice(config.BAD_GROUP_VARIANTS)
        elif reason == config.BAD_EDUCATION_FORM:
            self.education_form = random_source.choice(
                config.BAD_EDUCATION_FORMS
            )
        elif reason == config.BAD_EDUCATION_LEVEL:
            self.education_level = random_source.choice(
                config.BAD_EDUCATION_LEVELS
            )
        elif reason == config.BAD_INSTITUTE:
            self.institute = random_source.choice(config.BAD_INSTITUTES)

    def check_birth_date(self, rules, errors: list[str]) -> None:
        import config

        if (
            self.birth_date is None
            or self.birth_date.year > rules.max_valid_birth_year
        ):
            errors.append(config.ERROR_BAD_BIRTH_DATE)

    def check_group(self, rules, errors: list[str]) -> None:
        import config

        if not re.match(rules.group_pattern, self.group):
            errors.append(config.ERROR_BAD_GROUP_FORMAT)
            return

        prefix = self.group.split(config.GROUP_SEPARATOR)[0]
        if prefix not in rules.institute_group_prefixes.get(
            self.institute, []
        ):
            if hasattr(config, "ERROR_BAD_GROUP_PREFIX"):
                errors.append(config.ERROR_BAD_GROUP_PREFIX)

    def check_education_form(self, rules, errors: list[str]) -> None:
        import config

        if self.education_form not in rules.valid_education_forms:
            errors.append(config.ERROR_BAD_EDUCATION_FORM)

    def check_education_level(self, rules, errors: list[str]) -> None:
        import config

        if self.education_level not in rules.valid_education_levels:
            errors.append(config.ERROR_BAD_EDUCATION_LEVEL)

    def to_save_data(self) -> dict:
        import config

        return {
            config.SAVE_FULL_NAME: self.full_name,
            config.SAVE_GROUP: self.group,
            config.SAVE_BIRTH_DATE: date_to_save(self.birth_date),
            config.SAVE_EDUCATION_FORM: self.education_form,
            config.SAVE_EDUCATION_LEVEL: self.education_level,
            config.SAVE_INSTITUTE: self.institute,
            config.SAVE_ISSUE_DATE: date_to_save(self.issue_date),
            config.SAVE_DOCUMENT_TYPE: self.document_type,
            config.SAVE_SEED: self.seed,
        }

    @staticmethod
    def from_save_data(data: dict) -> "StudentDocument":
        import config

        return StudentDocument(
            full_name=str(data.get(config.SAVE_FULL_NAME, "")),
            group=str(data.get(config.SAVE_GROUP, "")),
            birth_date=date_from_save(data.get(config.SAVE_BIRTH_DATE)),
            education_form=str(data.get(config.SAVE_EDUCATION_FORM, "")),
            education_level=str(data.get(config.SAVE_EDUCATION_LEVEL, "")),
            institute=str(data.get(config.SAVE_INSTITUTE, "")),
            issue_date=date_from_save(data.get(config.SAVE_ISSUE_DATE)),
            seed=data.get(config.SAVE_SEED),
        )


class VipDocument(Document):
    import config

    document_type = config.DOCUMENT_TYPE_VIP

    def __init__(
        self,
        full_name: str = "",
        position: str = "",
        birth_date=None,
        department: str = "",
        degree: str = "",
        institute: str = "",
        issue_date=None,
        seed: int | None = None,
    ):
        super().__init__(full_name, birth_date, institute, issue_date, seed)
        self.position = position
        self.department = department
        self.degree = degree

    def get_display_data(self) -> list[str]:
        import config

        return [
            self.document_type,
            f"{config.PERSON_FULL_NAME_TEXT}: {self.full_name}",
            f"{config.PERSON_POSITION_TEXT}: {self.position}",
            f"{config.PERSON_BIRTH_DATE_TEXT}: {self.display_birth_date()}",
            f"{config.PERSON_DEPARTMENT_TEXT}: {self.department}",
            f"{config.PERSON_DEGREE_TEXT}: {self.degree}",
            f"{config.INSTITUTE_TEXT}: {self.institute}",
            f"{config.ISSUE_DATE_TEXT}: {self.display_issue_date()}",
        ]

    def apply_random_error(self, reason: str, random_source, rules) -> None:
        import config

        if reason == config.BAD_GROUP_FORMAT:
            self.position = random_source.choice(config.BAD_TEACHER_POSITIONS)
        elif reason == config.BAD_EDUCATION_FORM:
            self.department = random_source.choice(
                config.BAD_TEACHER_DEPARTMENTS
            )
        elif reason == config.BAD_EDUCATION_LEVEL:
            self.degree = random_source.choice(config.BAD_TEACHER_DEGREES)
        elif reason == config.BAD_INSTITUTE:
            self.institute = random_source.choice(config.BAD_INSTITUTES)

    def check_birth_date(self, rules, errors: list[str]) -> None:
        pass

    def check_group(self, rules, errors: list[str]) -> None:
        import config

        if self.position not in config.TEACHER_POSITIONS:
            errors.append(config.ERROR_BAD_GROUP_FORMAT)

    def check_education_form(self, rules, errors: list[str]) -> None:
        import config

        if self.department not in config.TEACHER_DEPARTMENTS:
            errors.append(config.ERROR_BAD_EDUCATION_FORM)

    def check_education_level(self, rules, errors: list[str]) -> None:
        import config

        if self.degree not in config.TEACHER_DEGREES:
            errors.append(config.ERROR_BAD_EDUCATION_LEVEL)

    def to_save_data(self) -> dict:
        import config

        return {
            config.SAVE_FULL_NAME: self.full_name,
            config.SAVE_GROUP: self.position,
            config.SAVE_BIRTH_DATE: date_to_save(self.birth_date),
            config.SAVE_EDUCATION_FORM: self.department,
            config.SAVE_EDUCATION_LEVEL: self.degree,
            config.SAVE_INSTITUTE: self.institute,
            config.SAVE_ISSUE_DATE: date_to_save(self.issue_date),
            config.SAVE_DOCUMENT_TYPE: self.document_type,
            config.SAVE_SEED: self.seed,
        }

    @staticmethod
    def from_save_data(data: dict) -> "VipDocument":
        import config

        return VipDocument(
            full_name=str(data.get(config.SAVE_FULL_NAME, "")),
            position=str(data.get(config.SAVE_GROUP, "")),
            birth_date=date_from_save(data.get(config.SAVE_BIRTH_DATE)),
            department=str(data.get(config.SAVE_EDUCATION_FORM, "")),
            degree=str(data.get(config.SAVE_EDUCATION_LEVEL, "")),
            institute=str(data.get(config.SAVE_INSTITUTE, "")),
            issue_date=date_from_save(data.get(config.SAVE_ISSUE_DATE)),
            seed=data.get(config.SAVE_SEED),
        )


class Person:
    """
    Модель посетителя (человек, стоящий перед столом).
    Содержит его реальные данные (full_name, group) и документ, который он нам дает (document).
    Ошибка игрока - это если данные в документе не совпадают с правилами,
    или если человек - обманщик (imposter).
    """
    def __init__(
        self,
        full_name: str = "",
        group: str = "",
        birth_date=None,
        document: Optional[Document] = None,
        is_important: bool = False,
        gender: str = "",
    ):
        self.full_name = full_name
        self.group = group
        self.birth_date = birth_date
        self.document = document
        self.is_important = is_important
        self.gender = gender

    def display_data(self) -> List[str]:
        group_label = (
            config.PERSON_POSITION_TEXT
            if self.is_important
            else config.PERSON_GROUP_TEXT
        )
        return [
            f"{config.PERSON_FULL_NAME_TEXT}: {self.full_name}",
            f"{group_label}: {self.group}",
            f"{config.PERSON_BIRTH_DATE_TEXT}: {display_date(self.birth_date)}",
        ]

    def document_data(self) -> List[str]:
        if self.document is None:
            return [config.NO_DOCUMENT_TEXT]

        return self.document.get_display_data()

    def to_save_data(self) -> dict:
        document_data = None

        if self.document is not None:
            document_data = self.document.to_save_data()

        return {
            config.SAVE_FULL_NAME: self.full_name,
            config.SAVE_GROUP: self.group,
            config.SAVE_BIRTH_DATE: date_to_save(self.birth_date),
            config.SAVE_DOCUMENT: document_data,
            config.SAVE_IS_IMPORTANT: self.is_important,
            "gender": self.gender,
        }

    @staticmethod
    def from_save_data(data) -> Optional["Person"]:
        if not isinstance(data, dict):
            return None

        return Person(
            full_name=str(data.get(config.SAVE_FULL_NAME, "")),
            group=str(data.get(config.SAVE_GROUP, "")),
            birth_date=date_from_save(data.get(config.SAVE_BIRTH_DATE)),
            document=Document.from_save_data(data.get(config.SAVE_DOCUMENT)),
            is_important=bool(data.get(config.SAVE_IS_IMPORTANT, False)),
            gender=str(data.get("gender", config.GENDER_MALE)),
        )


class CheckResult:
    """
    Содержит результаты проверки документа посетителя:
    флаг разрешения/отказа и список выявленных несоответствий (ошибок).
    """

    def __init__(self, allow: bool, errors: Tuple[str, ...]):
        self.allow = allow
        self.errors = errors


class RoundResult:
    """
    Содержит сводку по итогам одного раунда (одного посетителя):
    решение игрока, правильное решение, изменение баланса, ошибки и статус окончания игры.
    """

    def __init__(
        self,
        player_decision: Decision,
        correct_decision: Decision,
        is_correct: bool,
        errors: Tuple[str, ...],
        money_delta: int,
        balance: int,
        game_over: bool,
        game_over_reason: str = "",
    ):
        self.player_decision = player_decision
        self.correct_decision = correct_decision
        self.is_correct = is_correct
        self.errors = errors
        self.money_delta = money_delta
        self.balance = balance
        self.game_over = game_over
        self.game_over_reason = game_over_reason


class PersonGenerator:
    """
    Генератор посетителей (фабрика).
    Создает людей, заполняет им случайные имена, даты и группы.
    Если решено сгенерировать нарушителя, берет случайную ошибку (error_reason)
    и портит какой-то из параметров документа.
    """
    def __init__(
        self, rules: Optional[GameRules] = None, seed: Optional[int] = None
    ):
        self.rules = rules or GameRules()
        self.random = random.Random(seed)
        self.error_bag = ShuffleBag(config.INVALID_REASONS, self.random)
        self.invalid_chance = PseudoRandomChance(
            getattr(config, "PRD_BASE_CHANCE", 0.15),
            getattr(config, "PRD_STEP", 0.05),
            getattr(config, "PRD_MAX_CHANCE", 0.85),
            self.random,
        )

    def generate(
        self,
        force_invalid: Optional[bool] = None,
        error_reason: Optional[str] = None,
    ) -> Person:
        person = self._generate_valid_person()
        should_be_invalid = force_invalid

        if should_be_invalid is None:
            should_be_invalid = self.invalid_chance.roll()

        if should_be_invalid:
            self._apply_random_error(person, error_reason)

        return person

    def _generate_valid_person(self) -> Person:
        is_important = self.random.random() < 0.30

        institute = self.random.choice(self.rules.valid_institutes)

        if is_important:
            gender = config.GENDER_MALE
            department = self.random.choice(config.TEACHER_DEPARTMENTS)
            degree = self.random.choice(config.TEACHER_DEGREES)
            group = self.random.choice(config.TEACHER_POSITIONS)
            birth_date = self._generate_birth_date(1950, 2000)
            full_name = self._generate_full_name(gender)
            issue_date = self._generate_valid_issue_date(birth_date)

            document = VipDocument(
                full_name=full_name,
                position=group,
                birth_date=birth_date,
                department=department,
                degree=degree,
                institute=institute,
                issue_date=issue_date,
                seed=self.random.randint(1, 2000000000),
            )
        else:
            gender = self.random.choice(config.GENDERS)
            education_form = self.random.choice(
                self.rules.valid_education_forms
            )
            education_level = self.random.choice(
                self.rules.valid_education_levels
            )
            group = self._generate_valid_group(institute)
            birth_date = self._generate_valid_birth_date()
            full_name = self._generate_full_name(gender)
            issue_date = self._generate_valid_issue_date(birth_date)

            document = StudentDocument(
                full_name=full_name,
                group=group,
                birth_date=birth_date,
                education_form=education_form,
                education_level=education_level,
                institute=institute,
                issue_date=issue_date,
                seed=self.random.randint(1, 2000000000),
            )

        return Person(
            full_name=full_name,
            group=group,
            birth_date=birth_date,
            document=document,
            is_important=is_important,
            gender=gender,
        )

    def _apply_random_error(
        self, person: Person, reason: Optional[str] = None
    ) -> None:
        if reason is None:
            reason = self.error_bag.get()

        if reason == config.NO_DOCUMENT:
            person.document = None
            return

        document = person.document
        if document is None:
            return

        if reason == config.BAD_BIRTH_DATE:
            document.birth_date = self._generate_invalid_birth_date()
        elif reason == config.BAD_ISSUE_DATE:
            document.issue_date = self._generate_bad_issue_date(
                document.birth_date
            )
        elif reason == config.BAD_NOT_UNIQUE_PASS:
            person.document = StudentDocument(
                full_name=document.full_name,
                group=getattr(
                    document, "group", getattr(document, "position", "")
                ),
                birth_date=document.birth_date,
                education_form=getattr(
                    document,
                    "education_form",
                    getattr(document, "department", ""),
                ),
                education_level=getattr(
                    document,
                    "education_level",
                    getattr(document, "degree", ""),
                ),
                institute=document.institute,
                issue_date=document.issue_date,
                seed=document.seed,
            )
        elif reason == config.BAD_IMPOSTER:
            person.document = VipDocument(
                full_name=document.full_name,
                position=getattr(
                    document, "group", getattr(document, "position", "")
                ),
                birth_date=document.birth_date,
                department=getattr(
                    document,
                    "education_form",
                    getattr(document, "department", ""),
                ),
                degree=getattr(
                    document,
                    "education_level",
                    getattr(document, "degree", ""),
                ),
                institute=document.institute,
                issue_date=document.issue_date,
                seed=document.seed,
            )
        else:
            document.apply_random_error(reason, self.random, self.rules)

    def _generate_full_name(self, gender: str) -> str:
        if gender == config.GENDER_FEMALE:
            first_name = self.random.choice(config.FEMALE_NAMES)
            last_name = self.random.choice(config.FEMALE_LAST_NAMES)
            patronymic = self.random.choice(config.FEMALE_PATRONYMICS)
        else:
            first_name = self.random.choice(config.MALE_NAMES)
            last_name = self.random.choice(config.MALE_LAST_NAMES)
            patronymic = self.random.choice(config.MALE_PATRONYMICS)

        return f"{last_name} {first_name} {patronymic}"

    def _generate_valid_birth_date(self) -> date:
        return self._generate_birth_date(
            config.MIN_BIRTH_YEAR, self.rules.max_valid_birth_year
        )

    def _generate_invalid_birth_date(self) -> date:
        return self._generate_birth_date(
            self.rules.max_valid_birth_year + 1,
            config.MAX_BIRTH_YEAR,
        )

    def _generate_birth_date(self, min_year: int, max_year: int) -> date:
        year = self.random.randint(min_year, max_year)
        month = self.random.randint(config.MIN_MONTH, config.MAX_MONTH)
        day = self.random.randint(config.MIN_DAY, config.MAX_SAFE_DAY)

        return date(year, month, day)

    def _generate_valid_issue_date(self, birth_date: date) -> date:
        return date(
            config.ISSUE_DATE_YEAR,
            config.ISSUE_DATE_MONTH,
            config.ISSUE_DATE_DAY,
        )

    def _generate_bad_issue_date(self, birth_date: Optional[date]) -> date:
        day, month = config.ISSUE_DATE_DAY, config.ISSUE_DATE_MONTH
        issue_year = config.ISSUE_DATE_YEAR

        if self.random.random() < 0.5:
            day, month = self.random.choice(
                getattr(config, "BAD_ISSUE_DATE_VARIANTS", [(1, 9), (2, 9)])
            )
        else:
            issue_year = self.random.randint(2018, 2023)

        return date(issue_year, month, day)

    def _generate_valid_group(self, institute: str) -> str:
        prefixes = self.rules.institute_group_prefixes[institute]
        prefix = self.random.choice(prefixes)
        group_number = self.random.randint(
            config.MIN_GROUP_NUMBER, config.MAX_GROUP_NUMBER
        )

        return f"{prefix}{config.GROUP_SEPARATOR}{group_number}"


class Checker:
    """
    Класс, отвечающий за проверку документов посетителя на соответствие правилам игры.
    Сравнивает данные документа с фактическими данными и выявляет несоответствия.
    """

    def __init__(self, rules: Optional[GameRules] = None):
        self.rules = rules or GameRules()

    def check_exists(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            errors.append(config.ERROR_NO_DOCUMENT)

    def check_birth_date(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return
        person.document.check_birth_date(self.rules, errors)

    def check_issue_date(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        document = person.document

        if not self.is_issue_date_correct(document.issue_date):
            errors.append(config.ERROR_BAD_ISSUE_DATE)

    def check_group(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return
        person.document.check_group(self.rules, errors)

    def check_education_form(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return
        person.document.check_education_form(self.rules, errors)

    def check_education_level(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return
        person.document.check_education_level(self.rules, errors)

    def check_institute(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        if person.document.institute not in self.rules.valid_institutes:
            errors.append(config.ERROR_BAD_INSTITUTE)

    def check_vip(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        is_doc_vip = isinstance(person.document, VipDocument)
        if person.is_important and not is_doc_vip:
            errors.append(config.ERROR_NOT_UNIQUE_PASS)
        elif not person.is_important and is_doc_vip:
            errors.append(config.ERROR_IMPOSTER)

    def is_issue_date_correct(
        self,
        issue_date: Optional[date],
    ) -> bool:
        if issue_date is None:
            return False

        if issue_date.day != config.ISSUE_DATE_DAY:
            return False
        if issue_date.month != config.ISSUE_DATE_MONTH:
            return False
        if issue_date.year != config.ISSUE_DATE_YEAR:
            return False

        return True

    def check_all(
        self,
        person: Person,
        active_checks: Optional[Tuple[str, ...]] = None,
    ) -> Tuple[bool, List[str]]:
        if active_checks is None:
            active_checks = config.ALL_CHECKS

        errors: List[str] = []

        if config.CHECK_DOCUMENT in active_checks:
            self.check_exists(person, errors)
        if person.document is None:
            return False, errors

        if config.CHECK_BIRTH_DATE in active_checks:
            self.check_birth_date(person, errors)
        if config.CHECK_ISSUE_DATE in active_checks:
            self.check_issue_date(person, errors)
        if config.CHECK_GROUP in active_checks:
            self.check_group(person, errors)
        if config.CHECK_EDUCATION_FORM in active_checks:
            self.check_education_form(person, errors)
        if config.CHECK_EDUCATION_LEVEL in active_checks:
            self.check_education_level(person, errors)
        if config.CHECK_INSTITUTE in active_checks:
            self.check_institute(person, errors)
        if config.CHECK_VIP in active_checks:
            self.check_vip(person, errors)

        return len(errors) == 0, errors

    def get_result(
        self,
        person: Person,
        active_checks: Optional[Tuple[str, ...]] = None,
    ) -> CheckResult:
        allow, errors = self.check_all(person, active_checks)
        return CheckResult(allow=allow, errors=tuple(errors))


class GameModel:
    """
    Главный класс игровой логики (Модель в паттерне MVC).
    Управляет состоянием игры, днями, балансом, посетителями и их валидацией.
    """

    def __init__(
        self,
        rules: Optional[GameRules] = None,
        generator: Optional[PersonGenerator] = None,
        checker: Optional[Checker] = None,
        economy: Optional[Economy] = None,
        seed: Optional[int] = None,
        day_planner: Optional[GeneticDayPlanner] = None,
    ):
        self.rules = rules or GameRules()
        self.random = random.Random(seed)
        self.generator = generator or PersonGenerator(self.rules, seed)
        self.checker = checker or Checker(self.rules)
        self.economy = economy or Economy(
            reward=self.rules.reward_for_correct_decision,
            fine_amount=self.rules.fine_for_mistake,
        )
        self.day_planner = day_planner or GeneticDayPlanner(
            config.DAY_VISITORS_COUNT,
            config.DAY_MIN_BAD_VISITORS,
            config.DAY_MAX_BAD_VISITORS,
            config.DAY_PLAN_POPULATION_SIZE,
            config.DAY_PLAN_GENERATIONS,
            config.DAY_PLAN_MUTATION_CHANCE,
            self.random,
        )
        self._round_number = 0
        self._day_number = 0
        self._day_plan = []
        self._day_plan_index = 0
        self._current_person: Optional[Person] = None
        self._last_result: Optional[RoundResult] = None
        self._game_over = False
        self._game_over_reason = ""
        self._day_finished = False
        self._daily_processed = 0
        self._daily_correct = 0
        self._daily_mistakes = 0
        self._daily_money_earned = 0
        self._daily_money_lost = 0

        self.start_new_day()
        self.next_round()

    @property
    def round_number(self) -> int:
        return self._round_number

    @property
    def day_number(self) -> int:
        return self._day_number

    @property
    def current_person(self) -> Optional[Person]:
        return self._current_person

    @property
    def last_result(self) -> Optional[RoundResult]:
        return self._last_result

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def game_over_reason(self) -> str:
        return self._game_over_reason

    @property
    def day_finished(self) -> bool:
        return self._day_finished

    @property
    def daily_processed(self) -> int:
        return self._daily_processed

    @property
    def daily_correct(self) -> int:
        return self._daily_correct

    @property
    def daily_mistakes(self) -> int:
        return self._daily_mistakes

    @property
    def daily_money_earned(self) -> int:
        return self._daily_money_earned

    @property
    def daily_money_lost(self) -> int:
        return self._daily_money_lost

    def start_new_day(self) -> None:
        self._day_number += 1

        self._day_plan = self.day_planner.make_plan(self._day_number)
        self._day_plan_index = 0
        self._day_finished = False
        self._daily_processed = 0
        self._daily_correct = 0
        self._daily_mistakes = 0
        self._daily_money_earned = 0
        self._daily_money_lost = 0

    def next_round(self) -> Optional[Person]:
        if self._game_over:
            return None

        if self._day_plan_index >= len(self._day_plan):
            self._day_finished = True
            self._current_person = None
            return None

        should_be_invalid = self._day_plan[self._day_plan_index]
        active_checks = self.get_active_checks()
        error_reason = self.choose_error_reason(
            should_be_invalid, active_checks
        )
        self._day_plan_index += 1
        self._round_number += 1
        self._current_person = self.generate_person(
            should_be_invalid, error_reason
        )

        return self._current_person

    def choose_error_reason(
        self,
        should_be_invalid: bool,
        active_checks: Tuple[str, ...],
    ) -> Optional[str]:
        if not should_be_invalid:
            return None

        active_reasons = get_error_reasons_for_checks(active_checks)

        return self.random.choice(active_reasons)

    def generate_person(
        self,
        should_be_invalid: bool,
        error_reason: Optional[str],
    ) -> Person:
        if isinstance(self.generator, PersonGenerator):
            return self.generator.generate(should_be_invalid, error_reason)

        return self.generator.generate()

    def decide(self, decision: Union[Decision, str, bool]) -> RoundResult:
        if self._current_person is None:
            raise RuntimeError(config.MESSAGE_NO_CURRENT_PERSON)
        if self._game_over:
            raise RuntimeError(config.MESSAGE_GAME_ALREADY_OVER)

        player_decision = self._normalize_decision(decision)
        check_result = self.checker.get_result(
            self._current_person, self.get_active_checks()
        )
        correct_decision = (
            Decision.ALLOW if check_result.allow else Decision.DENY
        )
        is_correct = player_decision == correct_decision
        money_delta = self.economy.apply_result(is_correct)

        self._daily_processed += 1
        if is_correct:
            self._daily_correct += 1
            if money_delta > 0:
                self._daily_money_earned += money_delta
        else:
            self._daily_mistakes += 1
            if money_delta < 0:
                self._daily_money_lost -= money_delta

        if self.economy.money <= self.rules.dismissal_balance_limit:
            self._game_over = True
            self._game_over_reason = config.MESSAGE_DISMISSED

        result = RoundResult(
            player_decision=player_decision,
            correct_decision=correct_decision,
            is_correct=is_correct,
            errors=check_result.errors,
            money_delta=money_delta,
            balance=self.economy.money,
            game_over=self._game_over,
            game_over_reason=self._game_over_reason,
        )
        self._last_result = result

        if not self._game_over and not self._day_finished:
            self.next_round()

        return result

    def get_instruction(self) -> List[str]:
        return self.rules.instruction_lines(self._day_number)

    def get_active_checks(self) -> Tuple[str, ...]:
        return get_active_checks(self._day_number)

    def get_time_info(self) -> Tuple[int, str, str]:
        current_date = date(2024, 9, 1) + timedelta(days=self._day_number - 1)
        date_str = current_date.strftime(config.DATE_FORMAT)

        time_minutes = 8 * 60 + (self._day_plan_index - 1) * 35
        if time_minutes < 8 * 60:
            time_minutes = 8 * 60

        hours = time_minutes // 60
        minutes = time_minutes % 60
        time_str = f"{hours:02d}:{minutes:02d}"

        return self._day_number, date_str, time_str

    def to_save_data(self) -> dict:
        current_person_data = None

        if self._current_person is not None:
            current_person_data = self._current_person.to_save_data()

        return {
            config.SAVE_MONEY: self.economy.money,
            config.SAVE_ROUND_NUMBER: self._round_number,
            config.SAVE_DAY_NUMBER: self._day_number,
            config.SAVE_DAY_PLAN: self._day_plan,
            config.SAVE_DAY_PLAN_INDEX: self._day_plan_index,
            config.SAVE_CURRENT_PERSON: current_person_data,
            config.SAVE_GAME_OVER: self._game_over,
            config.SAVE_GAME_OVER_REASON: self._game_over_reason,
            config.SAVE_DAY_FINISHED: self._day_finished,
            config.SAVE_DAILY_PROCESSED: self._daily_processed,
            config.SAVE_DAILY_CORRECT: self._daily_correct,
            config.SAVE_DAILY_MISTAKES: self._daily_mistakes,
            config.SAVE_DAILY_MONEY_EARNED: self._daily_money_earned,
            config.SAVE_DAILY_MONEY_LOST: self._daily_money_lost,
        }

    @staticmethod
    def from_save_data(data) -> "GameModel":
        game = GameModel()

        if not isinstance(data, dict):
            return game

        game.economy.money = int(
            data.get(config.SAVE_MONEY, config.DEFAULT_MONEY)
        )
        game._round_number = int(data.get(config.SAVE_ROUND_NUMBER, 0))
        game._day_number = int(data.get(config.SAVE_DAY_NUMBER, 1))
        game._day_plan = GameModel.fix_day_plan(data.get(config.SAVE_DAY_PLAN))
        game._day_plan_index = int(data.get(config.SAVE_DAY_PLAN_INDEX, 0))
        game._current_person = Person.from_save_data(
            data.get(config.SAVE_CURRENT_PERSON)
        )
        game._game_over = bool(data.get(config.SAVE_GAME_OVER, False))
        game._game_over_reason = str(
            data.get(config.SAVE_GAME_OVER_REASON, "")
        )
        game._day_finished = bool(data.get(config.SAVE_DAY_FINISHED, False))
        game._daily_processed = int(data.get(config.SAVE_DAILY_PROCESSED, 0))
        game._daily_correct = int(data.get(config.SAVE_DAILY_CORRECT, 0))
        game._daily_mistakes = int(data.get(config.SAVE_DAILY_MISTAKES, 0))
        game._daily_money_earned = int(
            data.get(config.SAVE_DAILY_MONEY_EARNED, 0)
        )
        game._daily_money_lost = int(data.get(config.SAVE_DAILY_MONEY_LOST, 0))

        if len(game._day_plan) == 0:
            game._day_plan = game.day_planner.make_plan(game._day_number)
            game._day_plan_index = 0

        if (
            game._current_person is None
            and not game._game_over
            and not game._day_finished
        ):
            game.next_round()

        return game

    @staticmethod
    def fix_day_plan(value) -> List[bool]:
        if not isinstance(value, list):
            return []

        plan = []

        for item in value:
            plan.append(bool(item))

        return plan

    @staticmethod
    def _normalize_decision(decision: Union[Decision, str, bool]) -> Decision:
        if isinstance(decision, Decision):
            return decision
        if isinstance(decision, bool):
            return Decision.ALLOW if decision else Decision.DENY

        value = decision.strip().lower()

        if value in config.ALLOW_DECISIONS:
            return Decision.ALLOW
        if value in config.DENY_DECISIONS:
            return Decision.DENY

        raise ValueError(
            config.MESSAGE_UNKNOWN_DECISION.format(decision=decision)
        )
