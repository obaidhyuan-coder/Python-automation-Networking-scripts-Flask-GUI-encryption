from pathlib import Path
import re
from collections import Counter

# Count how many lines are in the text file.
def count_line(path: Path):
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        return len(lines)

# Count words in the file using a simple regex tokenizer.
def count_word(path: Path) -> Counter:
    counter = Counter()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            tokens = re.findall(r"\w+", line.lower())
            counter.update(tokens)
    return counter

# Build a summary of the file: line count, total words, unique words, and top words.
def file_summary(path: Path, top_n: int = 10) -> dict:
    lines = count_line(path)
    word_counts = count_word(path)
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    most_common = word_counts.most_common(top_n)
    avg_words_per_line = total_words / max(lines, 1)
    return {
        "lines": lines,
        "total_words": total_words,
        "unique_words": unique_words,
        "top": most_common,
        "avg_words_per_line": avg_words_per_line,
    }


def main():
    path = Path("sword.txt")
    count = count_word(path)
    summary = file_summary(path,top_n=10)
    occurences = summary["top"]
    print(lines := summary["lines"])
    print(f"Total words: {summary['total_words']}")
    print(f"Unique words: {summary['unique_words']}")
    print(f"Average words per line: {summary['avg_words_per_line']:.2f}")
    print("Most common words:")
    for word, freq in occurences:
        print(f"  {word}: {freq}")
    print("All word counts:")
    for word, freq in count.items():
        print(f"  {word}: {freq}")
if __name__ == "__main__":
    main()