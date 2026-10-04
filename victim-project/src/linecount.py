def count_nonempty_lines(text: str) -> int:
    return sum(bool(line.strip()) for line in text.splitlines())


if __name__ == "__main__":
    print(count_nonempty_lines("one\n\ntwo\n"))
