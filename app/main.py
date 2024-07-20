import sys


class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        literal_str = "null" if self.literal is None else str(self.literal)
        return f"{self.type} {self.lexeme} {literal_str}"


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errors = []

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens, self.errors

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        char = self.advance()
        if char == "(":
            self.add_token("LEFT_PAREN")
        elif char == ")":
            self.add_token("RIGHT_PAREN")
        elif char == "{":
            self.add_token("LEFT_BRACE")
        elif char == "}":
            self.add_token("RIGHT_BRACE")
        elif char == ",":
            self.add_token("COMMA")
        elif char == ".":
            self.add_token("DOT")
        elif char == "-":
            self.add_token("MINUS")
        elif char == "+":
            self.add_token("PLUS")
        elif char == ";":
            self.add_token("SEMICOLON")
        elif char == "*":
            self.add_token("STAR")
        elif char == "!":
            if self.match("="):
                self.add_token("BANG_EQUAL")
            else:
                self.add_token("BANG")
        elif char == "=":
            if self.match("="):
                self.add_token("EQUAL_EQUAL")
            else:
                self.add_token("EQUAL")
        elif char == "<":
            if self.match("="):
                self.add_token("LESS_EQUAL")
            else:
                self.add_token("LESS")
        elif char == ">":
            if self.match("="):
                self.add_token("GREATER_EQUAL")
            else:
                self.add_token("GREATER")
        elif char == "/":
            if self.match("/"):
                # Single-line comment
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token("SLASH")
        elif char == "\n":
            self.line += 1
        elif char == " " or char == "\r" or char == "\t":
            pass
        elif char == '"':
            self.string()
        elif char.isdigit():
            self.number()
        else:
            self.error(f"Unexpected character: {char}")

    def is_digit(self, char):
        return '0' <= char <= '9'

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token("NUMBER", value)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error("Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token("STRING", value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def error(self, message):
        self.errors.append(f"[line {self.line}] Error: {message}")


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    scanner = Scanner(file_contents)
    tokens, errors = scanner.scan_tokens()

    for token in tokens:
        print(token)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
