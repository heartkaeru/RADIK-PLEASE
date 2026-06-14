import config
from mvc.controller import GameController
from mvc.model import Decision, RoundResult


class TestGameController:
    def setup_method(self):
        self.controller = GameController.__new__(GameController)

    def test_fix_bool_returns_default_for_wrong_type(self):
        result = self.controller.fix_bool("yes", False)

        assert result is False

    def test_fix_volume_limits_big_value(self):
        result = self.controller.fix_volume(2.5, config.DEFAULT_MUSIC_VOLUME)

        assert result == config.MAX_VOLUME

    def test_fix_volume_limits_small_value(self):
        result = self.controller.fix_volume(-1, config.DEFAULT_MUSIC_VOLUME)

        assert result == config.MIN_VOLUME

    def test_fix_volume_ignores_bool(self):
        result = self.controller.fix_volume(True, config.DEFAULT_MUSIC_VOLUME)

        assert result == config.DEFAULT_MUSIC_VOLUME

    def test_fix_window_mode_number_returns_default_for_wrong_number(self):
        result = self.controller.fix_window_mode_number(100)

        assert result == config.DEFAULT_WINDOW_MODE_NUMBER

    def test_result_text_for_correct_decision(self):
        result = RoundResult(
            player_decision=Decision.ALLOW,
            correct_decision=Decision.ALLOW,
            is_correct=True,
            errors=(),
            money_delta=10,
            balance=10,
            game_over=False,
        )

        text = self.controller.get_result_text(result)

        assert text == config.RESULT_CORRECT_TEXT.format(money_delta=10)

    def test_result_text_for_mistake(self):
        result = RoundResult(
            player_decision=Decision.ALLOW,
            correct_decision=Decision.DENY,
            is_correct=False,
            errors=(),
            money_delta=-5,
            balance=-5,
            game_over=False,
        )

        text = self.controller.get_result_text(result)

        assert text == config.RESULT_MISTAKE_TEXT.format(money_delta=-5)

    def test_escape_opens_and_closes_menu(self):
        self.controller.screen_name = config.SCREEN_GAME
        self.controller.game_started = True

        self.controller.handle_escape()
        assert self.controller.screen_name == config.SCREEN_MENU

        self.controller.handle_escape()
        assert self.controller.screen_name == config.SCREEN_GAME

    def test_get_default_settings(self):
        settings = self.controller.get_default_settings()
        assert (
            settings[config.SETTING_MUSIC_ENABLED]
            == config.DEFAULT_MUSIC_ENABLED
        )
        assert (
            settings[config.SETTING_SOUND_ENABLED]
            == config.DEFAULT_SOUND_ENABLED
        )
        assert (
            settings[config.SETTING_MUSIC_VOLUME]
            == config.DEFAULT_MUSIC_VOLUME
        )
        assert (
            settings[config.SETTING_SOUND_VOLUME]
            == config.DEFAULT_SOUND_VOLUME
        )
        assert (
            settings[config.SETTING_WINDOW_MODE_NUMBER]
            == config.DEFAULT_WINDOW_MODE_NUMBER
        )

    def test_get_balance_without_game_model(self):
        self.controller.game_model = None
        assert self.controller.get_balance() == config.DEFAULT_MONEY
