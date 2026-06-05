import json
import os

import pygame

import config
from model import Decision, GameModel
from view import Screen


class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        settings = self.load_settings()

        pygame.mixer.music.load(config.MUSIC_PATH)
        pygame.mixer.music.set_volume(settings[config.SETTING_MUSIC_VOLUME])
        pygame.mixer.music.play(-1)

        self.view = Screen()
        self.screen_name = config.SCREEN_MENU
        self.music_enabled = settings[config.SETTING_MUSIC_ENABLED]
        self.sound_enabled = settings[config.SETTING_SOUND_ENABLED]
        self.music_volume = settings[config.SETTING_MUSIC_VOLUME]
        self.sound_volume = settings[config.SETTING_SOUND_VOLUME]
        self.window_mode_number = settings[config.SETTING_WINDOW_MODE_NUMBER]
        self.game_started = False
        self.game_model = None
        self.instruction_open = False
        self.student_card_open = False
        self.visitor_visible = False
        self.result_text = ""
        self.result_is_correct = True
        self.next_visitor_time = None
        self.active_slider = None
        self.clock = pygame.time.Clock()
        self.visitor_state = "NONE"
        self.visitor_x = 0.0
        self.leaving_person = None
        self.allow_pressed = False
        self.deny_pressed = False
        self.fade_alpha = 0.0
        self.fade_state = "NONE"

        if not self.music_enabled:
            pygame.mixer.music.pause()

        self.apply_window_mode()

    def run(self):
        while self.view.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update_game_state(dt)
            self.draw_current_screen()

        pygame.quit()

    def draw_current_screen(self):
        if self.screen_name == config.SCREEN_MENU:
            self.view.draw_menu(self.has_save())
        elif self.screen_name == config.SCREEN_SETTINGS:
            self.view.draw_settings(
                self.music_enabled,
                self.sound_enabled,
                self.music_volume,
                self.sound_volume,
            )
        elif self.screen_name == config.SCREEN_GAME:
            day, date_str, time_str = self.game_model.get_time_info()
            visitor_pos = (self.visitor_x, config.PERSON_RECT_Y) if self.visitor_visible else None
            student_card_on_table = (self.visitor_state == "AT_DESK")
            self.view.draw_game(
                self.get_balance(),
                day,
                date_str,
                time_str,
                self.get_current_person(),
                self.visitor_visible,
                self.student_card_open,
                self.result_text,
                self.result_is_correct,
                self.instruction_open,
                self.get_instruction_lines(),
                visitor_position=visitor_pos,
                student_card_on_table=student_card_on_table,
                allow_pressed=self.allow_pressed,
                deny_pressed=self.deny_pressed,
                visitor_state=self.visitor_state,
            )
        elif self.screen_name == config.SCREEN_DAY_SUMMARY:
            self.view.draw_day_summary(
                self.game_model.day_number,
                self.game_model.daily_processed,
                self.game_model.daily_correct,
                self.game_model.daily_mistakes,
                self.game_model.daily_money_earned,
                self.game_model.daily_money_lost,
            )
        elif self.screen_name == config.SCREEN_TUTORIAL:
            self.view.draw_tutorial()

        if self.fade_alpha > 0:
            self.view.draw_fade(self.fade_alpha)
            
        self.view.update_screen()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game()
                self.save_settings()
                self.view.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.handle_escape()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.handle_mouse_up(event.pos)
            elif event.type == pygame.MOUSEMOTION and self.active_slider is not None:
                self.handle_slider_drag(event.pos)

    def handle_escape(self):
        if self.screen_name == config.SCREEN_GAME:
            self.screen_name = config.SCREEN_MENU
        elif self.screen_name == config.SCREEN_MENU and self.game_started:
            self.screen_name = config.SCREEN_GAME
        elif self.screen_name == config.SCREEN_SETTINGS:
            self.screen_name = config.SCREEN_MENU

    def handle_mouse_down(self, mouse_pos):
        if self.screen_name == config.SCREEN_MENU:
            self.handle_menu_click(mouse_pos)
        elif self.screen_name == config.SCREEN_SETTINGS:
            self.handle_settings_click(mouse_pos)
        elif self.screen_name == config.SCREEN_GAME:
            self.handle_game_click(mouse_pos)
        elif self.screen_name == config.SCREEN_DAY_SUMMARY:
            self.handle_day_summary_click(mouse_pos)
        elif self.screen_name == config.SCREEN_TUTORIAL:
            self.handle_tutorial_click(mouse_pos)

    def handle_day_summary_click(self, mouse_pos):
        if config.BUTTON_NEXT_DAY in self.view.menu_buttons:
            if self.view.menu_buttons[config.BUTTON_NEXT_DAY].collidepoint(mouse_pos):
                self.game_model.start_new_day()
                self.game_model.next_round()
                self.screen_name = config.SCREEN_GAME
                self.fade_state = "FADE_IN"
                self.fade_alpha = 255
                self.visitor_visible = True
                self.visitor_state = "WALKING_IN"
                self.visitor_x = config.DEFAULT_WINDOW_WIDTH
                self.save_game()

    def handle_tutorial_click(self, mouse_pos):
        if config.BUTTON_TUTORIAL_CONTINUE in self.view.menu_buttons:
            if self.view.menu_buttons[config.BUTTON_TUTORIAL_CONTINUE].collidepoint(mouse_pos):
                self.screen_name = config.SCREEN_GAME

    def handle_menu_click(self, mouse_pos):
        buttons = self.view.menu_buttons

        if buttons[config.BUTTON_START].collidepoint(mouse_pos):
            self.start_game()
        elif config.BUTTON_CONTINUE in buttons and buttons[config.BUTTON_CONTINUE].collidepoint(mouse_pos) and self.has_save():
            self.continue_game()
        elif buttons[config.BUTTON_SETTINGS].collidepoint(mouse_pos):
            self.screen_name = config.SCREEN_SETTINGS
        elif buttons[config.BUTTON_EXIT].collidepoint(mouse_pos):
            self.save_game()
            self.save_settings()
            self.view.running = False

    def handle_settings_click(self, mouse_pos):
        buttons = self.view.settings_buttons

        if buttons[config.BUTTON_MUSIC].collidepoint(mouse_pos):
            self.toggle_music()
        elif self.slider_has_mouse(config.SLIDER_MUSIC_VOLUME, mouse_pos):
            self.active_slider = config.SLIDER_MUSIC_VOLUME
            self.set_music_volume_by_mouse(mouse_pos)
        elif buttons[config.BUTTON_SOUND].collidepoint(mouse_pos):
            self.toggle_sound()
        elif self.slider_has_mouse(config.SLIDER_SOUND_VOLUME, mouse_pos):
            self.active_slider = config.SLIDER_SOUND_VOLUME
            self.set_sound_volume_by_mouse(mouse_pos)
        elif buttons[config.BUTTON_BACK].collidepoint(mouse_pos):
            self.screen_name = config.SCREEN_MENU

    def handle_game_click(self, mouse_pos):
        if self.view.is_instruction_book_clicked(mouse_pos):
            self.instruction_open = not self.instruction_open
        elif self.game_model is None:
            return
        elif self.game_model.game_over:
            return
        elif not self.visitor_visible or self.visitor_state != "AT_DESK":
            return
        elif self.view.is_allow_button_clicked(mouse_pos):
            self.allow_pressed = True
        elif self.view.is_deny_button_clicked(mouse_pos):
            self.deny_pressed = True
        elif self.has_current_document() and self.view.is_student_card_clicked(mouse_pos):
            if self.visitor_state == "AT_DESK":
                self.student_card_open = not self.student_card_open

    def handle_mouse_up(self, mouse_pos=None):
        if self.active_slider is not None:
            self.save_settings()
            self.active_slider = None
            
        if self.screen_name == config.SCREEN_GAME and mouse_pos is not None:
            if self.allow_pressed and self.view.is_allow_button_clicked(mouse_pos):
                self.make_decision(Decision.ALLOW)
            elif self.deny_pressed and self.view.is_deny_button_clicked(mouse_pos):
                self.make_decision(Decision.DENY)
                
            self.allow_pressed = False
            self.deny_pressed = False

    def handle_slider_drag(self, mouse_pos):
        if self.active_slider == config.SLIDER_MUSIC_VOLUME:
            self.set_music_volume_by_mouse(mouse_pos)
        elif self.active_slider == config.SLIDER_SOUND_VOLUME:
            self.set_sound_volume_by_mouse(mouse_pos)

    def start_game(self):
        self.game_model = GameModel()
        self.delete_save()
        self.game_started = True
        self.instruction_open = False
        self.student_card_open = False
        self.visitor_visible = True
        self.visitor_state = "WALKING_IN"
        self.visitor_x = config.DEFAULT_WINDOW_WIDTH
        self.result_text = ""
        self.next_visitor_time = None
        self.screen_name = config.SCREEN_TUTORIAL

    def continue_game(self):
        if self.game_model is None:
            self.load_game()

        self.game_started = True
        
        if self.game_model.day_finished:
            self.screen_name = config.SCREEN_DAY_SUMMARY
        else:
            self.visitor_visible = True
            self.visitor_state = "WALKING_IN"
            self.visitor_x = config.DEFAULT_WINDOW_WIDTH
            self.student_card_open = False
            self.screen_name = config.SCREEN_GAME

    def update_game_state(self, dt):
        if self.screen_name == config.SCREEN_TUTORIAL:
            return

        if self.fade_state == "FADE_OUT":
            self.fade_alpha += config.FADE_SPEED * dt
            if self.fade_alpha >= 255:
                self.fade_alpha = 0
                self.fade_state = "NONE"
                self.screen_name = config.SCREEN_DAY_SUMMARY
            return
        elif self.fade_state == "FADE_IN":
            self.fade_alpha -= config.FADE_SPEED * dt
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_state = "NONE"
            return
            
        if self.visitor_state == "WALKING_IN":
            self.visitor_x -= 1000 * dt
            if self.visitor_x <= config.PERSON_RECT_X:
                self.visitor_x = config.PERSON_RECT_X
                self.visitor_state = "AT_DESK"
        elif self.visitor_state == "WALKING_OUT":
            self.visitor_x -= 1000 * dt
            if self.visitor_x <= -config.PERSON_RECT_WIDTH:
                self.visitor_state = "NONE"
                self.visitor_visible = False
                if self.game_model and not self.game_model.game_over:
                    if self.game_model.day_finished:
                        self.fade_state = "FADE_OUT"
                        self.next_visitor_time = None
                    else:
                        self.next_visitor_time = pygame.time.get_ticks() + 200

        if self.next_visitor_time is None:
            return

        if pygame.time.get_ticks() < self.next_visitor_time:
            return

        self.visitor_visible = True
        self.visitor_state = "WALKING_IN"
        self.visitor_x = config.DEFAULT_WINDOW_WIDTH
        self.student_card_open = False
        self.result_text = ""
        self.next_visitor_time = None

    def make_decision(self, decision):
        self.leaving_person = self.get_current_person()
        result = self.game_model.decide(decision)
        self.result_text = self.get_result_text(result)
        self.result_is_correct = result.is_correct
        self.visitor_state = "WALKING_OUT"
        self.student_card_open = False

        if result.game_over:
            self.result_text = result.game_over_reason
            self.next_visitor_time = None
            self.delete_save()
        else:
            self.next_visitor_time = None
            self.save_game()

    def get_result_text(self, result):
        if result.is_correct:
            return config.RESULT_CORRECT_TEXT.format(money_delta=result.money_delta)

        return config.RESULT_MISTAKE_TEXT.format(money_delta=result.money_delta)

    def get_balance(self):
        if self.game_model is None:
            return config.DEFAULT_MONEY

        return self.game_model.economy.money

    def get_current_person(self):
        if self.game_model is None:
            return None

        if self.visitor_state == "WALKING_OUT" and self.leaving_person is not None:
            return self.leaving_person

        return self.game_model.current_person

    def has_current_document(self):
        person = self.get_current_person()

        if person is None:
            return False

        return person.document is not None

    def get_instruction_lines(self):
        if self.game_model is None:
            return []

        return self.game_model.get_instruction()

    def has_save(self):
        return os.path.exists(config.SAVE_FILE)

    def load_game(self):
        if not self.has_save():
            self.game_model = GameModel()
            return
        try:
            with open(config.SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.game_model = GameModel.from_save_data(data)
        except Exception:
            self.game_model = GameModel()

    def save_game(self):
        if self.game_model is None or self.game_model.game_over:
            return
        try:
            data = self.game_model.to_save_data()
            with open(config.SAVE_FILE, "w", encoding="utf-8", newline="\r\n") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def delete_save(self):
        if self.has_save():
            try:
                os.remove(config.SAVE_FILE)
            except OSError:
                pass

    def toggle_music(self):
        self.music_enabled = not self.music_enabled

        if self.music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        self.save_settings()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.save_settings()

    def set_music_volume_by_mouse(self, mouse_pos):
        self.music_volume = self.get_volume_from_slider(config.SLIDER_MUSIC_VOLUME, mouse_pos)
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume_by_mouse(self, mouse_pos):
        self.sound_volume = self.get_volume_from_slider(config.SLIDER_SOUND_VOLUME, mouse_pos)

    def slider_has_mouse(self, slider_name, mouse_pos):
        slider = self.view.settings_sliders[slider_name]
        hit_box = slider.inflate(0, config.SLIDER_KNOB_HEIGHT)
        return hit_box.collidepoint(mouse_pos)

    def get_volume_from_slider(self, slider_name, mouse_pos):
        slider = self.view.settings_sliders[slider_name]
        volume = (mouse_pos[0] - slider.x) / slider.width

        if volume > config.MAX_VOLUME:
            return config.MAX_VOLUME
        if volume < config.MIN_VOLUME:
            return config.MIN_VOLUME

        return round(volume, config.VOLUME_ROUND_DIGITS)

    def change_window_size(self):
        self.window_mode_number += 1
        if self.window_mode_number >= len(config.WINDOW_MODES):
            self.window_mode_number = 0

        self.apply_window_mode()
        self.save_settings()

    def apply_window_mode(self):
        mode = config.WINDOW_MODES[self.window_mode_number]
        mode_type = mode[config.WINDOW_MODE_TYPE_INDEX]
        width = mode[config.WINDOW_MODE_WIDTH_INDEX]
        height = mode[config.WINDOW_MODE_HEIGHT_INDEX]

        self.view.set_window_mode(mode_type, width, height)

    def get_window_mode_text(self):
        mode = config.WINDOW_MODES[self.window_mode_number]
        return mode[config.WINDOW_MODE_TEXT_INDEX]

    def load_settings(self):
        settings = self.get_default_settings()

        if not os.path.exists(config.SETTINGS_FILE):
            return settings

        try:
            with open(config.SETTINGS_FILE, "r", encoding=config.SETTINGS_ENCODING) as file:
                saved_settings = json.load(file)
        except (OSError, ValueError):
            return settings

        if not isinstance(saved_settings, dict):
            return settings

        for key in settings:
            if key in saved_settings:
                settings[key] = saved_settings[key]

        settings[config.SETTING_MUSIC_ENABLED] = self.fix_bool(
            settings[config.SETTING_MUSIC_ENABLED],
            config.DEFAULT_MUSIC_ENABLED,
        )
        settings[config.SETTING_SOUND_ENABLED] = self.fix_bool(
            settings[config.SETTING_SOUND_ENABLED],
            config.DEFAULT_SOUND_ENABLED,
        )
        settings[config.SETTING_MUSIC_VOLUME] = self.fix_volume(
            settings[config.SETTING_MUSIC_VOLUME],
            config.DEFAULT_MUSIC_VOLUME,
        )
        settings[config.SETTING_SOUND_VOLUME] = self.fix_volume(
            settings[config.SETTING_SOUND_VOLUME],
            config.DEFAULT_SOUND_VOLUME,
        )
        settings[config.SETTING_WINDOW_MODE_NUMBER] = self.fix_window_mode_number(
            settings[config.SETTING_WINDOW_MODE_NUMBER]
        )

        return settings

    def save_settings(self):
        settings = {
            config.SETTING_MUSIC_ENABLED: self.music_enabled,
            config.SETTING_SOUND_ENABLED: self.sound_enabled,
            config.SETTING_MUSIC_VOLUME: self.music_volume,
            config.SETTING_SOUND_VOLUME: self.sound_volume,
            config.SETTING_WINDOW_MODE_NUMBER: self.window_mode_number,
        }

        with open(
            config.SETTINGS_FILE,
            "w",
            encoding=config.SETTINGS_ENCODING,
            newline="\r\n",
        ) as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

    def get_default_settings(self):
        return {
            config.SETTING_MUSIC_ENABLED: config.DEFAULT_MUSIC_ENABLED,
            config.SETTING_SOUND_ENABLED: config.DEFAULT_SOUND_ENABLED,
            config.SETTING_MUSIC_VOLUME: config.DEFAULT_MUSIC_VOLUME,
            config.SETTING_SOUND_VOLUME: config.DEFAULT_SOUND_VOLUME,
            config.SETTING_WINDOW_MODE_NUMBER: config.DEFAULT_WINDOW_MODE_NUMBER,
        }

    def fix_bool(self, value, default_value):
        if not isinstance(value, bool):
            return default_value

        return value

    def fix_volume(self, volume, default_volume):
        if isinstance(volume, bool):
            return default_volume
        if not isinstance(volume, int) and not isinstance(volume, float):
            return default_volume
        if volume < config.MIN_VOLUME:
            return config.MIN_VOLUME
        if volume > config.MAX_VOLUME:
            return config.MAX_VOLUME

        return round(volume, config.VOLUME_ROUND_DIGITS)

    def fix_window_mode_number(self, number):
        if isinstance(number, bool):
            return config.DEFAULT_WINDOW_MODE_NUMBER
        if not isinstance(number, int):
            return config.DEFAULT_WINDOW_MODE_NUMBER
        if number < 0 or number >= len(config.WINDOW_MODES):
            return config.DEFAULT_WINDOW_MODE_NUMBER

        return number
