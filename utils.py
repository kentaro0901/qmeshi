"""djangoに依存しない汎用処理"""
import unicodedata


def lcs(S, T):
    """最長共通部分列"""
    L1 = len(S)
    L2 = len(T)
    dp = [[0]*(L2+1) for i in range(L1+1)]

    for i in range(L1-1, -1, -1):
        for j in range(L2-1, -1, -1):
            r = max(dp[i+1][j], dp[i][j+1])
            if S[i] == T[j]:
                r = max(r, dp[i+1][j+1] + 1)
            dp[i][j] = r

    res = []
    i = 0
    j = 0
    while i < L1 and j < L2:
        if S[i] == T[j]:
            res.append(S[i])
            i += 1
            j += 1
        elif dp[i][j] == dp[i+1][j]:
            i += 1
        elif dp[i][j] == dp[i][j+1]:
            j += 1
    return ''.join(res)


def get_char_width(c):
    data = unicodedata.east_asian_width(c)
    if data == 'Na' or data == 'H':
        return 1
    return 2


def get_string_width(string):
    width = 0
    for c in string:
        width += get_char_width(c)
    return width
