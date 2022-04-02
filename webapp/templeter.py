

def createList(photos):
    ans = []
    idx = 0
    while idx < len(photos):
        ans.append('<img src=static/images/' + photos[idx] + '>')
        idx += 1
    return ans