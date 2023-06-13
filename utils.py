def set_locale(locale):
    with open('locale.txt', 'w', encoding='UTF-8') as f:
        f.write(locale)


def get_locale():
    with open('locale.txt', 'r', encoding='UTF-8') as f:
        locale = f.read()
    return locale
