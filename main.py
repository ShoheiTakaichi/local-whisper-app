import os
import whisper
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.clipboard import Clipboard

import japanize_kivy


def transscribe(audio_file):
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)
    return result["text"]


class TranscriptionBox(BoxLayout):
    result_text = StringProperty("")

    def __init__(self, **kwargs):
        super(TranscriptionBox, self).__init__(**kwargs)

    def transcribe_file(self, file_path):
        if file_path.endswith(".mp3"):
            self.result_text = transscribe(file_path)
        else:
            self.result_text = "選択されたファイルはMP3ファイルではありません。"

    def copy_to_clipboard(self):
        Clipboard.copy(self.result_text)


Builder.load_string("""
<TranscriptionBox>:
    orientation: "vertical"
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        FileChooserIconView:
            id: filechooser
            on_selection: root.transcribe_file(self.selection and self.selection[0] or '')
    Button:
        text: "文字起こしをする"
        on_press: root.transcribe_file(filechooser.selection and filechooser.selection[0] or '')
    Label:
        text: root.result_text
    Button:
        text: "結果をクリップボードに保存"
        on_press: root.copy_to_clipboard()
""")


class LocalWhisperApp(App):
    def build(self):
        return TranscriptionBox()


if __name__ == "__main__":
    LocalWhisperApp().run()