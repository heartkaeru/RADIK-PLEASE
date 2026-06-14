class ObjectPool:
    """
    Класс реализует паттерн проектирования "Пул объектов" (Object Pool).
    Идея в том, что создавать и удалять объекты в памяти (особенно много и часто) - это медленно.
    Поэтому мы создаем их один раз, а когда они становятся не нужны, не удаляем, а кладем обратно в "коробку" (пул).
    Когда нам снова нужен такой же объект, мы достаем его из коробки уже готовым.
    """
    def __init__(self, factory_func):
        """
        factory_func - это функция (или класс), которая умеет создавать новые объекты, если пул пуст.
        """
        self.factory_func = factory_func
        self.pool = []

    def get(self):
        """
        Если в пуле есть свободные объекты, берем последний добавленный (это быстрее всего) и удаляем из списка свободных.
        """
        if self.pool:
            return self.pool.pop()
        return self.factory_func()

    def release(self, obj):
        """
        Возвращаем отработанный объект обратно в список свободных, чтобы переиспользовать его позже.
        """
        self.pool.append(obj)


class FloatingTextEffect:
    """
    Эффект всплывающего текста (например, "+100 денег" или "-5 репутации", которые улетают вверх).
    Чтобы не создавать этот объект заново при каждом чихе, мы используем для него ObjectPool.
    """
    def __init__(self):
        """
        Объект создается "пустым" и неактивным. Значения по умолчанию.
        """
        self.active = False
        self.x = 0.0
        self.y = 0.0
        self.surface = None
        self.alpha = (
            255
        )
        self.speed = 0.0
        self.life_time = 0.0
        self.max_life_time = 0.0
        self.is_static = False

    def reset(
        self,
        text,
        color,
        font,
        x,
        y,
        speed=50.0,
        max_life_time=2.0,
        is_static=False,
    ):
        """
        Эта функция "оживляет" объект, когда мы достаем его из пула.
        Она задает ему новый текст, координаты, скорость и время жизни.
        """
        self.surface = font.render(
            text, True, color
        ).convert_alpha()
        self.x = float(x)
        self.y = float(y)
        self.alpha = 255
        self.speed = float(speed)
        self.life_time = 0.0
        self.max_life_time = float(max_life_time)
        self.is_static = is_static
        self.active = True

    def update(self, dt):
        """
        dt (delta time) - время, прошедшее с прошлого кадра (чтобы анимация не зависела от FPS).
        Если эффект неактивен или он должен просто висеть на месте (is_static), ничего не обновляем.
        """
        if not self.active or self.is_static:
            return

        self.life_time += dt
        self.y -= self.speed * dt

        fade_start = self.max_life_time * 0.5
        if self.life_time > fade_start:
            progress = (self.life_time - fade_start) / (
                self.max_life_time - fade_start
            )
            self.alpha = max(0, int(255 * (1.0 - progress)))
            if self.surface:
                self.surface.set_alpha(
                    self.alpha
                )

        if self.life_time >= self.max_life_time:
            self.active = False

    def draw(self, screen):
        """
        Отрисовываем картинку текста на экране по его координатам (только если эффект активен).
        """
        if self.active and self.surface:
            screen.blit(self.surface, (int(self.x), int(self.y)))
