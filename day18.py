def tile(row, pos):
    r = f".{row}."
    p = pos + 1
    data = r[p-1:p+2]
    if data in {"^^.", ".^^", "^..", "..^"}:
        return "^"
    return "."

def new_row(row):
    r = ""
    for pos, _ in enumerate(row):
        r += tile(row, pos)
    return r

def safe_count(current_row, iterations):
    safe = current_row.count(".")
    for _ in range(iterations-1):
        current_row = new_row(current_row)
        safe += current_row.count(".")
    return safe

if __name__ == "__main__":
    current_row = ".^^^.^.^^^^^..^^^..^..^..^^..^.^.^.^^.^^....^.^...^.^^.^^.^^..^^..^.^..^^^.^^...^...^^....^^.^^^^^^^"

    print(safe_count(current_row, 40))
    print(safe_count(current_row, 400_000))
