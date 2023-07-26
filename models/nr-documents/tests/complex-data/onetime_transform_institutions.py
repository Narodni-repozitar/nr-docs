import re

import openpyxl
from unidecode import unidecode

# nasty
rowidx = 0


def next_row(it):
    global rowidx
    rowidx += 1
    return [x.value for x in next(it)]


def empty(r):
    for val in r:
        if val:
            return False
    return True


wb_obj = openpyxl.load_workbook("tests/complex-data/institutions_old.xlsx")
sheet_obj = wb_obj.active


it = sheet_obj.iter_rows()

stack = []
ids = set()

shortcuts = {
    "fakulta-jaderna-a-fyzikalne-inzenyrska": "FJFI",
    "prirodovedecka": "Pr",
    "pedagogicka": "Ped",
    "filozoficka": "F",
    "strojni": "St",
}

try:
    row = next_row(it)
    while empty(row):
        row = next_row(it)
    while not empty(row):
        row = next_row(it)
    while empty(row):
        row = next_row(it)
    header = True
    while True:
        if not empty(row):
            if header:
                assert row[0] == "level"
                assert row[1] == "slug"
                assert row[7] == "props.acronym"

                sheet_obj.cell(row=rowidx, column=1).value = "hierarchy.parent"
                sheet_obj.cell(row=rowidx, column=2).value = "id"
                header = False
                row = next_row(it)
                continue

            level = int(row[0])
            slug = re.sub(r"\W+", "-", row[2].lower().strip())
            while level <= len(stack):
                stack.pop()
            if stack:
                parent, base = stack[-1]
            else:
                parent, base = ("", "")
            id = str(row[7] or slug)
            split_id = []
            if id.endswith("-cas"):
                split_id = [id]
            else:
                for word in id.split("-"):
                    if word in shortcuts:
                        split_id.append(shortcuts[word])
                        continue
                    for ci, c in enumerate(word):
                        if ci == 0 or c == c.upper():
                            split_id.append(c.upper())
            short_id = "".join(split_id)

            if base:
                id = f"{base}-{id}"
                short_id = f"{base}-{short_id}"

            if short_id not in ids and len(short_id) > 2:
                base = short_id
            else:
                base = id
            id = unidecode(id.lower())
            assert id not in ids

            print(id, str(row[7] or slug))

            ids.add(id)
            stack.append((id, base))
            sheet_obj.cell(row=rowidx, column=1).value = parent
            sheet_obj.cell(row=rowidx, column=2).value = id

        row = next_row(it)
except StopIteration:
    pass


wb_obj.save("tests/complex-data/institutions.xlsx")
