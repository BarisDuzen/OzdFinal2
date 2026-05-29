class PlateTuringRecognizer:
    BLANK = "_"

    DIGITS = set("0123456789")
    UPPERCASE_LETTERS = set("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ")

    DIGIT_MARK = "N"    
    LETTER_MARK = "L"  

    def __init__(self, plate):
        self.plate = plate
        self.tape = list(plate) + [self.BLANK]
        self.head = 0
        self.state = "q0"
        self.step_no = 0

        self.accept_state = "q_accept"
        self.reject_state = "q_reject"

        self.transitions = {
            ("q0", "DIGIT"):  ("q1", self.DIGIT_MARK,  "R"), #yeni durum,yazılacak ifade,kafa hareketi
            ("q1", "DIGIT"):  ("q2", self.DIGIT_MARK,  "R"),
            ("q2", "LETTER"): ("q3", self.LETTER_MARK, "R"),
            ("q3", "LETTER"): ("q4", self.LETTER_MARK, "R"),
            ("q4", "DIGIT"):  ("q5", self.DIGIT_MARK,  "R"),
            ("q5", "DIGIT"):  ("q6", self.DIGIT_MARK,  "R"),
            ("q6", "DIGIT"):  ("q7", self.DIGIT_MARK,  "R"),
            ("q7", "BLANK"):  ("q_accept", self.BLANK, "S"),
        }

    def tape_str(self):
        return "".join(self.tape)

    def read_symbol(self):
        if self.head >= len(self.tape):
            self.tape.append(self.BLANK)
        return self.tape[self.head]

    def symbol_type(self, symbol):
        if symbol in self.DIGITS:
            return "DIGIT"
        if symbol in self.UPPERCASE_LETTERS:
            return "LETTER"
        if symbol == self.BLANK:
            return "BLANK"
        return "OTHER"

    def write_symbol(self, symbol):
        self.tape[self.head] = symbol

    def move_head(self, direction):
        if direction == "R":
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append(self.BLANK)
        elif direction == "L":
            if self.head > 0:
                self.head -= 1
        elif direction == "S":
            pass

    def print_step(self, current_state, read, write, movement, next_state):
        print(
            f"Adım {self.step_no} | "
            f"Durum: {current_state} | "
            f"Okunan: {read} | "
            f"Yazılan: {write} | "
            f"Hareket: {movement} | "
            f"Yeni durum: {next_state} | "
            f"Bant: {self.tape_str()}"
        )
        self.step_no += 1

    def step(self):
        current_state = self.state
        read = self.read_symbol()
        read_type = self.symbol_type(read)

        transition_key = (current_state, read_type)

        if transition_key not in self.transitions:
            self.state = self.reject_state
            self.print_step(current_state, read, "-", "S", self.state)
            return

        next_state, write, movement = self.transitions[transition_key]

        self.write_symbol(write)

        self.state = next_state
        self.print_step(current_state, read, write, movement, self.state)
        self.move_head(movement)

    def run(self):
        print(f"Girdi bandı: {self.tape_str()}")
        print("Beklenen format: NNLLNNN")
        print("N = rakam (0-9), L = büyük harf (A-Z)\n")

        while self.state not in [self.accept_state, self.reject_state]:
            self.step()

        print()
        if self.state == self.accept_state:
            print("Sonuç: KABUL")
        else:
            print("Sonuç: RED")


def main():
    plate = input("Plaka bilgisini giriniz: ").strip()
    machine = PlateTuringRecognizer(plate)
    machine.run()


if __name__ == "__main__":
    main()
