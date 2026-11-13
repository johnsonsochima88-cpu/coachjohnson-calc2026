from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import ast
import operator

Window.clearcolor = get_color_from_hex("#101820")


class CalculatorApp(App):

    def build(self):
        self.title = "Coach Johnson Calculator"

        main = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.display = TextInput(
            text="0",
            font_size=40,
            readonly=True,
            halign="right",
            size_hint=(1, 0.25),
            background_color=get_color_from_hex("#202A35"),
            foreground_color=get_color_from_hex("#FFFFFF")
        )

        main.add_widget(self.display)

        grid = GridLayout(
            cols=4,
            spacing=8,
            size_hint=(1, 0.75)
        )

        buttons = [
            "C", "DEL", "%", "/",
            "7", "8", "9", "*",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "00", "0", ".", "="
        ]

        for text in buttons:
            btn = Button(
                text=text,
                font_size=26,
                bold=True,
                background_normal="",
                background_color=get_color_from_hex("#34495E"),
                color=get_color_from_hex("#FFFFFF")
            )

            if text == "=":
                btn.background_color = get_color_from_hex("#00C853")

            elif text == "C":
                btn.background_color = get_color_from_hex("#E53935")

            elif text in ["+", "-", "*", "/", "%"]:
                btn.background_color = get_color_from_hex("#FF9800")

            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)

        main.add_widget(grid)

        return main

    def on_button_press(self, instance):
        value = instance.text
        current = self.display.text

        if value == "C":
            self.display.text = "0"

        elif value == "DEL":
            self.display.text = current[:-1] or "0"

        elif value == "=":
            try:
                result = self.safe_calculate(current)
                self.display.text = str(result)
            except Exception:
                self.display.text = "Error"

        else:
            if current == "0" or current == "Error":
                self.display.text = value
            else:
                self.display.text += value

    def safe_calculate(self, expression):
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.USub: operator.neg
        }

        def evaluate(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Invalid")

            elif isinstance(node, ast.BinOp):
                op = operators[type(node.op)]
                return op(
                    evaluate(node.left),
                    evaluate(node.right)
                )

            elif isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](
                    evaluate(node.operand)
                )

            else:
                raise ValueError("Invalid expression")

        return evaluate(ast.parse(expression, mode="eval").body)


if __name__ == "__main__":
    CalculatorApp().run()
