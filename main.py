s = "ELMRU"
cnt = 0
for c1 in s:
    for c2 in s:
        for c3 in s:
            for c4 in s:
                word = c1 + c2 + c3 + c4
                cnt += 1
                print(cnt, word)