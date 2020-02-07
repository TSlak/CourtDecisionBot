def readyThisNumber(link, user_id):
    f = open('SubscribeCourt.txt', 'r')
    for line in f.readlines():
        arg = line.split(',')
        if arg[0] == user_id and arg[1].find(link) > -1:
            f.close()
            return True
    f.close()
    return False


def save(user_id, link):
    if readyThisNumber(link, user_id):
        f = open('SubscribeCourt.txt', 'a+')
        f.write(user_id + "," + link + '\n')
        f.close()
