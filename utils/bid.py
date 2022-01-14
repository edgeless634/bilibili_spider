"""
BV号解密
"""
table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
tr = {}
for i in range(58):
	tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def decode(x):
    """
    解密格式为 BVxxxxxx 的视频号为B站aid(AV号)
    """
    r = 0
    for i in range(6):
        r += tr[x[s[i]]]*58**i
    return (r-add)^xor

def encode(x):
    """
    加密B站aid(AV号)为格式为 BVxxxxxx 的视频号
    """
    x=(x^xor)+add
    r=list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]]=table[x//58**i%58]
    return ''.join(r)


if __name__ == "__main__":
    print(decode('BV17x411w7KC'))
    print(encode(977937344))