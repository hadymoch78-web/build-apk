from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
}


def hitung(expr):
    try:
        tree = ast.parse(expr, mode="eval")
        return evaluasi(tree.body)
    except Exception:
        raise ValueError("Perhitungan tidak valid")


def evaluasi(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError()

    if isinstance(node, ast.BinOp):
        op = OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError()

        kiri = evaluasi(node.left)
        kanan = evaluasi(node.right)

        return op(kiri, kanan)

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -evaluasi(node.operand)

        if isinstance(node.op, ast.UAdd):
            return evaluasi(node.operand)

    raise ValueError()


class Calculator(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=8,
            padding=8,
            **kwargs
        )

        self.expression = ""

        self.display = Label(
            text="0",
            font_size=36,
            halign="right",
            valign="middle",
            size_hint_y=0.25
        )

        self.display.bind(size=self.update_text_size)

        self.add_widget(self.display)

        buttons = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        grid = GridLayout(
            cols=4,
            spacing=6,
            size_hint_y=0.75
        )

        for row in buttons:
            for text in row:
                button = Button(
                    text=text,
                    font_size=26
                )
                button.bind(on_press=self.press)
                grid.add_widget(button)

        self.add_widget(grid)
