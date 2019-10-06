nums = [str(x) for x in range(10) if x != 1] + ['j', 'q', 'k', 'a']
suits = ['d', 'h', 'c', 's']

out = []
label = 0
for s in suits:
    for n in nums:
        out.append(s + n)
        print(f"{label}: {s + n}")
        label += 1
