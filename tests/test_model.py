import pytest
from datetime import date

import config
from model import Checker, Decision, Document, Economy, GameModel, GameRules, Person, PersonGenerator


def make_valid_person() -> Person:
    birth_date = date(2007, 1, 1)
    document = Document(
        full_name="Иванов Иван Иванович",
        group="ЭК-123456",
        birth_date=birth_date,
        education_form="очная",
        education_level="бакалавриат",
        institute="ИнЭУ",
        issue_date=date(2024, 9, 1),
    )

    return Person(
        full_name="Иванов Иван Иванович",
        group="ЭК-123456",
        birth_date=birth_date,
        document=document,
    )


class FixedGenerator:
    def __init__(self, person: Person):
        self.person = person

    def generate(self) -> Person:
        return self.person


class TestChecker:
    def setup_method(self):
        self.checker = Checker(GameRules())

    def test_valid_student_card_is_allowed(self):
        person = make_valid_person()

        result = self.checker.get_result(person)

        assert result.allow is True
        assert result.errors == ()

    def test_person_without_student_card_is_denied(self):
        person = make_valid_person()
        person.document = None

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_NO_DOCUMENT in result.errors

    def test_bad_birth_year_is_denied(self):
        person = make_valid_person()
        person.document.birth_date = date(2008, 1, 1)

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_BAD_BIRTH_DATE in result.errors

    def test_bad_issue_date_is_denied(self):
        person = make_valid_person()
        person.document.issue_date = date(2027, 10, 1)

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_BAD_ISSUE_DATE in result.errors

    def test_bad_group_format_is_denied(self):
        person = make_valid_person()
        person.document.group = "ИС123456"

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_BAD_GROUP_FORMAT in result.errors

    def test_bad_group_prefix_is_denied(self):
        person = make_valid_person()
        person.document.group = "ЮР-123456"

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_BAD_GROUP_PREFIX in result.errors

    def test_bad_education_form_is_denied(self):
        person = make_valid_person()
        person.document.education_form = "Домашняя"

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_BAD_EDUCATION_FORM in result.errors

    def test_bad_education_level_is_denied(self):
        person = make_valid_person()
        person.document.education_level = "Супервысшее"

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_BAD_EDUCATION_LEVEL in result.errors

    def test_bad_institute_is_denied(self):
        person = make_valid_person()
        person.document.institute = "Факультет без расписания"

        result = self.checker.get_result(person)

        assert result.allow is False
        assert config.ERROR_BAD_INSTITUTE in result.errors


class TestPersonGenerator:
    def test_generated_valid_person_has_correct_student_card(self):
        rules = GameRules()
        generator = PersonGenerator(rules, seed=1)

        person = generator._generate_valid_person()
        result = Checker(rules).get_result(person)

        assert result.allow is True
        assert person.document is not None
        assert len(person.full_name.split()) == 3


class TestEconomy:
    def test_correct_result_adds_money(self):
        economy = Economy(money=0, reward=10, fine_amount=5)

        money_delta = economy.apply_result(True)

        assert money_delta == 10
        assert economy.money == 10

    def test_mistake_takes_money(self):
        economy = Economy(money=0, reward=10, fine_amount=5)

        money_delta = economy.apply_result(False)

        assert money_delta == -5
        assert economy.money == -5


class TestGameModel:
    def test_allowing_valid_person_is_correct(self):
        person = make_valid_person()
        game = GameModel(generator=FixedGenerator(person))

        result = game.decide(Decision.ALLOW)

        assert result.is_correct is True
        assert result.money_delta == config.DEFAULT_REWARD
        assert result.balance == config.DEFAULT_REWARD

    def test_denying_person_without_card_is_correct(self):
        person = make_valid_person()
        person.document = None
        game = GameModel(generator=FixedGenerator(person))

        result = game.decide(Decision.DENY)

        assert result.is_correct is True
        assert result.money_delta == config.DEFAULT_REWARD

    def test_wrong_decision_can_end_game(self):
        person = make_valid_person()
        rules = GameRules(
            fine_for_mistake=5,
            dismissal_balance_limit=-5,
        )
        economy = Economy(money=0, reward=10, fine_amount=5)
        game = GameModel(
            rules=rules,
            generator=FixedGenerator(person),
            economy=economy,
        )

        result = game.decide(Decision.DENY)

        assert result.is_correct is False
        assert result.game_over is True
        assert result.balance == -5
