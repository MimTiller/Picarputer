from kivy.app import App
from functools import partial
from kivy.uix.button import Button
from kivy.resources import resource_find
from kivy.garden.notification import Notification


class Notifier(Button):
    def __init__(self, **kwargs):
        super(Notifier, self).__init__(**kwargs)
        self.bind(on_release=self.show_notification)

    def printer(self, *args):
        print(args)

    def show_notification(self, *args):
        # open default notification
        Notification().open(
            title='Kivy Notification',
            message='Hello from the other side?',
            timeout=5,
            icon=resource_find('data/logo/kivy-icon-128.png'),
            on_stop=partial(self.printer, 'Notification closed')
        )

        # open notification with layout in kv
        Notification().open(
            title='Kivy Notification',
            message="I'm a Button!",
            kv="Button:\n    text: app.message"
        )


class KivyNotification(App):
    def build(self):
        return Notifier()


if __name__ == '__main__':
    KivyNotification().run()
