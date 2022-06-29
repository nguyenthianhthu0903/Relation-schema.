
# attributes = "ABCDGH"
# rel= "S->MR; NS->QM; PQ->RS; MO->NR; N->R"
# rel = "AB->C; B->D; A->GH"

def xuliInput():
    f = open('caua.txt', 'r')
    qa = f.readlines()

    attributes = qa[0].replace("\n", "")
    rel = qa[1]

    foo = list(rel.split(';'))
    FDs = {}
    for i in foo:
        temp = i.split('->')
        FDs[temp[0].strip()] = temp[1]
    return [attributes, FDs]


attributes = xuliInput()[0]
foo = xuliInput()[1]

# R is relation schema, FDs is functional dependencies


def findClosure(attr, R, FDs):
    closureOfAttr = set(attr)
    closureOfOldAttr = None

    while closureOfOldAttr != closureOfAttr:
        closureOfOldAttr = closureOfAttr
        for FD in FDs:
            if set(FD).issubset(closureOfAttr):
                closureOfAttr = closureOfAttr.union(FDs[FD])

    return closureOfAttr

# bar = findClosure('MO', attributes, foo)
# print(findClosure('OP', attributes, foo))


def findCandidateKeys(R, FDs):
    # Xac dinh cac thuộc tính trái phải
    left = set()
    right = set()
    for k, v in FDs.items():
        left.update(set(k))
        right.update(set(v))

    # Tìm tập đích, trung gian, nguồn
    target = right.difference(left)
    mid = left.intersection(right)
    source = set(R).difference(target.union(mid))

    # Tìm tập con của tập trung gian
    import itertools
    temp = []
    for i in range(len(mid)+1):
        temp.extend(list(itertools.combinations(mid, i)))
    subsets = [list(i) for i in temp]

    # Xác định khóa
    keys = [list(source) + subsets[i] for i in range(len(subsets))
            if findClosure(list(source) + subsets[i], R, foo) == set(R)]

    # Loại bỏ siêu khóa
    temp = [keys[j] for i in range(len(keys)) for j in range(
        i+1, len(keys)) if (all(item in keys[j] for item in keys[i]))]
# Explain:
    # temp = [] # list chứa các tập cha của candidate keys
    # for i in range(len(keys)): # duyệt từng khóa
    #   for j in range(i+1, len(keys)): # và xét với các khóa còn lại
    #     if (all(item in keys[j] for item in keys[i])): # nếu khóa keys[i] là con của keys[j]
    #       temp.append(keys[j]) # thêm khóa keys[j] vào temp
    candidateKeys = [item for item in keys if item not in temp]
    return candidateKeys


print("Tất cả các khoá của lược đồ trên là: ",findCandidateKeys(attributes, foo))
