import os
import whisper
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
# import japanize_kivy

# print(japanize_kivy.__file__)

def transscribe(audio_file):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file)
    return result["text"]

class TranscriptionBox(BoxLayout):
    result_text = StringProperty("")
    file_path_text = StringProperty("ファイルをここにドラッグ＆ドロップしてください。")
    file_path = None

    def __init__(self, **kwargs):
        super(TranscriptionBox, self).__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)

    def _on_file_drop(self, window, file_path):
        self.file_path = file_path.decode('utf-8')
        self.file_path_text = self.file_path

    def transcribe_file(self):
        if self.file_path is None:
            self.result_text = "ファイルが選択されていません。"
        elif self.file_path.endswith(".mp3"):
            try:
                self.result_text = transscribe(self.file_path)
            except Exception:
                self.result_text = "文字起こしに失敗しました。ファイルを確認してください。"
        else:
            self.result_text = "選択されたファイルはMP3ファイルではありません。"

    def copy_to_clipboard(self):
        Clipboard.copy(self.result_text)


Builder.load_string("""
<TranscriptionBox>:
    orientation: "vertical"
    Label:
        text: root.file_path_text
    Button:
        text: "文字起こしをする"
        on_press: root.transcribe_file()
    ScrollView:
        size_hint_y: 0.8
        Label:
            text: root.result_text
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
    Button:
        text: "結果をクリップボードに保存"
        on_press: root.copy_to_clipboard()
""")


class LocalWhisperApp(App):
    def build(self):
        return TranscriptionBox()


if __name__ == "__main__":
    LocalWhisperApp().run()