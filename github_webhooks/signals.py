from django.dispatch import Signal

issues_signal = Signal(providing_args=["payload"])
