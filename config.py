DEFAULT_REWARD = 10
DEFAULT_FINE = 5
DEFAULT_DISMISSAL_BALANCE = -50
DEFAULT_MONEY = 0

INVALID_PERSON_CHANCE = 0.45

MIN_BIRTH_YEAR = 1980
MAX_BIRTH_YEAR = 2025
MAX_VALID_BIRTH_YEAR = 2007
MIN_DAY = 1
MAX_SAFE_DAY = 28
MIN_MONTH = 1
MAX_MONTH = 12
ISSUE_DATE_DAY = 1
ISSUE_DATE_MONTH = 9
VALID_ISSUE_AGES = (17, 18)
BAD_ISSUE_AGES = (16, 19, 20)

MIN_GROUP_NUMBER = 100000
MAX_GROUP_NUMBER = 999999
GROUP_SEPARATOR = "-"
GROUP_SPLIT_MAX_COUNT = 1
GROUP_PATTERN = r"^[А-ЯЁ]{2}-\d{6}$"
VALID_GROUP_PREFIXES = ("РИ", "ИС", "ПИ", "БИ", "ЭК", "МТ")
BAD_GROUP_PREFIX = "ЮР"
BAD_GROUP_VARIANTS = ("123456", "АА123456", "A1-000001", "ГРУППА")

GENDER_FEMALE = "female"
GENDER_MALE = "male"
GENDERS = (GENDER_FEMALE, GENDER_MALE)

FEMALE_NAMES = (
    "Анна",
    "Мария",
    "София",
    "Дарья",
    "Арина",
    "Полина",
    "Елизавета",
    "Виктория",
    "Ксения",
    "Ольга",
    "Наталья",
    "Елена",
    "Ирина",
    "Татьяна",
    "Светлана",
    "Екатерина",
    "Анастасия",
    "Марина",
    "Юлия",
    "Валерия",
    "Алиса",
    "Вероника",
    "Милана",
    "Евгения",
    "Кристина",
    "Надежда",
    "Любовь",
    "Вера",
    "Галина",
    "Валентина",
    "Людмила",
    "Зоя",
    "Нина",
    "Майя",
    "Диана",
    "Камилла",
    "Варвара",
    "Ульяна",
    "Яна",
    "Есения",
    "Аглая",
    "Пелагея",
    "Алина",
    "Алёна",
    "Алла",
    "Анжела",
    "Анжелика",
    "Василиса",
    "Асия",
    "Амина",
    "Амелия",
)

MALE_NAMES = (
    "Александр",
    "Максим",
    "Дмитрий",
    "Алексей",
    "Андрей",
    "Артем",
    "Михаил",
    "Никита",
    "Сергей",
    "Иван",
    "Борис",
    "Глеб",
    "Марк",
    "Роман",
    "Павел",
    "Лев",
    "Тимофей",
    "Даниил",
    "Владислав",
    "Егор",
    "Игорь",
    "Константин",
    "Николай",
    "Петр",
    "Ярослав",
    "Вадим",
    "Руслан",
    "Тимур",
    "Григорий",
    "Федор",
    "Ян",
    "Арсений",
    "Георгий",
    "Денис",
    "Юрий",
    "Анатолий",
    "Валерий",
    "Виктор",
    "Владимир",
    "Олег",
    "Рашид",
    "Эдуард",
    "Ростислав",
    "Станислав",
    "Всеволод",
    "Богдан",
    "Мирон",
    "Ефим",
    "Илья",
    "Герман",
)

FEMALE_LAST_NAMES = (
    "Иванова",
    "Петрова",
    "Сидорова",
    "Соколова",
    "Михайлова",
    "Фёдорова",
    "Попова",
    "Васильева",
    "Кузнецова",
    "Андронова",
    "Морозова",
    "Волкова",
    "Козлова",
    "Новикова",
    "Никонова",
    "Лебедева",
    "Семенова",
    "Егорова",
    "Павлова",
    "Козаченко",
    "Ковалева",
    "Федорова",
    "Смирнова",
    "Ульянова",
    "Козырева",
    "Макарова",
    "Романова",
    "Борисова",
    "Григорьева",
    "Антонова",
    "Орлова",
    "Захарова",
    "Титова",
    "Шаповалова",
    "Волчанская",
    "Белоусова",
    "Васильченко",
    "Горбунова",
    "Денисова",
    "Емелина",
    "Жаркова",
    "Зайцева",
    "Калашникова",
    "Карпова",
    "Киреева",
    "Киселева",
    "Котова",
    "Кузьмина",
    "Лапина",
    "Ларина",
    "Литвинова",
    "Лобанова",
    "Лосева",
    "Лукьянова",
    "Лыкова",
    "Маркова",
    "Мартынова",
    "Матвеева",
    "Медведева",
    "Меркушева",
    "Мещерякова",
    "Минаева",
    "Мироненко",
    "Митрофанова",
    "Моисеева",
    "Наумова",
    "Назарова",
    "Носкова",
    "Охлопкова",
)

MALE_LAST_NAMES = (
    "Иванов",
    "Петров",
    "Сидоров",
    "Соколов",
    "Михайлов",
    "Фёдоров",
    "Попов",
    "Васильев",
    "Кузнецов",
    "Андреев",
    "Морозов",
    "Волков",
    "Козлов",
    "Новиков",
    "Никонов",
    "Лебедев",
    "Семенов",
    "Егоров",
    "Павлов",
    "Козаченко",
    "Ковалев",
    "Федоров",
    "Смирнов",
    "Ульянов",
    "Козырев",
    "Макаров",
    "Романов",
    "Борисов",
    "Григорьев",
    "Антонов",
    "Орлов",
    "Захаров",
    "Титов",
    "Шаповалов",
    "Волчанский",
    "Белоусов",
    "Васильченко",
    "Горбунов",
    "Денисов",
    "Емелин",
    "Жарков",
    "Зайцев",
    "Калашников",
    "Карпов",
    "Киреев",
    "Киселев",
    "Котов",
    "Кузьмин",
    "Лапин",
    "Ларин",
    "Литвинов",
    "Лобанов",
    "Лосев",
    "Лукьянов",
    "Лыков",
    "Марков",
    "Мартынов",
    "Матвеев",
    "Медведев",
    "Меркушев",
    "Мещеряков",
    "Минаев",
    "Мироненко",
    "Митрофанов",
    "Моисеев",
    "Наумов",
    "Назаров",
    "Носков",
    "Охлопков",
)

FEMALE_PATRONYMICS = (
    "Александровна",
    "Алексеевна",
    "Анатольевна",
    "Андреевна",
    "Антоновна",
    "Артемовна",
    "Борисовна",
    "Валентиновна",
    "Валерьевна",
    "Васильевна",
    "Викторовна",
    "Владимировна",
    "Владиславовна",
    "Геннадиевна",
    "Георгиевна",
    "Григорьевна",
    "Даниловна",
    "Денисовна",
    "Дмитриевна",
    "Евгеньевна",
    "Егоровна",
    "Ефимовна",
    "Ивановна",
    "Игоревна",
    "Ильинична",
    "Иосифовна",
    "Кирилловна",
    "Константиновна",
    "Леонидовна",
    "Львовна",
    "Максимовна",
    "Матвеевна",
    "Михайловна",
    "Николаевна",
    "Олеговна",
    "Павловна",
    "Петровна",
    "Романовна",
    "Семеновна",
    "Сергеевна",
    "Степановна",
    "Тарасовна",
    "Тимофеевна",
    "Федоровна",
    "Юрьевна",
    "Яковлевна",
    "Ярославовна",
)

MALE_PATRONYMICS = (
    "Александрович",
    "Алексеевич",
    "Анатольевич",
    "Андреевич",
    "Антонович",
    "Артемович",
    "Борисович",
    "Валентинович",
    "Валерьевич",
    "Васильевич",
    "Викторович",
    "Владимирович",
    "Владиславович",
    "Геннадиевич",
    "Георгиевич",
    "Григорьевич",
    "Данилович",
    "Денисович",
    "Дмитриевич",
    "Евгеньевич",
    "Егорович",
    "Ефимович",
    "Иванович",
    "Игоревич",
    "Ильич",
    "Иосифович",
    "Кириллович",
    "Константинович",
    "Леонидович",
    "Львович",
    "Максимович",
    "Матвеевич",
    "Михайлович",
    "Николаевич",
    "Олегович",
    "Павлович",
    "Петрович",
    "Романович",
    "Семенович",
    "Сергеевич",
    "Степанович",
    "Тарасович",
    "Тимофеевич",
    "Федорович",
    "Юрьевич",
    "Яковлевич",
    "Ярославович",
)

EDUCATION_FORMS = ("очная", "заочная", "очно-заочная")
BAD_EDUCATION_FORMS = (
    "Домашняя",
    "Заочка-онлайн",
    "Очно-заочно",
    "Самостоятельно",
    "В свободном графике",
    "Неофициально",
    "Без формы",
    "По желанию",
    "Вечерняя-дистанционная",
    "Онлайн-заочно",
    "Дистант-очно",
    "Свободное посещение",
    "Без обучения",
    "По гибкому графику",
    "На дому",
    "Частично очно частично онлайн",
    "В интернете",
    "Как удобно",
    "В любое время",
    "По индивидуальному плану",
)
EDUCATION_LEVELS = ("бакалавриат", "специалитет", "магистратура", "аспирантура")
BAD_EDUCATION_LEVELS = (
    "Болезненное",
    "Низкое",
    "Высокое",
    "Среднее",
    "Начальное",
    "Супервысшее",
    "Высшее-бакалавр",
    "Магистр-бакалавр",
    "Аспирант-студент",
    "Докторант-магистр",
    "Неоконченное бакалавриат",
    "Среднее высшее",
    "Высшее среднее",
    "Профессиональное высшее",
    "Высшее профессиональное переподготовка",
    "Ускоренное высшее",
    "Гибридное высшее",
    "Смешанное высшее",
    "Онлайн-высшее",
    "Дистант-бакалавриат",
    "Заочно-очно",
    "Вечерне-заочное",
    "Семейное высшее",
    "Надомное бакалавриат",
    "Экстернат-магистратура",
    "Самообразование высшее",
)
INSTITUTES = (
    "ИнЭУ",
    "ИНМиТ",
    "ИЕНиМ",
    "ИРИТ-РТФ",
    "ИФКСиМП",
    "ИФО",
    "ИСА",
    "УГИ",
    "УЭИ",
    "ФТИ",
    "ХТИ",
)
BAD_INSTITUTES = (
    "Институт случайных решений",
    "Факультет домашних наук",
    "Академия свободного посещения",
    "Институт интернет-обучения",
    "Центр неофициального образования",
    "Институт без кафедр",
    "Академия вечернего дистант-очно",
    "Факультет гибкого графика",
    "Институт самостоятельных студентов",
    "Высшая школа как удобно",
    "Институт временного обучения",
    "Факультет неизвестных направлений",
    "Институт личного плана",
    "Факультет без расписания",
)

TEACHER_POSITIONS = ("Профессор", "Доцент", "Старший преподаватель", "Ассистент")
BAD_TEACHER_POSITIONS = ("Директор", "Начальник", "Учитель", "Менеджер", "Охранник", "Дворник")

TEACHER_DEGREES = ("Доктор наук", "Кандидат наук", "Без степени")
BAD_TEACHER_DEGREES = ("Магистр магии", "Академик", "Доктор всея Руси", "Студент", "Бакалавр наук")

TEACHER_DEPARTMENTS = ("Кафедра ПИ", "Кафедра ИС", "Кафедра БИ", "Кафедра ЭК", "Кафедра РИ", "Кафедра МТ")
BAD_TEACHER_DEPARTMENTS = ("Кафедра магии", "Кафедра отдыха", "Отдел продаж", "Бухгалтерия")

DECISION_ALLOW = "allow"
DECISION_DENY = "deny"
ALLOW_DECISIONS = ("allow", "accept", "pass", "пропустить", "допустить")
DENY_DECISIONS = ("deny", "reject", "kick", "вышвырнуть", "отказать", "не пропустить")

NO_DOCUMENT = "no_document"
BAD_BIRTH_DATE = "bad_birth_date"
BAD_ISSUE_DATE = "bad_issue_date"
BAD_GROUP_FORMAT = "bad_group_format"
BAD_EDUCATION_FORM = "bad_education_form"
BAD_EDUCATION_LEVEL = "bad_education_level"
BAD_INSTITUTE = "bad_institute"
BAD_NOT_UNIQUE_PASS = "bad_not_unique_pass"
BAD_IMPOSTER = "bad_imposter"

CHECK_DOCUMENT = "document"
CHECK_BIRTH_DATE = "birth_date"
CHECK_ISSUE_DATE = "issue_date"
CHECK_GROUP = "group"
CHECK_EDUCATION_FORM = "education_form"
CHECK_EDUCATION_LEVEL = "education_level"
CHECK_INSTITUTE = "institute"
CHECK_VIP = "vip"
ALL_CHECKS = (
    CHECK_DOCUMENT,
    CHECK_BIRTH_DATE,
    CHECK_ISSUE_DATE,
    CHECK_GROUP,
    CHECK_EDUCATION_FORM,
    CHECK_EDUCATION_LEVEL,
    CHECK_INSTITUTE,
    CHECK_VIP,
)
CHECKS_BY_DAY = {
    1: (CHECK_DOCUMENT, CHECK_BIRTH_DATE),
    2: (CHECK_DOCUMENT, CHECK_BIRTH_DATE, CHECK_ISSUE_DATE, CHECK_VIP),
    3: (CHECK_DOCUMENT, CHECK_BIRTH_DATE, CHECK_ISSUE_DATE, CHECK_GROUP, CHECK_VIP),
    4: (
        CHECK_DOCUMENT,
        CHECK_BIRTH_DATE,
        CHECK_ISSUE_DATE,
        CHECK_GROUP,
        CHECK_EDUCATION_FORM,
        CHECK_EDUCATION_LEVEL,
        CHECK_VIP,
    ),
    5: ALL_CHECKS,
}
CHECK_ERROR_REASONS = {
    CHECK_DOCUMENT: (NO_DOCUMENT,),
    CHECK_BIRTH_DATE: (BAD_BIRTH_DATE,),
    CHECK_ISSUE_DATE: (BAD_ISSUE_DATE,),
    CHECK_GROUP: (BAD_GROUP_FORMAT,),
    CHECK_EDUCATION_FORM: (BAD_EDUCATION_FORM,),
    CHECK_EDUCATION_LEVEL: (BAD_EDUCATION_LEVEL,),
    CHECK_INSTITUTE: (BAD_INSTITUTE,),
    CHECK_VIP: (BAD_NOT_UNIQUE_PASS, BAD_IMPOSTER),
}
INVALID_REASONS = (
    NO_DOCUMENT,
    BAD_BIRTH_DATE,
    BAD_ISSUE_DATE,
    BAD_GROUP_FORMAT,
    BAD_EDUCATION_FORM,
    BAD_EDUCATION_LEVEL,
    BAD_INSTITUTE,
    BAD_NOT_UNIQUE_PASS,
    BAD_IMPOSTER,
)

DATE_FORMAT = "%d.%m.%Y"
NO_DATE_TEXT = "нет данных"

STUDENT_CARD_TEXT = "Студенческий билет"
DOCUMENT_TYPE_STUDENT = "Студенческий билет"
DOCUMENT_TYPE_VIP = "Удостоверение преподавателя"
PERSON_FULL_NAME_TEXT = "ФИО"
PERSON_GROUP_TEXT = "Группа"
PERSON_BIRTH_DATE_TEXT = "Дата рождения"
EDUCATION_FORM_TEXT = "Форма обучения"
EDUCATION_LEVEL_TEXT = "Уровень обучения"
PERSON_POSITION_TEXT = "Должность"
PERSON_DEPARTMENT_TEXT = "Кафедра"
PERSON_DEGREE_TEXT = "Ученая степень"
INSTITUTE_TEXT = "Институт"
ISSUE_DATE_TEXT = "Дата выдачи"
NO_DOCUMENT_TEXT = "Студенческого билета нет"



ERROR_NO_DOCUMENT = "Нет студенческого билета"
ERROR_BAD_BIRTH_DATE = "Неверная дата рождения"
ERROR_BAD_ISSUE_DATE = "Неверная дата выдачи"
ERROR_BAD_GROUP_FORMAT = "Неверный формат группы"
ERROR_BAD_EDUCATION_FORM = "Неверная форма обучения"
ERROR_BAD_EDUCATION_LEVEL = "Неверный уровень обучения"
ERROR_BAD_INSTITUTE = "Неизвестный институт"
ERROR_NOT_UNIQUE_PASS = "Требуется удостоверение преподавателя"
ERROR_IMPOSTER = "Чужое удостоверение"

MESSAGE_NO_CURRENT_PERSON = "Нельзя принять решение: нет текущего посетителя"
MESSAGE_GAME_ALREADY_OVER = "Игра окончена"
MESSAGE_DISMISSED = "Долг слишком большой: игрока уволили"
MESSAGE_UNKNOWN_DECISION = "Неизвестное решение игрока: {decision}"

PERSON_RECT_X = 850
PERSON_RECT_Y = 220
PERSON_RECT_WIDTH = 260
PERSON_RECT_HEIGHT = 687
PERSON_COLOR = (0, 0, 0)
VIP_PERSON_COLOR = (218, 165, 32)

GAME_TITLE = "RADIK, PLEASE!"
ICON_PATH = "assets/images/icon.png"
BACKGROUND_PATH = "assets/images/bg.png"
TABLE_PATH = "assets/images/table.png"
MUSIC_PATH = "assets/sounds/bg.mp3"
DEFAULT_MUSIC_VOLUME = 0.4
DEFAULT_SOUND_VOLUME = 0.7
DEFAULT_MUSIC_ENABLED = True
DEFAULT_SOUND_ENABLED = True
MIN_VOLUME = 0.0
MAX_VOLUME = 1.0
VOLUME_ROUND_DIGITS = 2
VOLUME_PERCENT = 100
FONT_NAME = "segoeui"

DEFAULT_WINDOW_WIDTH = 1536
DEFAULT_WINDOW_HEIGHT = 1024
WINDOW_MODE_TYPE_INDEX = 0
WINDOW_MODE_TEXT_INDEX = 1
WINDOW_MODE_WIDTH_INDEX = 2
WINDOW_MODE_HEIGHT_INDEX = 3
WINDOW_MODE_WINDOWED = "windowed"
WINDOW_MODE_FULLSCREEN = "fullscreen"
WINDOW_MODE_BORDERED_FULLSCREEN = "bordered_fullscreen"
WINDOW_MODES = (
    (WINDOW_MODE_BORDERED_FULLSCREEN, "Полный экран с рамками", 0, 0),
)
DEFAULT_WINDOW_MODE_NUMBER = 0

SCREEN_MENU = "menu"
SCREEN_SETTINGS = "settings"
SCREEN_GAME = "game"

BUTTON_START = "start"
BUTTON_CONTINUE = "continue"
BUTTON_SETTINGS = "settings"
BUTTON_EXIT = "exit"
BUTTON_MUSIC = "music"
BUTTON_SOUND = "sound"
BUTTON_WINDOW_SIZE = "window_size"
BUTTON_BACK = "back"
SLIDER_MUSIC_VOLUME = "music_volume"
SLIDER_SOUND_VOLUME = "sound_volume"

SAVE_FILE = "save.json"
SETTINGS_FILE = "settings.json"
SETTINGS_ENCODING = "utf-8"
SAVE_MONEY = "money"
SAVE_ROUND_NUMBER = "round_number"
SAVE_DAY_NUMBER = "day_number"

SAVE_DAY_PLAN = "day_plan"
SAVE_DAY_PLAN_INDEX = "day_plan_index"
SAVE_CURRENT_PERSON = "current_person"
SAVE_GAME_OVER = "game_over"
SAVE_GAME_OVER_REASON = "game_over_reason"
SAVE_FULL_NAME = "full_name"
SAVE_GROUP = "group"
SAVE_BIRTH_DATE = "birth_date"
SAVE_DOCUMENT = "document"
SAVE_IS_IMPORTANT = "is_important"
SAVE_EDUCATION_FORM = "education_form"
SAVE_EDUCATION_LEVEL = "education_level"
SAVE_INSTITUTE = "institute"
SAVE_ISSUE_DATE = "issue_date"
SAVE_DOCUMENT_TYPE = "document_type"
SETTING_MUSIC_ENABLED = "music_enabled"
SETTING_SOUND_ENABLED = "sound_enabled"
SETTING_MUSIC_VOLUME = "music_volume"
SETTING_SOUND_VOLUME = "sound_volume"
SETTING_WINDOW_MODE_NUMBER = "window_mode_number"

MENU_TITLE_TEXT = "RADIK, PLEASE!"
MENU_START_TEXT = "Начать игру"
MENU_CONTINUE_TEXT = "Продолжить"
MENU_SETTINGS_TEXT = "Настройки"
MENU_EXIT_TEXT = "Выход"
MENU_BACK_TEXT = "Назад"

SETTINGS_TITLE_TEXT = "Настройки"
SETTING_ON_TEXT = "вкл"
SETTING_OFF_TEXT = "выкл"
MUSIC_SETTING_TEXT = "Музыка: {state}"
SOUND_SETTING_TEXT = "Звук: {state}"
MUSIC_VOLUME_TEXT = "Громкость музыки: {volume}%"
SOUND_VOLUME_TEXT = "Громкость звука: {volume}%"
WINDOW_SIZE_TEXT = "Окно: {mode}"
BALANCE_TEXT = "{balance} ₽"
DAY_TEXT = "День {day}"
DATE_TEXT = "{date}"
TIME_TEXT = "{time}"
RESULT_CORRECT_TEXT = "Верно: {money_delta} ₽"
RESULT_MISTAKE_TEXT = "Ошибка: {money_delta} ₽"
INSTRUCTION_TITLE_TEXT = "Инструкция"

MENU_BUTTON_WIDTH = 520
MENU_BUTTON_HEIGHT = 60
MENU_FIRST_BUTTON_Y = 240
MENU_BUTTON_GAP = 80
SETTINGS_FIRST_BUTTON_Y = 180
SETTINGS_BUTTON_GAP = 70
SLIDER_TRACK_WIDTH = 360
SLIDER_TRACK_HEIGHT = 8
SLIDER_TRACK_OFFSET_Y = 42
SLIDER_LABEL_OFFSET_Y = 24
SLIDER_KNOB_WIDTH = 18
SLIDER_KNOB_HEIGHT = 28

TITLE_Y = 120
TITLE_FONT_SIZE = 64
BUTTON_FONT_SIZE = 38
GAME_FONT_SIZE = 40
INSTRUCTION_FONT_SIZE = 24
STUDENT_CARD_FONT_SIZE = 28

BACKGROUND_X = 0
BACKGROUND_Y = 0
TABLE_X = -25
TABLE_Y = 400
TABLE_WIDTH = 1600
TABLE_HEIGHT = 915
INSTRUCTION_BOOK_X = 985
INSTRUCTION_BOOK_Y = 700
INSTRUCTION_BOOK_WIDTH = 320
INSTRUCTION_BOOK_HEIGHT = 230
STUDENT_CARD_X = 630
STUDENT_CARD_Y = 750
STUDENT_CARD_WIDTH = 270
STUDENT_CARD_HEIGHT = 160
STUDENT_CARD_PATH = "assets/images/student_card.png"
STUDENT_CARD_PANEL_WIDTH = 760
STUDENT_CARD_PANEL_HEIGHT = 520
STUDENT_CARD_PANEL_Y = 110
STUDENT_CARD_PANEL_PADDING = 34
STUDENT_CARD_LINE_GAP = 10
INSTRUCTION_BG_PATH = "assets/images/instruction_bg.png"
ALLOW_BUTTON_PATH = "assets/images/btn_allow.png"
ALLOW_BUTTON_PRESSED_PATH = "assets/images/btn_allow_pressed.png"
DENY_BUTTON_PATH = "assets/images/btn_deny.png"
DENY_BUTTON_PRESSED_PATH = "assets/images/btn_deny_pressed.png"
ALLOW_BUTTON_X = 320
ALLOW_BUTTON_Y = 820
ALLOW_BUTTON_SIZE = 120
DENY_BUTTON_X = 460
DENY_BUTTON_Y = 820
DENY_BUTTON_SIZE = 120
BALANCE_X = 30
BALANCE_Y = 30
DAY_INFO_X = 30
DAY_INFO_Y = 82
DAY_INFO_GAP_Y = 40
RESULT_X = 30
RESULT_Y = 215

DAY_VISITORS_COUNT = 15
DAY_MIN_BAD_VISITORS = 1
DAY_MAX_BAD_VISITORS = 3
DAY_PLAN_POPULATION_SIZE = 50
DAY_PLAN_GENERATIONS = 100
DAY_PLAN_MUTATION_CHANCE = 0.1


INSTITUTE_GROUP_PREFIXES = {
    "ИнЭУ": ("ЭК", "МТ"),
    "ИНМиТ": ("МТ",),
    "ИЕНиМ": ("БИ",),
    "ИРИТ-РТФ": ("РИ", "ПИ", "ИС"),
    "ИФКСиМП": ("БИ",),
    "ИФО": ("РИ",),
    "ИСА": ("ИС",),
    "УГИ": ("ЭК",),
    "УЭИ": ("ЭК",),
    "ФТИ": ("ПИ",),
    "ХТИ": ("БИ",),
}
NEXT_VISITOR_DELAY = 900
INSTRUCTION_PANEL_WIDTH = 1000
INSTRUCTION_PANEL_HEIGHT = 600
INSTRUCTION_PANEL_PADDING = 32
INSTRUCTION_TITLE_GAP = 46
INSTRUCTION_LINE_GAP = 8

MENU_BACKGROUND_COLOR = (0, 0, 0)
MENU_TEXT_COLOR = (235, 235, 235)
BUTTON_COLOR = (45, 45, 45)
BUTTON_HOVER_COLOR = (70, 70, 70)
BUTTON_DISABLED_COLOR = (35, 35, 35)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_DISABLED_TEXT_COLOR = (120, 120, 120)
SLIDER_TRACK_COLOR = (70, 70, 70)
SLIDER_FILL_COLOR = (180, 180, 180)
SLIDER_KNOB_COLOR = (255, 255, 255)
BALANCE_TEXT_COLOR = (60, 220, 90)
RESULT_CORRECT_COLOR = (60, 220, 90)
RESULT_MISTAKE_COLOR = (230, 70, 70)
INSTRUCTION_PANEL_COLOR = (28, 28, 28)
INSTRUCTION_BORDER_COLOR = (120, 120, 120)
INSTRUCTION_TEXT_COLOR = (255, 255, 255)
STUDENT_CARD_COLOR = (0, 0, 0)
STUDENT_CARD_PANEL_COLOR = (245, 245, 240)
STUDENT_CARD_PANEL_BORDER_COLOR = (20, 20, 20)
STUDENT_CARD_PANEL_TEXT_COLOR = (20, 20, 20)


MIN_ISSUE_YEAR = 2024
MAX_ISSUE_YEAR = 2024

INSTRUCTION_DAY = "День {day}. Сегодняшние правила:"

INSTRUCTIONS_BY_DAY = {
    1: [
        "ПРАВИЛА ПРОПУСКА:",
        "- Обязателен студенческий билет (для преподавателей - удостоверение).",
        "- Год рождения посетителя не позднее {max_year}.",
        "",
        "ИНСТРУКЦИЯ:",
        "Нажмите зеленую кнопку чтобы пропустить",
        "и красную в ином случае."
    ],
    2: [
        "ПРАВИЛА ПРОПУСКА:",
        "- Обязателен студенческий билет (для преподавателей - удостоверение преподавателя).",
        "- Год рождения не позднее {max_year}.",
        "- Дата выдачи строго 01.09.2024.",
        "",
        "ВНИМАНИЕ:",
        "Пропускайте преподавателей только с удостоверением!"
    ],
    3: [
        "ПРАВИЛА ПРОПУСКА:",
        "- Студенческий билет (для преподавателей - удостоверение преподавателя).",
        "- Год рождения не позднее {max_year}.",
        "- Дата выдачи строго 01.09.2024.",
        "- Группа студента: формат АА-123456.",
        "- Должность преподавателя: {teacher_positions}."
    ],
    4: [
        "ПРАВИЛА ПРОПУСКА (ДЕНЬ 4):",
        "- Все правила предыдущего дня сохраняются.",
        "- Форма обучения студента: {forms}.",
        "- Кафедра преподавателя: {teacher_departments}.",
        "- Уровень обучения студента: {levels}.",
        "- Ученая степень преподавателя: {teacher_degrees}."
    ],
    5: [
        "ПРАВИЛА ПРОПУСКА (ВСЕ ПРОВЕРКИ АКТИВНЫ):",
        "- Правила 4-го дня.",
        "- Институт должен быть только в списке разрешенных.",
        "",
        "РАЗРЕШЕННЫЕ ИНСТИТУТЫ:",
        "{institutes}"
    ]
}
