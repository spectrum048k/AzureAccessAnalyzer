import datetime_helper


def test_get_last_hour():
    last_hour, now = datetime_helper.get_last_hour()
    print(type(last_hour))
    assert last_hour < now


def test_get_last_day():
    last_day, now = datetime_helper.get_last_day()
    assert last_day < now


def test_get_last_week():
    last_week, now = datetime_helper.get_last_week()
    assert last_week < now


def test_get_last_n_hours():
    last_n_hours, now = datetime_helper.get_last_n_hours(3)
    assert last_n_hours < now


def test_get_last_n_hours_negative():
    try:
        last_n_hours, now = datetime_helper.get_last_n_hours(-3)
        assert False
    except ValueError:
        assert True
