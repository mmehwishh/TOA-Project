import tkinter as tk
from tkinter import messagebox


class UnaryMultiplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unary Multiplication - Turing Machine")
        self.root.geometry("900x650")
        self.root.configure(bg="#ffffff")

        self.tape = []
        self.position = 0
        self.state = 0
        self.accept_states = {10}
        self.history = []

        self.transitions = [
            [{'read': '1', 'write': '_', 'move': 'r', 'new_state': 1}, {'read': '*', 'write': '_', 'move': 'r', 'new_state': 9}],
            [{'read': '1', 'write': '1', 'move': 'r', 'new_state': 1}, {'read': '*', 'write': '*', 'move': 'r', 'new_state': 2}],
            [{'read': '1', 'write': 'x', 'move': 'r', 'new_state': 3}, {'read': '_', 'write': '_', 'move': 'l', 'new_state': 7}],
            [{'read': '1', 'write': '1', 'move': 'r', 'new_state': 3}, {'read': '_', 'write': '_', 'move': 'r', 'new_state': 4}],
            [{'read': '1', 'write': '1', 'move': 'r', 'new_state': 4}, {'read': '_', 'write': '1', 'move': 'l', 'new_state': 5}],
            [{'read': '1', 'write': '1', 'move': 'l', 'new_state': 5}, {'read': '_', 'write': '_', 'move': 'l', 'new_state': 6}],
            [{'read': '1', 'write': '1', 'move': 'l', 'new_state': 6}, {'read': 'x', 'write': 'x', 'move': 'r', 'new_state': 2}],
            [{'read': 'x', 'write': '1', 'move': 'l', 'new_state': 7}, {'read': '*', 'write': '*', 'move': 'l', 'new_state': 8}],
            [{'read': '1', 'write': '1', 'move': 'l', 'new_state': 8}, {'read': '_', 'write': '_', 'move': 'r', 'new_state': 0}],
            [{'read': '1', 'write': '_', 'move': 'r', 'new_state': 9}, {'read': '_', 'write': '_', 'move': 'r', 'new_state': 10}]
        ]

        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root, bg="#ffffff", pady=10)
        input_frame.pack(pady=20)

        entry_style = {"font": ("Arial", 14), "relief": "groove", "bd": 2, "width": 18, "justify": "center"}

        tk.Label(input_frame, text="Number 1:", bg="#ffffff", font=("Arial", 14)).grid(row=0, column=0, padx=15, pady=10)
        self.num1_entry = tk.Entry(input_frame, **entry_style)
        self.num1_entry.grid(row=0, column=1, padx=15, pady=10)

        tk.Label(input_frame, text="Number 2:", bg="#ffffff", font=("Arial", 14)).grid(row=0, column=2, padx=15, pady=10)
        self.num2_entry = tk.Entry(input_frame, **entry_style)
        self.num2_entry.grid(row=0, column=3, padx=15, pady=10)

        buttons_frame = tk.Frame(self.root, bg="#ffffff")
        buttons_frame.pack(pady=15)

        button_style = {
            "bg": "#3366cc", "fg": "white", "font": ("Arial", 12, "bold"),
            "bd": 0, "relief": "solid", "activebackground": "#2547a5",
            "activeforeground": "white", "width": 14, "height": 2
        }

        self.start_button = tk.Button(buttons_frame, text="Start", command=self.start, **button_style)
        self.start_button.grid(row=0, column=0, padx=8)

        self.reset_button = tk.Button(buttons_frame, text="Reset", command=self.reset, **button_style)
        self.reset_button.grid(row=0, column=1, padx=8)

        self.step_button = tk.Button(buttons_frame, text="Step Forward", command=self.step_forward, **button_style)
        self.step_button.grid(row=0, column=2, padx=8)

        self.step_back_button = tk.Button(buttons_frame, text="Step Backward", command=self.step_backward, **button_style)
        self.step_back_button.grid(row=0, column=3, padx=8)

        self.final_button = tk.Button(buttons_frame, text="Go Final", command=self.go_final, **button_style)
        self.final_button.grid(row=0, column=4, padx=8)

        tape_frame = tk.Frame(self.root, bg="#e6ecf0", bd=3, relief="ridge")
        tape_frame.pack(padx=30, pady=10, fill="both", expand=True)

        self.tape_display = tk.Text(tape_frame, height=8, width=95, bg="#f5f7fa",
                                    font=("Courier", 14), bd=0, relief="flat")
        self.tape_display.pack(pady=10, padx=10, fill="both", expand=True)

        self.output_label = tk.Label(self.root, text="Output: ", bg="#ffffff", font=("Arial", 18, "bold"), fg="#0f3460")
        self.output_label.pack(pady=20)

    def start(self):
        try:
            num1 = int(self.num1_entry.get())
            num2 = int(self.num2_entry.get())
            self.num1 = num1
            self.num2 = num2
            self.tape = ['1'] * num1 + ['*'] + ['1'] * num2
            self.position = 0
            self.state = 0
            self.history.clear()
            self.save_history()
            self.update_tape_display()
            self.output_label.config(text="Output: ")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers.")

    def reset(self):
        self.tape.clear()
        self.position = 0
        self.state = 0
        self.history.clear()
        self.num1_entry.delete(0, tk.END)
        self.num2_entry.delete(0, tk.END)
        self.tape_display.delete('1.0', tk.END)
        self.output_label.config(text="Output: ")

    def step_forward(self):
        if self.state in self.accept_states:
            return

        read_val = self.tape[self.position] if self.position < len(self.tape) else '_'

        for transition in self.transitions[self.state]:
            if transition['read'] == read_val:
                self.tape[self.position] = transition['write']

                if transition['move'] == 'r':
                    self.position += 1
                    if self.position >= len(self.tape):
                        self.tape.append('_')
                else:
                    self.position = max(0, self.position - 1)

                self.state = transition['new_state']
                self.save_history()
                self.update_tape_display()

                if self.state in self.accept_states:
                    product = self.num1 * self.num2
                    unary = '1' * product
                    self.output_label.config(text=f"Decimal Product: {product} | Unary: {unary}")
                break

    def step_backward(self):
        if len(self.history) > 1:
            self.history.pop()
            last_snapshot = self.history[-1]
            self.tape = last_snapshot['tape'].copy()
            self.position = last_snapshot['position']
            self.state = last_snapshot['state']
            self.update_tape_display()

    def go_final(self):
        while self.state not in self.accept_states:
            self.step_forward()

    def save_history(self):
        self.history.append({
            'tape': self.tape.copy(),
            'position': self.position,
            'state': self.state
        })

    def update_tape_display(self):
        self.tape_display.delete('1.0', tk.END)
        display = ""

        for i, symbol in enumerate(self.tape):
            if i == self.position:
                display += f"[{symbol}]"
            else:
                display += symbol

        state_info = f"\n\nState: {self.state}    |    Head Position: {self.position}"

        self.tape_display.insert(tk.END, display + state_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = UnaryMultiplicationGUI(root)
    root.mainloop()