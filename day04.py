from collections import Counter
import re

def read_data(filename="data/input04.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    result = []
    p = re.compile(r"^(\d+)\[([^\]]+)\]$")
    for line in lines:
        components = line.split("-")
        letters = components[:-1]
        m = p.match(components[-1])
        result.append((letters, int(m.group(1)), m.group(2)))

    return result

def verify(row):
    letter_list, _value, checksum = row

    letters = "".join(letter_list)
    c = Counter(letters)

    # The checksum is the five most common letters
    for i in letters:
        if i not in checksum:
            for j in checksum:
                if c[i] > c[j]:
                    return False


    # Must be sorted in descending order
    distribution = [c[i] for i in checksum]
    if not all(x >= y for x, y in zip(distribution, distribution[1:])):
        return False

    # Equal neighbours must appear alphabetically in the checksum
    for i in range(1, len(distribution)):
        if distribution[i-1] == distribution[i]:
            if checksum[i-1] > checksum[i]:
                return False

    return True

def decrypt(row):
    alphabet = list(map(chr, range(97, 123)))
    decrypted = []
    for word in row[0]:
        new_word = ""
        for letter in word:
            i = ord(letter) - ord('a')
            shifted_index = (i+row[1])%len(alphabet)
            new_word += alphabet[shifted_index]
        decrypted.append(new_word)

    return decrypted


if __name__ == "__main__":
    data = parse_data(read_data())

    print(sum(item[1] for item in filter(verify, data)))

    for r in filter(verify, data):
        words = decrypt(r)
        if "northpole" in words:
            print(r, words)
            break
