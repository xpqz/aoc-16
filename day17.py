import hashlib
import heapq

def get_digest(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()[:4]

def move(pos, door):
    return {
        "U": (pos[0], pos[1]-1), "D": (pos[0], pos[1]+1),
        "L": (pos[0]-1, pos[1]), "R": (pos[0]+1, pos[1])
    }[door]

def open_doors(pos, key):
    doors = ""
    digest = get_digest(key)
    for i in range(4):
        if digest[i] in {"b", "c", "d", "e", "f"}:
            door = ["U", "D", "L", "R"][i]
            new_pos = move(pos, door)
            if 0 <= new_pos[0] <= 3 and 0 <= new_pos[1] <= 3:
                doors += door

    return doors

def neighbours(pos, doors):
    for door in doors:
        yield move(pos, door), door

def breadth_first_search(seed, start_point=(0, 0), end_point=(3, 3)):
    frontier = []
    start = start_point + (open_doors(start_point, seed),)
    heapq.heappush(frontier, (0, start, ""))

    while frontier:
        item = heapq.heappop(frontier)

        current = item[1]
        path = item[2]

        pos = current[:-1]
        doors = current[-1]

        if pos == end_point:
            break

        for new_pos, door in neighbours(pos, doors):
            new_path = path + door
            key = seed + new_path
            new_doors = open_doors(new_pos, key)

            if not new_doors and new_pos != end_point:
                continue

            neighbour = new_pos + (new_doors,)
            heapq.heappush(frontier, (len(new_path), neighbour, new_path))

    return path


def longest_path(seed, start_point=(0, 0), end_point=(3, 3)):
    frontier = []
    start = start_point + (open_doors(start_point, seed),)
    heapq.heappush(frontier, (0, start, ""))

    maxlen = 0

    while frontier:
        item = heapq.heappop(frontier)

        current = item[1]
        path = item[2]

        pos = current[:-1]
        doors = current[-1]

        if pos == end_point:
            if len(path) > maxlen:
                maxlen = len(path)
            continue

        for new_pos, door in neighbours(pos, doors):
            new_path = path + door
            key = seed + new_path
            new_doors = open_doors(new_pos, key)

            if not new_doors and new_pos != end_point:
                continue

            neighbour = new_pos + (new_doors,)
            heapq.heappush(frontier, (len(new_path), neighbour, new_path))

    return maxlen


if __name__ == "__main__":
    seed = "qzthpkfp"

    print(breadth_first_search(seed))
    print(longest_path(seed))
