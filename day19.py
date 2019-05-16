def gen(elves):
    new_elves = []
    for pos in range(len(elves)):
        if elves[pos]["presents"] == 0:
            continue
        target = (pos+1)%len(elves)
        elves[pos]["presents"] += elves[target]["presents"]
        new_elves.append(elves[pos])
        elves[target]["presents"] = 0

    return list(filter(lambda x: x["presents"]>0, new_elves))

if __name__ == "__main__":
    elf_count = 3014603
    elves = [{"id": elf_id, "presents": 1} for elf_id in range(1, elf_count+1)]
    while len(elves) > 1:
        elves = gen(elves)
    print(elves)
