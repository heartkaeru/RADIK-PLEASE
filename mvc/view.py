import pygame

import config
from systems import procedural
from mvc import model


class Screen:
    """
    Класс, отвечающий за отрисовку графики.
    Управляет окном игры, загрузкой картинок, звуков, шрифтов и рисованием всех экранов.
    Никакой логики (кто прав, кто виноват) тут нет, только картинки.
    """
    def __init__(self):
        self.width = config.DEFAULT_WINDOW_WIDTH
        self.height = config.DEFAULT_WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(config.GAME_TITLE)
        self.myfont = self.create_font(config.GAME_FONT_SIZE)
        self.title_font = self.create_font(config.TITLE_FONT_SIZE)
        self.button_font = self.create_font(config.BUTTON_FONT_SIZE)
        try:
            self.instruction_font = pygame.font.Font(
                config.INSTRUCTION_FONT_PATH, config.INSTRUCTION_FONT_SIZE
            )
        except Exception:
            self.instruction_font = self.create_font(
                config.INSTRUCTION_FONT_SIZE
            )
        self.student_card_font = self.create_font(
            config.STUDENT_CARD_FONT_SIZE
        )

        icon = pygame.image.load(config.ICON_PATH)
        pygame.display.set_icon(icon)

        self.background_image = pygame.image.load(
            config.BACKGROUND_PATH
        ).convert()
        self.game_width = self.background_image.get_width()
        self.game_height = self.background_image.get_height()
        self.game_scene = pygame.Surface(
            (self.game_width, self.game_height)
        ).convert()
        self.game_rect = None
        self.update_game_rect()

        table_image = pygame.image.load(config.TABLE_PATH).convert_alpha()
        self.table = pygame.transform.scale(
            table_image, (config.TABLE_WIDTH, config.TABLE_HEIGHT)
        )

        self.allow_button_image = self.create_image_button(
            config.ALLOW_BUTTON_PATH, config.ALLOW_BUTTON_SIZE
        )
        self.allow_button_pressed_image = self.create_image_button(
            config.ALLOW_BUTTON_PRESSED_PATH, config.ALLOW_BUTTON_SIZE
        )

        self.deny_button_image = self.create_image_button(
            config.DENY_BUTTON_PATH, config.DENY_BUTTON_SIZE
        )
        self.deny_button_pressed_image = self.create_image_button(
            config.DENY_BUTTON_PRESSED_PATH, config.DENY_BUTTON_SIZE
        )

        self.person_images = {}
        self.walk_frames = {}

        for person_id in ["male", "female", "professor"]:
            person_img = pygame.image.load(
                f"assets/images/{person_id}/straight.png"
            ).convert_alpha()
            scale_factor = config.PERSON_RECT_HEIGHT / person_img.get_height()
            new_width = int(person_img.get_width() * scale_factor)
            self.person_images[person_id] = pygame.transform.scale(
                person_img, (new_width, config.PERSON_RECT_HEIGHT)
            )

            frames = []
            for name in ["left.png", "left2.png"]:
                img = pygame.image.load(
                    f"assets/images/{person_id}/{name}"
                ).convert_alpha()
                frames.append(
                    pygame.transform.scale(
                        img,
                        (
                            int(img.get_width() * scale_factor),
                            config.PERSON_RECT_HEIGHT,
                        ),
                    )
                )
            self.walk_frames[person_id] = frames

        self.person_rect = pygame.Rect(
            config.PERSON_RECT_X,
            config.PERSON_RECT_Y,
            config.PERSON_RECT_WIDTH,
            config.PERSON_RECT_HEIGHT,
        )
        self.instruction_book_rect = pygame.Rect(
            config.INSTRUCTION_BOOK_X,
            config.INSTRUCTION_BOOK_Y,
            config.INSTRUCTION_BOOK_WIDTH,
            config.INSTRUCTION_BOOK_HEIGHT,
        )
        self.student_card_rect = pygame.Rect(
            config.STUDENT_CARD_X,
            config.STUDENT_CARD_Y,
            config.STUDENT_CARD_WIDTH,
            config.STUDENT_CARD_HEIGHT,
        )

        student_card_img = pygame.image.load(
            config.STUDENT_CARD_PATH
        ).convert_alpha()
        self.student_card_image = pygame.transform.scale(
            student_card_img,
            (config.STUDENT_CARD_WIDTH, config.STUDENT_CARD_HEIGHT),
        )

        try:
            instruction_bg_img = pygame.image.load(
                config.INSTRUCTION_BG_PATH
            ).convert_alpha()
            self.instruction_bg_image = pygame.transform.scale(
                instruction_bg_img,
                (
                    config.INSTRUCTION_PANEL_WIDTH,
                    config.INSTRUCTION_PANEL_HEIGHT,
                ),
            )
        except Exception:
            self.instruction_bg_image = None

        try:
            speech_bubble_img = pygame.image.load(
                config.SPEECH_BUBBLE_PATH
            ).convert_alpha()
            self.speech_bubble_image = pygame.transform.scale(
                speech_bubble_img, (400, 250)
            )
        except Exception:
            self.speech_bubble_image = None

        self.allow_button_rect = pygame.Rect(
            config.ALLOW_BUTTON_X,
            config.ALLOW_BUTTON_Y,
            config.ALLOW_BUTTON_SIZE,
            config.ALLOW_BUTTON_SIZE,
        )
        self.deny_button_rect = pygame.Rect(
            config.DENY_BUTTON_X,
            config.DENY_BUTTON_Y,
            config.DENY_BUTTON_SIZE,
            config.DENY_BUTTON_SIZE,
        )

        self.menu_buttons = {}
        self.settings_buttons = {}
        self.settings_sliders = {}
        self.update_buttons()

        self.running = True
        self.clock = pygame.time.Clock()
        self.procedural_cache = {}

    def create_font(self, size: int) -> pygame.font.Font:
        font = pygame.font.SysFont(config.FONT_NAME, size)

        if font is None:
            return pygame.font.Font(None, size)

        return font

    def set_window_mode(self, mode_type: str, width: int, height: int) -> None:
        if mode_type == config.WINDOW_MODE_FULLSCREEN:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif mode_type == config.WINDOW_MODE_BORDERED_FULLSCREEN:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode(
                (info.current_w, info.current_h)
            )
        else:
            self.screen = pygame.display.set_mode((width, height))

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.update_game_rect()
        self.update_buttons()

    def update_game_rect(self) -> None:
        self.game_rect = pygame.Rect(0, 0, self.width, self.height)

    def update_buttons(self) -> None:
        """Обновляет позиционирование всех кнопок и слайдеров в зависимости от размера окна."""
        self.last_has_save = None
        self.update_menu_buttons(True)
        self.settings_buttons = {
            config.BUTTON_MUSIC: self.create_ui_element(
                0,
                config.SETTINGS_FIRST_BUTTON_Y,
                config.SETTINGS_BUTTON_GAP,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            ),
            config.BUTTON_SOUND: self.create_ui_element(
                2,
                config.SETTINGS_FIRST_BUTTON_Y,
                config.SETTINGS_BUTTON_GAP,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            ),
            config.BUTTON_WINDOW_SIZE: self.create_ui_element(
                4,
                config.SETTINGS_FIRST_BUTTON_Y,
                config.SETTINGS_BUTTON_GAP,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            ),
            config.BUTTON_BACK: self.create_ui_element(
                5,
                config.SETTINGS_FIRST_BUTTON_Y,
                config.SETTINGS_BUTTON_GAP,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            ),
        }
        self.settings_sliders = {
            config.SLIDER_MUSIC_VOLUME: self.create_ui_element(
                1,
                config.SETTINGS_FIRST_BUTTON_Y,
                config.SETTINGS_BUTTON_GAP,
                config.SLIDER_TRACK_WIDTH,
                config.SLIDER_TRACK_HEIGHT,
                config.SLIDER_TRACK_OFFSET_Y,
            ),
            config.SLIDER_SOUND_VOLUME: self.create_ui_element(
                3,
                config.SETTINGS_FIRST_BUTTON_Y,
                config.SETTINGS_BUTTON_GAP,
                config.SLIDER_TRACK_WIDTH,
                config.SLIDER_TRACK_HEIGHT,
                config.SLIDER_TRACK_OFFSET_Y,
            ),
        }

    def update_menu_buttons(self, has_save: bool) -> None:
        """Обновляет кнопки главного меню в зависимости от наличия сохранения."""
        if getattr(self, "last_has_save", None) == has_save:
            return
        self.last_has_save = has_save

        self.menu_buttons = {
            config.BUTTON_START: self.create_ui_element(
                0,
                config.MENU_FIRST_BUTTON_Y,
                config.MENU_BUTTON_GAP,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            ),
        }

        button_idx = 1
        if has_save:
            self.menu_buttons[config.BUTTON_CONTINUE] = self.create_ui_element(
                button_idx,
                config.MENU_FIRST_BUTTON_Y,
                config.MENU_BUTTON_GAP,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            )
            button_idx += 1

        self.menu_buttons[config.BUTTON_SETTINGS] = self.create_ui_element(
            button_idx,
            config.MENU_FIRST_BUTTON_Y,
            config.MENU_BUTTON_GAP,
            config.MENU_BUTTON_WIDTH,
            config.MENU_BUTTON_HEIGHT,
        )
        button_idx += 1
        self.menu_buttons[config.BUTTON_EXIT] = self.create_ui_element(
            button_idx,
            config.MENU_FIRST_BUTTON_Y,
            config.MENU_BUTTON_GAP,
            config.MENU_BUTTON_WIDTH,
            config.MENU_BUTTON_HEIGHT,
        )

    def create_image_button(self, path: str, size: int) -> pygame.Surface:
        """Загружает и масштабирует изображение для кнопки-печати."""
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))

    def create_ui_element(
        self,
        number: int,
        start_y: int,
        gap_y: int,
        width: int,
        height: int,
        offset_y: int = 0,
    ) -> pygame.Rect:
        """
        Универсальная фабрика для создания UI-элементов (кнопок, слайдеров).
        Рассчитывает положение элемента по центру экрана с заданным смещением.
        """
        x = self.width // 2 - width // 2
        y = start_y + number * gap_y + offset_y
        return pygame.Rect(x, y, width, height)

    def draw_menu(self, has_save: bool) -> None:
        self.update_menu_buttons(has_save)

        self.draw_menu_background()
        self.draw_title(config.MENU_TITLE_TEXT)

        self.draw_button(
            self.menu_buttons[config.BUTTON_START], config.MENU_START_TEXT
        )
        if config.BUTTON_CONTINUE in self.menu_buttons:
            self.draw_button(
                self.menu_buttons[config.BUTTON_CONTINUE],
                config.MENU_CONTINUE_TEXT,
                True,
            )
        self.draw_button(
            self.menu_buttons[config.BUTTON_SETTINGS],
            config.MENU_SETTINGS_TEXT,
        )
        self.draw_button(
            self.menu_buttons[config.BUTTON_EXIT], config.MENU_EXIT_TEXT
        )

    def draw_settings(
        self,
        music_enabled: bool,
        sound_enabled: bool,
        music_volume: float,
        sound_volume: float,
    ) -> None:
        music_text = self.get_setting_text(
            config.MUSIC_SETTING_TEXT, music_enabled
        )
        sound_text = self.get_setting_text(
            config.SOUND_SETTING_TEXT, sound_enabled
        )
        music_volume_text = self.get_volume_text(
            config.MUSIC_VOLUME_TEXT, music_volume
        )
        sound_volume_text = self.get_volume_text(
            config.SOUND_VOLUME_TEXT, sound_volume
        )

        self.draw_menu_background()
        self.draw_title(config.SETTINGS_TITLE_TEXT)

        self.draw_button(
            self.settings_buttons[config.BUTTON_MUSIC], music_text
        )
        self.draw_slider(
            self.settings_sliders[config.SLIDER_MUSIC_VOLUME],
            music_volume_text,
            music_volume,
        )
        self.draw_button(
            self.settings_buttons[config.BUTTON_SOUND], sound_text
        )
        self.draw_slider(
            self.settings_sliders[config.SLIDER_SOUND_VOLUME],
            sound_volume_text,
            sound_volume,
        )
        self.draw_button(
            self.settings_buttons[config.BUTTON_BACK], config.MENU_BACK_TEXT
        )

    def draw_game(
        self,
        balance: int,
        day_number: int,
        date_string: str,
        time_string: str,
        person=None,
        visitor_visible: bool = True,
        student_card_open: bool = False,
        active_effects=None,
        instruction_open: bool = False,
        instruction_lines=None,
        visitor_position=None,
        student_card_on_table: bool = True,
        allow_pressed: bool = False,
        deny_pressed: bool = False,
        visitor_state: str = "NONE",
        speech_bubble_text: str = None,
    ) -> None:
        """
        Отрисовывает основной игровой экран: стол, посетителя, документы, инструменты и информацию.
        """
        self.screen.fill(config.MENU_BACKGROUND_COLOR)
        self.draw_game_scene(
            person,
            visitor_visible,
            visitor_position,
            student_card_on_table,
            allow_pressed,
            deny_pressed,
            visitor_state,
            speech_bubble_text,
        )

        scaled_scene = pygame.transform.scale(
            self.game_scene, self.game_rect.size
        )
        self.screen.blit(scaled_scene, self.game_rect)
        self.draw_balance(balance)
        self.draw_day_info(day_number, date_string, time_string)

        if active_effects:
            for effect in active_effects:
                effect.draw(self.screen)

        if student_card_open and person is not None:
            self.draw_student_card_panel(person)

        if instruction_open:
            self.draw_instruction(instruction_lines)

    def draw_game_scene(
        self,
        person,
        visitor_visible: bool,
        visitor_position,
        student_card_on_table: bool,
        allow_pressed: bool = False,
        deny_pressed: bool = False,
        visitor_state: str = "NONE",
        speech_bubble_text: str = None,
    ) -> None:
        """
        Рисуем задний фон (стену кабинета)
        """
        self.game_scene.blit(
            self.background_image, (config.BACKGROUND_X, config.BACKGROUND_Y)
        )

        if visitor_visible:
            person_id = "male"
            if person:
                if person.is_important:
                    person_id = "professor"
                elif person.gender == config.GENDER_FEMALE:
                    person_id = "female"
            person_rect = self.get_person_rect(visitor_position)
            img = self.person_images[person_id]
            if (
                visitor_state in ("WALKING_IN", "WALKING_OUT")
                and visitor_position is not None
            ):
                frame_index = (-int(visitor_position[0]) // 120) % len(
                    self.walk_frames[person_id]
                )
                img = self.walk_frames[person_id][frame_index]
                if frame_index % 2 != 0:
                    person_rect.y -= 10

            person_rect.width = img.get_width()
            person_rect.height = img.get_height()
            self.game_scene.blit(img, person_rect)

            if speech_bubble_text and self.speech_bubble_image:
                bubble_x = person_rect.right - 50
                bubble_y = person_rect.top - 100
                self.game_scene.blit(
                    self.speech_bubble_image, (bubble_x, bubble_y)
                )

                wrapped_lines = self.wrap_text(
                    speech_bubble_text,
                    self.student_card_font,
                    self.speech_bubble_image.get_width() - 60,
                )

                line_height = self.student_card_font.get_height() + 2
                total_text_height = len(wrapped_lines) * line_height
                text_y = bubble_y + 114 - (total_text_height // 2)

                for line in wrapped_lines:
                    text_surface = self.student_card_font.render(
                        line, True, (0, 0, 0)
                    )
                    text_x = (
                        bubble_x
                        + (
                            self.speech_bubble_image.get_width()
                            - text_surface.get_width()
                        )
                        // 2
                    )
                    self.game_scene.blit(text_surface, (text_x, text_y))
                    text_y += line_height

        self.game_scene.blit(self.table, (config.TABLE_X, config.TABLE_Y))
        self.draw_table_tools(allow_pressed, deny_pressed)

        if (
            student_card_on_table
            and person is not None
            and person.document is not None
        ):
            self.game_scene.blit(
                self.student_card_image, self.student_card_rect
            )

    def get_person_rect(self, visitor_position) -> pygame.Rect:
        if visitor_position is None:
            return self.person_rect

        return pygame.Rect(
            int(visitor_position[0]),
            int(visitor_position[1]),
            config.PERSON_RECT_WIDTH,
            config.PERSON_RECT_HEIGHT,
        )

    def draw_menu_background(self) -> None:
        self.screen.fill(config.MENU_BACKGROUND_COLOR)

    def draw_balance(self, balance: int) -> None:
        text = config.BALANCE_TEXT.format(balance=balance)
        label = self.myfont.render(text, True, config.BALANCE_TEXT_COLOR)
        label_rect = label.get_rect(
            topleft=(config.BALANCE_X, config.BALANCE_Y)
        )

        self.screen.blit(label, label_rect)

    def draw_day_info(self, day: int, date_str: str, time_str: str) -> None:
        day_text = config.DAY_TEXT.format(day=day)
        date_text = config.DATE_TEXT.format(date=date_str)
        time_text = config.TIME_TEXT.format(time=time_str)

        label_day = self.myfont.render(day_text, True, (255, 255, 255))
        self.screen.blit(label_day, (config.DAY_INFO_X, config.DAY_INFO_Y))

        label_date = self.myfont.render(date_text, True, (255, 255, 255))
        self.screen.blit(
            label_date,
            (config.DAY_INFO_X, config.DAY_INFO_Y + config.DAY_INFO_GAP_Y),
        )

        label_time = self.myfont.render(time_text, True, (255, 255, 255))
        self.screen.blit(
            label_time,
            (config.DAY_INFO_X, config.DAY_INFO_Y + config.DAY_INFO_GAP_Y * 2),
        )

    def draw_table_tools(
        self, allow_pressed: bool, deny_pressed: bool
    ) -> None:
        if allow_pressed:
            self.game_scene.blit(
                self.allow_button_pressed_image, self.allow_button_rect
            )
        else:
            self.game_scene.blit(
                self.allow_button_image, self.allow_button_rect
            )

        if deny_pressed:
            self.game_scene.blit(
                self.deny_button_pressed_image, self.deny_button_rect
            )
        else:
            self.game_scene.blit(self.deny_button_image, self.deny_button_rect)

    def draw_student_card_panel(self, person) -> None:
        """
        Отрисовка развернутого студенческого билета крупным планом.
        """
        panel = pygame.Rect(
            0,
            0,
            config.STUDENT_CARD_PANEL_WIDTH,
            config.STUDENT_CARD_PANEL_HEIGHT,
        )
        panel.centerx = self.width // 2
        panel.y = config.STUDENT_CARD_PANEL_Y

        seed = person.document.seed if person.document else 0
        is_vip = (
            isinstance(person.document, model.VipDocument)
            if person.document
            else False
        )

        person_id = "male"
        if person:
            if person.is_important:
                person_id = "professor"
            elif person.gender == config.GENDER_FEMALE:
                person_id = "female"
        original_sprite = self.person_images[person_id]

        if seed not in self.procedural_cache:
            bg_surf = procedural.generate_card_background(
                seed, panel.width, panel.height, is_vip
            )
            avatar_surf = procedural.generate_document_photo(
                original_sprite,
                config.STUDENT_CARD_PHOTO_WIDTH,
                config.STUDENT_CARD_PHOTO_HEIGHT,
                seed,
            )
            sig_surf = procedural.generate_signature(
                seed,
                config.STUDENT_CARD_SIGNATURE_WIDTH,
                config.STUDENT_CARD_SIGNATURE_HEIGHT,
            )
            self.procedural_cache[seed] = (bg_surf, avatar_surf, sig_surf)

        bg_surf, avatar_surf, sig_surf = self.procedural_cache[seed]

        self.screen.blit(bg_surf, panel.topleft)
        pygame.draw.rect(
            self.screen, config.STUDENT_CARD_PANEL_BORDER_COLOR, panel, 2
        )

        avatar_x = (
            panel.right
            - config.STUDENT_CARD_PANEL_PADDING
            - config.STUDENT_CARD_PHOTO_WIDTH
        )
        avatar_y = panel.top + config.STUDENT_CARD_PANEL_PADDING
        self.screen.blit(avatar_surf, (avatar_x, avatar_y))

        x = panel.x + config.STUDENT_CARD_PANEL_PADDING
        y = panel.y + config.STUDENT_CARD_PANEL_PADDING
        max_width = panel.width - config.STUDENT_CARD_PANEL_PADDING * 2

        for line in person.document_data():
            wrapped_lines = self.wrap_text(
                line, self.student_card_font, max_width
            )
            for wrapped_line in wrapped_lines:
                text = self.student_card_font.render(
                    wrapped_line,
                    True,
                    config.STUDENT_CARD_PANEL_TEXT_COLOR,
                )
                self.screen.blit(text, (x, y))
                y += (
                    self.student_card_font.get_height()
                    + config.STUDENT_CARD_LINE_GAP
                )

            y += config.STUDENT_CARD_LINE_GAP

        sig_x = panel.left + config.STUDENT_CARD_PANEL_PADDING
        sig_y = (
            panel.bottom
            - config.STUDENT_CARD_PANEL_PADDING
            - config.STUDENT_CARD_SIGNATURE_HEIGHT
        )
        self.screen.blit(sig_surf, (sig_x, sig_y))

    def draw_instruction(self, instruction_lines) -> None:
        if not instruction_lines:
            instruction_lines = {"students": [], "teachers": []}

        panel = pygame.Rect(
            0,
            0,
            config.INSTRUCTION_PANEL_WIDTH,
            config.INSTRUCTION_PANEL_HEIGHT,
        )
        panel.center = (self.width // 2, self.height // 2)

        if self.instruction_bg_image:
            self.screen.blit(self.instruction_bg_image, panel)
        else:
            pygame.draw.rect(
                self.screen, config.INSTRUCTION_PANEL_COLOR, panel
            )
            pygame.draw.rect(
                self.screen, config.INSTRUCTION_BORDER_COLOR, panel, 2
            )

        left_x = panel.x + 240
        left_y = panel.y + 120
        max_width = 340

        for line in instruction_lines.get("students", []):
            left_y = self.draw_text_with_spaces(
                line,
                self.instruction_font,
                config.INSTRUCTION_TEXT_COLOR,
                left_x,
                left_y,
                max_width,
                config.INSTRUCTION_LINE_GAP,
            )

        right_x = panel.centerx + 40
        right_y = panel.y + 120

        for line in instruction_lines.get("teachers", []):
            right_y = self.draw_text_with_spaces(
                line,
                self.instruction_font,
                config.INSTRUCTION_TEXT_COLOR,
                right_x,
                right_y,
                max_width,
                config.INSTRUCTION_LINE_GAP,
            )

    def draw_title(self, text: str) -> None:
        title = self.title_font.render(text, True, config.MENU_TEXT_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, config.TITLE_Y))
        self.screen.blit(title, title_rect)

    def draw_button(
        self, rect: pygame.Rect, text: str, enabled: bool = True
    ) -> None:
        mouse_pos = pygame.mouse.get_pos()
        color = config.BUTTON_COLOR
        text_color = config.BUTTON_TEXT_COLOR

        if not enabled:
            color = config.BUTTON_DISABLED_COLOR
            text_color = config.BUTTON_DISABLED_TEXT_COLOR
        elif rect.collidepoint(mouse_pos):
            color = config.BUTTON_HOVER_COLOR

        pygame.draw.rect(self.screen, color, rect)

        label = self.button_font.render(text, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def draw_slider(self, rect: pygame.Rect, text: str, value: float) -> None:
        label = self.button_font.render(text, True, config.BUTTON_TEXT_COLOR)
        label_rect = label.get_rect(
            center=(self.width // 2, rect.y - config.SLIDER_LABEL_OFFSET_Y)
        )
        self.screen.blit(label, label_rect)

        pygame.draw.rect(self.screen, config.SLIDER_TRACK_COLOR, rect)

        fill_width = int(rect.width * value)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(self.screen, config.SLIDER_FILL_COLOR, fill_rect)

        knob_x = rect.x + fill_width
        knob = pygame.Rect(
            0, 0, config.SLIDER_KNOB_WIDTH, config.SLIDER_KNOB_HEIGHT
        )
        knob.center = (knob_x, rect.centery)
        pygame.draw.rect(self.screen, config.SLIDER_KNOB_COLOR, knob)

    def draw_day_summary(
        self,
        day: int,
        processed: int,
        correct: int,
        mistakes: int,
        earned: int,
        lost: int,
    ) -> None:
        self.draw_menu_background()

        self.draw_title(config.DAY_SUMMARY_TITLE.format(day=day))

        start_y = config.TITLE_Y + 120
        gap_y = 60

        lines = [
            config.DAY_SUMMARY_PROCESSED.format(processed=processed),
            config.DAY_SUMMARY_CORRECT.format(correct=correct),
            config.DAY_SUMMARY_MISTAKES.format(mistakes=mistakes),
            config.DAY_SUMMARY_MONEY_EARNED.format(earned=earned),
            config.DAY_SUMMARY_MONEY_LOST.format(lost=lost),
            config.DAY_SUMMARY_TOTAL.format(total=earned - lost),
        ]

        for i, text in enumerate(lines):
            label = self.myfont.render(text, True, config.MENU_TEXT_COLOR)
            label_rect = label.get_rect(
                center=(self.width // 2, start_y + i * gap_y)
            )
            self.screen.blit(label, label_rect)

        advice = self.myfont.render(
            config.DAY_SUMMARY_ADVICE, True, config.BUTTON_DISABLED_TEXT_COLOR
        )
        advice_rect = advice.get_rect(
            center=(self.width // 2, start_y + len(lines) * gap_y + 40)
        )
        self.screen.blit(advice, advice_rect)

        if config.BUTTON_NEXT_DAY not in self.menu_buttons:
            self.menu_buttons[config.BUTTON_NEXT_DAY] = pygame.Rect(
                self.width // 2 - config.MENU_BUTTON_WIDTH // 2,
                self.height - 150,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            )

        self.draw_button(
            self.menu_buttons[config.BUTTON_NEXT_DAY],
            config.DAY_SUMMARY_NEXT_TEXT,
        )

    def draw_tutorial(self) -> None:
        self.draw_menu_background()
        self.draw_title(config.TUTORIAL_TITLE)

        start_y = config.TITLE_Y + 120
        gap_y = 60

        for i, text in enumerate(config.TUTORIAL_TEXT):
            label = self.myfont.render(text, True, config.MENU_TEXT_COLOR)
            label_rect = label.get_rect(
                center=(self.width // 2, start_y + i * gap_y)
            )
            self.screen.blit(label, label_rect)

        if config.BUTTON_TUTORIAL_CONTINUE not in self.menu_buttons:
            self.menu_buttons[config.BUTTON_TUTORIAL_CONTINUE] = pygame.Rect(
                self.width // 2 - config.MENU_BUTTON_WIDTH // 2,
                self.height - 150,
                config.MENU_BUTTON_WIDTH,
                config.MENU_BUTTON_HEIGHT,
            )

        self.draw_button(
            self.menu_buttons[config.BUTTON_TUTORIAL_CONTINUE],
            config.TUTORIAL_CONTINUE_TEXT,
        )

    def draw_fade(self, alpha: float) -> None:
        if alpha <= 0:
            return
        if alpha > 255:
            alpha = 255

        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(int(alpha))
        self.screen.blit(fade_surface, (0, 0))

    def get_setting_text(self, template: str, enabled: bool) -> str:
        if enabled:
            state = config.SETTING_ON_TEXT
        else:
            state = config.SETTING_OFF_TEXT

        return template.format(state=state)

    def get_volume_text(self, template: str, volume: float) -> str:
        volume_percent = int(volume * config.VOLUME_PERCENT)
        return template.format(volume=volume_percent)

    def draw_text_with_spaces(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple,
        x: int,
        y: int,
        max_width: int,
        line_gap: int,
    ) -> int:
        if not text:
            return y + font.get_height() + line_gap

        words = text.split()
        space_width = font.size(" ")[0]
        if space_width < 5:
            space_width = 12

        current_x = x
        current_y = y
        max_line_height = font.get_height()

        for word in words:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()

            if current_x + word_width > x + max_width and current_x != x:
                current_x = x
                current_y += max_line_height + line_gap

            self.screen.blit(word_surface, (current_x, current_y))
            current_x += word_width + space_width

        return current_y + max_line_height + line_gap

    def wrap_text(
        self, text: str, font: pygame.font.Font, max_width: int
    ) -> list:
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if current_line == "":
                new_line = word
            else:
                new_line = current_line + " " + word

            if font.size(new_line)[0] <= max_width:
                current_line = new_line
            else:
                if current_line != "":
                    lines.append(current_line)
                current_line = word

        if current_line != "":
            lines.append(current_line)

        return lines

    def get_game_mouse_pos(self, mouse_pos):
        if not self.game_rect.collidepoint(mouse_pos):
            return None

        game_x = int(
            (mouse_pos[0] - self.game_rect.x)
            * self.game_width
            / self.game_rect.width
        )
        game_y = int(
            (mouse_pos[1] - self.game_rect.y)
            * self.game_height
            / self.game_rect.height
        )

        return game_x, game_y

    def is_instruction_book_clicked(self, mouse_pos) -> bool:
        game_pos = self.get_game_mouse_pos(mouse_pos)

        if game_pos is None:
            return False

        return self.instruction_book_rect.collidepoint(game_pos)

    def is_student_card_clicked(self, mouse_pos) -> bool:
        game_pos = self.get_game_mouse_pos(mouse_pos)

        if game_pos is None:
            return False

        return self.student_card_rect.collidepoint(game_pos)

    def is_allow_button_clicked(self, mouse_pos) -> bool:
        game_pos = self.get_game_mouse_pos(mouse_pos)

        if game_pos is None:
            return False

        return self.allow_button_rect.collidepoint(game_pos)

    def is_deny_button_clicked(self, mouse_pos) -> bool:
        game_pos = self.get_game_mouse_pos(mouse_pos)

        if game_pos is None:
            return False

        return self.deny_button_rect.collidepoint(game_pos)

    def update_screen(self) -> None:
        pygame.display.update()
        self.clock.tick(60)
