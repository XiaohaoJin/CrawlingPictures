import re

nums = str(['共5'])

count = re.findall(r"\d+\.?\d*", nums)
for c in count:
    print(c, count)