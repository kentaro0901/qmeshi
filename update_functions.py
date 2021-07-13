# 邪魔なので分割
import re

tag_dict = {'C丼':'丼', 'HALA  L対応':'HALAL', 'HALAL  カレー':'HALAL', 'とり天・豚汁':'定食', 'カレー':'カレー', 'カレー  定番':'カレー', 'カレー定番':'カレー', 'カレー類（スープなし）':'カレー', 'クイック丼':'丼', 'サラダ/スープ':'副菜', 'スープ/サラダ他':'副菜', 'スープ・サラダ':'副菜', 'デザート':'その他', 'パスタ':'麺', 'ビーフ丼':'丼', 'プレートランチMスープ付':'定食', 'プレートランチSスープ付':'定食', 'ボール':'丼', 'マグロ丼':'丼', 'ランチ':'定食', '主菜  (焼･炒･煮)':'主菜', '主菜（揚）':'主菜', '主菜（魚）':'主菜', '丼':'丼', '丼他':'丼', '和麺定番  うどん':'麺', '固定うどん':'麺', '固定丼':'丼', '夕メニュー�@':'定食', '夕メニュー�A':'定食', '夜メニュー':'定食', '夜限定メニュー':'定食', '定番うどん':'麺', '定番カレー':'カレー', '定番丼':'丼', '定番（麺）':'麺', '定番：唐揚':'主菜', '定番：麻婆':'主菜', '定食':'定食', '手作りカレー':'カレー' ,'揚':'主菜', '揚げ':'主菜', '揚げ２':'主菜', '揚げ３':'主菜', '揚げ４':'主菜', '日替り定食':'定食', '日替アグリ定食':'定食', '日替定食':'定食', '炒め':'主菜', '焼・炒・煮':'主菜', '豚丼':'丼', '週替':'カレー', '週替1':'麺', '週替2':'麺', '週替3':'麺', '週替うどん':'麺', '週替うどん  (月・火・水）':'麺', '週替うどん  (木・金）':'麺', '週替うどん1':'麺', '週替うどん2':'麺', '週替わり':'カレー', '週替カレー':'カレー', '週替ラーメン  (月・火・水）':'麺', '週替ラーメン  (木・金）':'麺', '週替中華麺':'麺', '週替中華麺1':'麺', '週替中華麺2':'麺', '週替麺A':'麺', '週替麺B':'麺', '週替麺C':'麺', '週替麺D':'麺', '魚':'主菜', '魚丼':'丼', '魚丼1':'丼', '魚丼2':'丼', '鮭丼':'丼', '鶏/豚丼':'丼', '鶏丼':'丼', '鶏丼/豚丼':'丼', '鶏天定食':'定食', '麺定番':'麺', '麺定番  うどん':'麺', '麻婆系':'主菜'}
def summarized_tag(tag):
    if type(tag) != str:
        return 'その他'
    else:
        if tag in tag_dict:
            return tag_dict[tag]
        else:
            return 'その他'

## ここ要検討
def fit_string(s):
    if type(s) != str:
        return s
    tmp = []
    for sep in s.split('/'):
        tmp.append(sep.replace('　', '').replace(' ','').replace('（','(').replace('）',')').replace('★', '').strip())
        #sep = re.sub(r'(\w+)(\(.+\))?', r'\1', sep)
    return '/'.join(tmp)

def summarized_menu(menu):
    return menu

#最長共通部分列
def lcs(S, T):
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
    i = 0; j = 0
    while i < L1 and j < L2:
        if S[i] == T[j]:
            res.append(S[i])
            i += 1; j += 1
        elif dp[i][j] == dp[i+1][j]:
            i += 1
        elif dp[i][j] == dp[i][j+1]:
            j += 1
    return ''.join(res)