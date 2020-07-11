from djoser import email


class ActivationTemplate(email.ActivationEmail):

    template_name = "activation.html"
