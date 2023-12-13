def dict_diff(dict1, dict2):
    a = {}
    for i in dict1:
        for j in dict2:
            if j == i and dict1[i] == dict2[j]:
                a[i] = dict1[i]
    return a


newdict1 = {'1': '14', '2': '17'}
newdict2 = {'1': '16', '3': '19'}

