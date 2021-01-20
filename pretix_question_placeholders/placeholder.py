from pretix.base.mail import BaseMailPlaceholder


class QuestionMailPlaceholder(BaseMailPlaceholder):
    def __init__(self, placeholder):
        self._identifier = f"question_{placeholder.question.id}"
        self.placeholder = placeholder

    @property
    def required_context(self):
        return ["order"]

    @property
    def identifier(self):
        return self._identifier

    def render(self, context):
        return self.placeholder.render(context["order"])
