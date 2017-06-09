import scrapgh


def one_user():
    # here your github username
    user_github = 'jack-factor222222'
    return scrapgh.get_index_data(user_github)


def multi_user():
    users_github = ['jack-factor', 'VictorAlberto87']
    result = []
    for user in users_github:
        if user is not None:
            result.append(scrapgh.get_index_data(user))
    return result


example1 = one_user()
example2 = multi_user()
if example1 is not None:
    print(example1['username'])
else:
    print('Not Found')

print('--------------------------------------')
print(example1)
print('--------------------------------------')
print(example2)
