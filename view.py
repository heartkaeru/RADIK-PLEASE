import pygame

import config


class Screen:
    def __init__(self):
        self.width = config.DEFAULT_WINDOW_WIDTH
        self.height = config.DEFAULT_WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(config.GAME_TITLE)
        self.myfont = self.create_font(config.GAME_FONT_SIZE)
        self.title_font = self.create_font(config.TITLE_FONT_SIZE)
        self.button_font = self.create_font(config.BUTTON_FONT_SIZE)
        self.instruction_font = self.create_font(config.INSTRUCTION_FONT_SIZE)
        self.student_card_font = self.create_font(config.STUDENT_CARD_FONT_SIZE)

        icon = pygame.image.load(config.ICON_PATH)
        pygame.display.set_icon(icon)

        self.background_image = pygame.image.load(config.BACKGROUND_PATH).convert()
        self.game_width = self.background_image.get_width()
        self.game_height = self.background_image.get_height()
        self.game_scene = pygame.Surface((self.game_width, self.game_height)).convert()
        self.game_rect = None
        self.update_game_rect()

        table_image = pygame.image.load(config.TABLE_PATH).convert_alpha()
        self.table = pygame.transform.scale(table_image, (config.TABLE_WIDTH, config.TABLE_HEIGHT))

        allow_img = pygame.image.load(config.ALLOW_BUTTON_PATH).convert_alpha()
        self.allow_button_image = pygame.transform.scale(allow_img, (config.ALLOW_BUTTON_SIZE, config.ALLOW_BUTTON_SIZE))
        allow_pressed_img = pygame.image.load(config.ALLOW_BUTTON_PRESSED_PATH).convert_alpha()
        self.allow_button_pressed_image = pygame.transform.scale(allow_pressed_img, (config.ALLOW_BUTTON_SIZE, config.ALLOW_BUTTON_SIZE))

        deny_img = pygame.image.load(config.DENY_BUTTON_PATH).convert_alpha()
        self.deny_button_image = pygame.transform.scale(deny_img, (config.DENY_BUTTON_SIZE, config.DENY_BUTTON_SIZE))
        deny_pressed_img = pygame.image.load(config.DENY_BUTTON_PRESSED_PATH).convert_alpha()
        self.deny_button_pressed_image = pygame.transform.scale(deny_pressed_img, (config.DENY_BUTTON_SIZE, config.DENY_BUTTON_SIZE))

        self.person_images = {}
        self.walk_frames = {}
        
        for person_id in ["male", "female", "professor"]:
            person_img = pygame.image.load(f"assets/images/{person_id}/straight.png").convert_alpha()
            self.person_images[person_id] = pygame.transform.scale(person_img, (config.PERSON_RECT_WIDTH, config.PERSON_RECT_HEIGHT))

            frames = []
            for name in ["left.png", "left2.png"]:
                img = pygame.image.load(f"assets/images/{person_id}/{name}").convert_alpha()
                frames.append(pygame.transform.scale(img, (config.PERSON_RECT_WIDTH, config.PERSON_RECT_HEIGHT)))
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

        student_card_img = pygame.image.load(config.STUDENT_CARD_PATH).convert_alpha()
        self.student_card_image = pygame.transform.scale(student_card_img, (config.STUDENT_CARD_WIDTH, config.STUDENT_CARD_HEIGHT))
        
        try:
            instruction_bg_img = pygame.image.load(config.INSTRUCTION_BG_PATH).convert_alpha()
            self.instruction_bg_image = pygame.transform.scale(instruction_bg_img, (config.INSTRUCTION_PANEL_WIDTH, config.INSTRUCTION_PANEL_HEIGHT))
        except Exception:
            self.instruction_bg_image = None

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
            self.screen = pygame.display.set_mode((info.current_w, info.current_h))
        else:
            self.screen = pygame.display.set_mode((width, height))

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.update_game_rect()
        self.update_buttons()

    def update_game_rect(self) -> None:
        self.game_rect = pygame.Rect(0, 0, self.width, self.height)

    def update_buttons(self) -> None:
        self.last_has_save = None
        self.update_menu_buttons(True)
        self.settings_buttons = {
            config.BUTTON_MUSIC: self.create_settings_button(0),
            config.BUTTON_SOUND: self.create_settings_button(2),
            config.BUTTON_WINDOW_SIZE: self.create_settings_button(4),
            config.BUTTON_BACK: self.create_settings_button(5),
        }
        self.settings_sliders = {
            config.SLIDER_MUSIC_VOLUME: self.create_settings_slider(1),
            config.SLIDER_SOUND_VOLUME: self.create_settings_slider(3),
        }

    def update_menu_buttons(self, has_save: bool) -> None:
        if getattr(self, "last_has_save", None) == has_save:
            return
        self.last_has_save = has_save

        self.menu_buttons = {
            config.BUTTON_START: self.create_button(0),
        }
        
        button_idx = 1
        if has_save:
            self.menu_buttons[config.BUTTON_CONTINUE] = self.create_button(button_idx)
            button_idx += 1
            
        self.menu_buttons[config.BUTTON_SETTINGS] = self.create_button(button_idx)
        button_idx += 1
        self.menu_buttons[config.BUTTON_EXIT] = self.create_button(button_idx)

    def create_button(self, number: int) -> pygame.Rect:
        x = self.width // 2 - config.MENU_BUTTON_WIDTH // 2
        y = config.MENU_FIRST_BUTTON_Y + number * config.MENU_BUTTON_GAP
        return pygame.Rect(x, y, config.MENU_BUTTON_WIDTH, config.MENU_BUTTON_HEIGHT)

    def create_settings_button(self, number: int) -> pygame.Rect:
        x = self.width // 2 - config.MENU_BUTTON_WIDTH // 2
        y = config.SETTINGS_FIRST_BUTTON_Y + number * config.SETTINGS_BUTTON_GAP
        return pygame.Rect(x, y, config.MENU_BUTTON_WIDTH, config.MENU_BUTTON_HEIGHT)

    def create_settings_slider(self, number: int) -> pygame.Rect:
        x = self.width // 2 - config.SLIDER_TRACK_WIDTH // 2
        y = config.SETTINGS_FIRST_BUTTON_Y + number * config.SETTINGS_BUTTON_GAP
        y += config.SLIDER_TRACK_OFFSET_Y
        return pygame.Rect(x, y, config.SLIDER_TRACK_WIDTH, config.SLIDER_TRACK_HEIGHT)

    def draw_menu(self, has_save: bool) -> None:
        self.update_menu_buttons(has_save)
        
        self.draw_menu_background()
        self.draw_title(config.MENU_TITLE_TEXT)

        self.draw_button(self.menu_buttons[config.BUTTON_START], config.MENU_START_TEXT)
        if config.BUTTON_CONTINUE in self.menu_buttons:
            self.draw_button(
                self.menu_buttons[config.BUTTON_CONTINUE],
                config.MENU_CONTINUE_TEXT,
                True,
            )
        self.draw_button(self.menu_buttons[config.BUTTON_SETTINGS], config.MENU_SETTINGS_TEXT)
        self.draw_button(self.menu_buttons[config.BUTTON_EXIT], config.MENU_EXIT_TEXT)

        self.update_screen()

    def draw_settings(
        self,
        music_enabled: bool,
        sound_enabled: bool,
        music_volume: float,
        sound_volume: float,
    ) -> None:
        music_text = self.get_setting_text(config.MUSIC_SETTING_TEXT, music_enabled)
        sound_text = self.get_setting_text(config.SOUND_SETTING_TEXT, sound_enabled)
        music_volume_text = self.get_volume_text(config.MUSIC_VOLUME_TEXT, music_volume)
        sound_volume_text = self.get_volume_text(config.SOUND_VOLUME_TEXT, sound_volume)

        self.draw_menu_background()
        self.draw_title(config.SETTINGS_TITLE_TEXT)

        self.draw_button(self.settings_buttons[config.BUTTON_MUSIC], music_text)
        self.draw_slider(
            self.settings_sliders[config.SLIDER_MUSIC_VOLUME],
            music_volume_text,
            music_volume,
        )
        self.draw_button(self.settings_buttons[config.BUTTON_SOUND], sound_text)
        self.draw_slider(
            self.settings_sliders[config.SLIDER_SOUND_VOLUME],
            sound_volume_text,
            sound_volume,
        )
        self.draw_button(self.settings_buttons[config.BUTTON_BACK], config.MENU_BACK_TEXT)

        self.update_screen()

    def draw_game(
        self,
        balance: int,
        day_number: int,
        date_string: str,
        time_string: str,
        person=None,
        visitor_visible: bool = True,
        student_card_open: bool = False,
        result_text: str = "",
        result_is_correct: bool = True,
        instruction_open: bool = False,
        instruction_lines=None,
        visitor_position=None,
        student_card_on_table: bool = True,
        allow_pressed: bool = False,
        deny_pressed: bool = False,
        visitor_state: str = "NONE",
    ) -> None:
        self.screen.fill(config.MENU_BACKGROUND_COLOR)
        self.draw_game_scene(person, visitor_visible, visitor_position, student_card_on_table, allow_pressed, deny_pressed, visitor_state)

        scaled_scene = pygame.transform.scale(self.game_scene, self.game_rect.size)
        self.screen.blit(scaled_scene, self.game_rect)
        self.draw_balance(balance)
        self.draw_day_info(day_number, date_string, time_string)
        self.draw_result(result_text, result_is_correct)

        if student_card_open and person is not None:
            self.draw_student_card_panel(person)

        if instruction_open:
            self.draw_instruction(instruction_lines)

        self.update_screen()

    def draw_game_scene(
        self,
        person,
        visitor_visible: bool,
        visitor_position,
        student_card_on_table: bool,
        allow_pressed: bool = False,
        deny_pressed: bool = False,
        visitor_state: str = "NONE",
    ) -> None:
        self.game_scene.blit(self.background_image, (config.BACKGROUND_X, config.BACKGROUND_Y))

        if visitor_visible:
            person_id = "male"
            if person:
                if person.is_important:
                    person_id = "professor"
                elif person.gender == config.GENDER_FEMALE:
                    person_id = "female"
            person_rect = self.get_person_rect(visitor_position)
            img = self.person_images[person_id]
            if visitor_state in ("WALKING_IN", "WALKING_OUT") and visitor_position is not None:
                frame_index = (-int(visitor_position[0]) // 120) % len(self.walk_frames[person_id])
                img = self.walk_frames[person_id][frame_index]
                # Add a small bobbing effect for walking
                if frame_index % 2 != 0:
                    person_rect.y -= 10
            self.game_scene.blit(img, person_rect)

        self.game_scene.blit(self.table, (config.TABLE_X, config.TABLE_Y))
        self.draw_table_tools(allow_pressed, deny_pressed)

        if student_card_on_table and person is not None and person.document is not None:
            self.game_scene.blit(self.student_card_image, self.student_card_rect)

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
        label_rect = label.get_rect(topleft=(config.BALANCE_X, config.BALANCE_Y))

        self.screen.blit(label, label_rect)

    def draw_day_info(self, day: int, date_str: str, time_str: str) -> None:
        day_text = config.DAY_TEXT.format(day=day)
        date_text = config.DATE_TEXT.format(date=date_str)
        time_text = config.TIME_TEXT.format(time=time_str)

        label_day = self.myfont.render(day_text, True, (255, 255, 255))
        self.screen.blit(label_day, (config.DAY_INFO_X, config.DAY_INFO_Y))

        label_date = self.myfont.render(date_text, True, (255, 255, 255))
        self.screen.blit(label_date, (config.DAY_INFO_X, config.DAY_INFO_Y + config.DAY_INFO_GAP_Y))

        label_time = self.myfont.render(time_text, True, (255, 255, 255))
        self.screen.blit(label_time, (config.DAY_INFO_X, config.DAY_INFO_Y + config.DAY_INFO_GAP_Y * 2))

    def draw_result(self, text: str, is_correct: bool) -> None:
        if text == "":
            return

        color = config.RESULT_CORRECT_COLOR
        if not is_correct:
            color = config.RESULT_MISTAKE_COLOR

        label = self.myfont.render(text, True, color)
        label_rect = label.get_rect(topleft=(config.RESULT_X, config.RESULT_Y))
        self.screen.blit(label, label_rect)

    def draw_table_tools(self, allow_pressed: bool, deny_pressed: bool) -> None:
        if allow_pressed:
            self.game_scene.blit(self.allow_button_pressed_image, self.allow_button_rect)
        else:
            self.game_scene.blit(self.allow_button_image, self.allow_button_rect)
            
        if deny_pressed:
            self.game_scene.blit(self.deny_button_pressed_image, self.deny_button_rect)
        else:
            self.game_scene.blit(self.deny_button_image, self.deny_button_rect)

    def draw_student_card_panel(self, person) -> None:
        panel = pygame.Rect(0, 0, config.STUDENT_CARD_PANEL_WIDTH, config.STUDENT_CARD_PANEL_HEIGHT)
        panel.centerx = self.width // 2
        panel.y = config.STUDENT_CARD_PANEL_Y

        pygame.draw.rect(self.screen, config.STUDENT_CARD_PANEL_COLOR, panel)
        pygame.draw.rect(self.screen, config.STUDENT_CARD_PANEL_BORDER_COLOR, panel, 2)

        x = panel.x + config.STUDENT_CARD_PANEL_PADDING
        y = panel.y + config.STUDENT_CARD_PANEL_PADDING
        max_width = panel.width - config.STUDENT_CARD_PANEL_PADDING * 2

        for line in person.document_data():
            wrapped_lines = self.wrap_text(line, self.student_card_font, max_width)
            for wrapped_line in wrapped_lines:
                text = self.student_card_font.render(
                    wrapped_line,
                    True,
                    config.STUDENT_CARD_PANEL_TEXT_COLOR,
                )
                self.screen.blit(text, (x, y))
                y += self.student_card_font.get_height() + config.STUDENT_CARD_LINE_GAP

            y += config.STUDENT_CARD_LINE_GAP

    def draw_instruction(self, instruction_lines) -> None:
        if instruction_lines is None:
            instruction_lines = []

        panel = pygame.Rect(0, 0, config.INSTRUCTION_PANEL_WIDTH, config.INSTRUCTION_PANEL_HEIGHT)
        panel.center = (self.width // 2, self.height // 2)

        if self.instruction_bg_image:
            self.screen.blit(self.instruction_bg_image, panel)
        else:
            pygame.draw.rect(self.screen, config.INSTRUCTION_PANEL_COLOR, panel)
            pygame.draw.rect(self.screen, config.INSTRUCTION_BORDER_COLOR, panel, 2)

        title = self.button_font.render(config.INSTRUCTION_TITLE_TEXT, True, config.INSTRUCTION_TEXT_COLOR)
        title_rect = title.get_rect(center=(panel.centerx, panel.y + config.INSTRUCTION_PANEL_PADDING))
        self.screen.blit(title, title_rect)

        x = panel.x + config.INSTRUCTION_PANEL_PADDING
        y = panel.y + config.INSTRUCTION_TITLE_GAP
        max_width = panel.width - config.INSTRUCTION_PANEL_PADDING * 2

        for line in instruction_lines:
            wrapped_lines = self.wrap_text(line, self.instruction_font, max_width)
            for wrapped_line in wrapped_lines:
                text = self.instruction_font.render(wrapped_line, True, config.INSTRUCTION_TEXT_COLOR)
                self.screen.blit(text, (x, y))
                y += self.instruction_font.get_height() + config.INSTRUCTION_LINE_GAP

            y += config.INSTRUCTION_LINE_GAP

    def draw_title(self, text: str) -> None:
        title = self.title_font.render(text, True, config.MENU_TEXT_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, config.TITLE_Y))
        self.screen.blit(title, title_rect)

    def draw_button(self, rect: pygame.Rect, text: str, enabled: bool = True) -> None:
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
        label_rect = label.get_rect(center=(self.width // 2, rect.y - config.SLIDER_LABEL_OFFSET_Y))
        self.screen.blit(label, label_rect)

        pygame.draw.rect(self.screen, config.SLIDER_TRACK_COLOR, rect)

        fill_width = int(rect.width * value)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(self.screen, config.SLIDER_FILL_COLOR, fill_rect)

        knob_x = rect.x + fill_width
        knob = pygame.Rect(0, 0, config.SLIDER_KNOB_WIDTH, config.SLIDER_KNOB_HEIGHT)
        knob.center = (knob_x, rect.centery)
        pygame.draw.rect(self.screen, config.SLIDER_KNOB_COLOR, knob)

    def get_setting_text(self, template: str, enabled: bool) -> str:
        if enabled:
            state = config.SETTING_ON_TEXT
        else:
            state = config.SETTING_OFF_TEXT

        return template.format(state=state)

    def get_volume_text(self, template: str, volume: float) -> str:
        volume_percent = int(volume * config.VOLUME_PERCENT)
        return template.format(volume=volume_percent)

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list:
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

        game_x = int((mouse_pos[0] - self.game_rect.x) * self.game_width / self.game_rect.width)
        game_y = int((mouse_pos[1] - self.game_rect.y) * self.game_height / self.game_rect.height)

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
