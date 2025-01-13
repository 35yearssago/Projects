from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import asyncio
import threading


class ChatClientApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.host = "127.0.0.1"
        self.port = 12345
        self.loop = asyncio.new_event_loop()
        self.writer = None
        self.reader = None
        self.running = True

    def build(self):

        self.root_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        self.chat_scroll = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)
        self.chat_layout = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter("height"))
        self.chat_scroll.add_widget(self.chat_layout)

        self.message_input = TextInput(
            size_hint=(0.8, None),
            height=40,
            multiline=False,
            hint_text="Type your message here...",
        )
        self.message_input.bind(on_text_validate=self.send_message)  # Enter key sends message

        self.send_button = Button(text="Send", size_hint=(0.2, None), height=40)
        self.send_button.bind(on_press=self.send_message)

        self.bottom_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        self.bottom_layout.add_widget(self.message_input)
        self.bottom_layout.add_widget(self.send_button)

        self.root_layout.add_widget(self.chat_scroll)
        self.root_layout.add_widget(self.bottom_layout)

        threading.Thread(target=self.run_event_loop, daemon=True).start()

        return self.root_layout

    def run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_client())

    async def start_client(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.display_message("Connected to the server.")
            await self.receive_messages()
        except Exception as e:
            self.display_message(f"Error connecting to server: {e}")

    async def receive_messages(self):
        try:
            while self.running:
                data = await self.reader.read(1024)
                if not data:
                    self.display_message("Disconnected from server.")
                    break
                message = data.decode("utf-8")
                self.display_message(message)
        except Exception as e:
            self.display_message(f"Error receiving messages: {e}")
        finally:
            self.writer = None

    def send_message(self, *args):
        message = self.message_input.text.strip()
        if not message:
            return

        if not self.writer:
            self.display_message("Error: Not connected to the server.")
            return

        asyncio.run_coroutine_threadsafe(self._send_message(message), self.loop)
        self.message_input.text = ""

    async def _send_message(self, message):
        try:
            self.writer.write(message.encode("utf-8"))
            await self.writer.drain()
            self.display_message(f"You: {message}")
        except Exception as e:
            self.display_message(f"Error sending message: {e}")

    def display_message(self, message):

        Clock.schedule_once(lambda dt: self._add_message_to_ui(message))

    def _add_message_to_ui(self, message):

        label = Label(
            text=message,
            size_hint_y=None,
            halign="left",
            valign="middle",
            padding=(10, 10),
            color=(1, 1, 1, 1),
        )
        label.text_size = (self.chat_scroll.width - 20, None)
        label.height = label.texture_size[1] + 20
        self.chat_layout.add_widget(label)
        self.chat_scroll.scroll_y = 0

    def on_stop(self):
        self.running = False
        if self.writer:
            try:
                asyncio.run_coroutine_threadsafe(self.writer.close(), self.loop)
            except Exception:
                pass
        self.loop.stop()


if __name__ == "__main__":
    ChatClientApp().run()