import random
from enum import Enum
import pygame
import config


class NodeStatus(Enum):
    SUCCESS = 1
    FAILURE = 2
    RUNNING = 3


class BTNode:
    def tick(self, context, dt) -> NodeStatus:
        raise NotImplementedError


class Sequence(BTNode):
    def __init__(self, children):
        self.children = children
        self.current_index = 0

    def tick(self, context, dt) -> NodeStatus:
        """
        Если мы уже выполнили все узлы, возвращаем успех
        """
        if self.current_index >= len(self.children):
            return NodeStatus.SUCCESS

        status = self.children[self.current_index].tick(context, dt)

        if status == NodeStatus.SUCCESS:
            self.current_index += 1
            if self.current_index >= len(self.children):
                self.current_index = 0
                return NodeStatus.SUCCESS
            return NodeStatus.RUNNING
        elif status == NodeStatus.FAILURE:
            self.current_index = 0
            return NodeStatus.FAILURE

        return NodeStatus.RUNNING

    def reset(self):
        """
        Сброс индекса, чтобы начать последовательность сначала
        """
        self.current_index = 0


class Selector(BTNode):
    def __init__(self, children):
        self.children = children
        self.current_index = 0

    def tick(self, context, dt) -> NodeStatus:
        if self.current_index >= len(self.children):
            return NodeStatus.FAILURE

        status = self.children[self.current_index].tick(context, dt)

        if status == NodeStatus.SUCCESS:
            self.current_index = 0
            return NodeStatus.SUCCESS
        elif status == NodeStatus.FAILURE:
            self.current_index += 1
            if self.current_index >= len(self.children):
                self.current_index = 0
                return NodeStatus.FAILURE
            return NodeStatus.RUNNING

        return NodeStatus.RUNNING

    def reset(self):
        self.current_index = 0


class WalkInAction(BTNode):
    def tick(self, context, dt) -> NodeStatus:
        """
        Устанавливаем состояние контроллера, чтобы он знал, что мы идем
        """
        context.visitor_state = "WALKING_IN"
        context.visitor_x -= 1000 * dt
        if context.visitor_x <= config.PERSON_RECT_X:
            context.visitor_x = config.PERSON_RECT_X
            context.visitor_state = "AT_DESK"
            return NodeStatus.SUCCESS

        return NodeStatus.RUNNING


class WaitDecisionAction(BTNode):
    def tick(self, context, dt) -> NodeStatus:
        """
        Если в контексте (контроллере) появилось решение (игрок нажал кнопку печати),
        то ожидание успешно закончено.
        """
        if context.decision_made is not None:
            return NodeStatus.SUCCESS
        return NodeStatus.RUNNING


class ProcessReactionAction(BTNode):
    def __init__(self):
        self.started = False
        self.timer = 0
        self.is_bribe = False

    def tick(self, context, dt) -> NodeStatus:
        person = context.get_current_person()

        bribe_pending = getattr(context, "bribe_pending", False)

        if not self.started:
            self.started = True

            if bribe_pending:
                if context.decision_made.name == "ALLOW":
                    context.game_model.economy.add_money(50)
                context.bribe_pending = False
                self.started = False
                return NodeStatus.SUCCESS

            if (
                not person
                or not person.is_important
                or context.decision_made.name == "ALLOW"
            ):
                self.started = False
                return NodeStatus.SUCCESS

            check_result = context.game_model.checker.get_result(
                person, context.game_model.get_active_checks()
            )

            if not check_result.allow and random.random() < 0.50:
                self.is_bribe = True
                self.timer = 2.0
                context.speech_bubble_text = (
                    "Я дам тебе небольшую сумму, пропусти"
                )
                context.bribe_pending = (
                    True
                )
            else:
                self.started = False
                return NodeStatus.SUCCESS

        if self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                context.speech_bubble_text = None
                if self.is_bribe:
                    context.decision_made = None
            return NodeStatus.RUNNING

        self.started = False

        if self.is_bribe:
            return NodeStatus.FAILURE

        return NodeStatus.SUCCESS


class FinalizeDecisionAction(BTNode):
    def tick(self, context, dt) -> NodeStatus:
        decision = context.decision_made
        context.leaving_person = context.get_current_person()

        result = context.game_model.decide(decision)

        text = context.get_result_text(result)
        color = (
            config.RESULT_CORRECT_COLOR
            if result.is_correct
            else config.RESULT_MISTAKE_COLOR
        )
        effect = context.effect_pool.get()
        effect.reset(
            text, color, context.view.myfont, config.RESULT_X, config.RESULT_Y
        )
        context.active_effects.append(effect)

        context.student_card_open = False

        if result.game_over:
            go_effect = context.effect_pool.get()
            go_effect.reset(
                result.game_over_reason,
                config.RESULT_MISTAKE_COLOR,
                context.view.myfont,
                config.RESULT_X,
                config.RESULT_Y + 40,
                is_static=True,
            )
            context.active_effects.append(go_effect)
            context.next_visitor_time = None
            context.delete_save()
        else:
            context.next_visitor_time = None
            context.save_game()

        return NodeStatus.SUCCESS


class WalkOutAction(BTNode):
    def tick(self, context, dt) -> NodeStatus:
        context.visitor_state = "WALKING_OUT"
        context.visitor_x -= 1000 * dt
        if context.visitor_x <= -config.PERSON_RECT_WIDTH:
            context.visitor_state = "NONE"
            context.visitor_visible = False

            if context.game_model and not context.game_model.game_over:
                if context.game_model.day_finished:
                    context.fade_state = (
                        "FADE_OUT"
                    )
                    context.next_visitor_time = None
                else:
                    context.next_visitor_time = pygame.time.get_ticks() + 200

            return NodeStatus.SUCCESS

        return NodeStatus.RUNNING


class RepeatUntilSuccess(BTNode):
    def __init__(self, child):
        self.child = child

    def tick(self, context, dt) -> NodeStatus:
        status = self.child.tick(context, dt)
        if status == NodeStatus.SUCCESS:
            return NodeStatus.SUCCESS
        if status == NodeStatus.FAILURE:
            if hasattr(self.child, "reset"):
                self.child.reset()
            return NodeStatus.RUNNING
        return NodeStatus.RUNNING


def build_visitor_tree():
    """
    Цикл взаимодействия: ждем решения, обрабатываем реакцию (взятку)
    """
    interaction_sequence = Sequence(
        [WaitDecisionAction(), ProcessReactionAction()]
    )

    loop = RepeatUntilSuccess(interaction_sequence)

    root = Sequence(
        [WalkInAction(), loop, FinalizeDecisionAction(), WalkOutAction()]
    )

    return root
