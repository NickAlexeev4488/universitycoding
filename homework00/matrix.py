def dict_diff(dict1, dict2):
    a = {}
    for i in dict1:
        for j in dict2:
            if j == i and dict1[i] == dict2[j]:
                a[i] = dict1[i]
    return a


newdict1 = {'1': '14', '2': '17', '3': '24'}
newdict2 = {'1': '14', '3': '17', '2': '17'}
print(dict_diff(newdict1, newdict2))
