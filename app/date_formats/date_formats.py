from datetime import datetime
import calendar


def get_str_date_1(year: int, month: int, day: int) -> str:
    """Преобразовывает дату в строку формата гггг-мм-дд"""
    if day >= 10:
        day = str(day)
    else:
        day = '0' + str(day)

    if month >= 10:
        month = str(month)
    else:
        month = '0' + str(month)

    year = str(year)

    return f'{year}-{month}-{day}'


def get_str_date_2(year, month, day):
    """Преобразовывает дату в строку формата дд.мм.гггг"""
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    year = str(year)
    return f'{day}.{month}.{year}'


def transform_date_to_int(year, month, day) -> int:
    """Преобразовывает дату в целочисленное значение"""
    dt = datetime(year, month, day)
    return int(round(dt.timestamp() * 1000))


def str_to_int_time(time_str):
    """Get Seconds from time."""
    if time_str == '0':
        return 0
    else:
        h, m, s = time_str.split(':')
        return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000


def get_first_last_this_month_dates():
    today_date = datetime.now().strftime('%Y-%m-%d')
    year = (today_date.split('-')[0])
    month = (today_date.split('-')[1])
    last_day = calendar._monthlen(int(year), int(month))
    dates = {'first_date': f'{year}-{month}-01', 'last_date': f'{year}-{month}-{last_day}'}
    return dates


if __name__ == '__main__':
    print(get_first_last_this_month_dates())
