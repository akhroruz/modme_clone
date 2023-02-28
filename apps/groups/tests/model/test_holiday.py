from datetime import date

import pytest

from groups.models import Branch, Holiday, Company


@pytest.mark.django_db
class TestHolidayModel:
    def test_holiday(self):
        company = Company.objects.create(name='test_company')  # noqa
        branch = Branch.objects.create(
            name='test branch',
            address='test branch address',
            phone='934341245',
            about='test branch about',
            image='branch_image.png',
            company=company
        )
        data = {
            'name': 'test_name',
            'holiday_date': date(2023, 12, 25),
            'affect_payment': False,
            'branch': branch
        }
        holiday_count = Holiday.objects.count()
        holiday = Holiday.objects.create(**data)

        assert holiday.name == data['name']
        assert holiday.holiday_date == data['holiday_date']
        assert not holiday.affect_payment
        assert branch == branch
        assert str(holiday) == holiday.name
        assert holiday_count + 1 == Holiday.objects.count()
