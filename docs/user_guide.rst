User Guide
===========

Using signals
-------------

On each allowed event github_webhooks executes a signal.

You can receive a signal by adding listeners like that:

.. code-block:: python

    # receivers.py
    def issue_event(payload: dict, **kwargs) -> None:
        # Save / update etc. data
        pass


    # apps.py
    from github_webhooks import signals


    class MyApp(AppConfig):
        name = "myapp"

        def ready():
            from . import receivers
            signals.issues_signal.connect(receivers.issue_event)
