from mycroft import MycroftSkill, intent_file_handler


class PlayFile(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('file.play.intent')
    def handle_file_play(self, message):
        self.speak_dialog('file.play')


def create_skill():
    return PlayFile()

