# import pytest
#
# from groups.models import Company, Branch, Room, Course, Holiday
#
#
# @pytest.mark.django_db
# class TestCompanyModel:
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(name='PDP')
#         return company
#
#     def test_company(self, company):
#         assert company.name == 'PDP'
#         assert str(company) == company.name
#
#
# @pytest.mark.django_db
# class TestBranchModel:
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(name='Test Company')
#         return company
#
#     @pytest.fixture
#     def branch(self, company):  # noqa
#         branch = Branch.objects.create(
#             name='Test Branch',
#             address='Test Address',
#             company=company,
#             phone='1234567890',
#             about='Test About',
#             image='test.png'
#         )
#         return branch
#
#     def test_branch_model(self, branch, company):  # noqa
#         assert branch.name == 'Test Branch'
#         assert branch.address == 'Test Address'
#         assert branch.phone == '1234567890'
#         assert branch.about == 'Test About'
#         assert branch.image == 'test.png'
#         assert str(branch) == branch.name
#         assert str(company) == company.name
#         assert branch.company.name == 'Test Company'
#
#
# @pytest.mark.django_db
# class TestRoomModel:
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(name='ECMA')
#         return company
#
#     @pytest.fixture
#     def branch(self, company):
#         branch = Branch.objects.create(
#             name='test_name',
#             address='test_address',
#             company=company,
#             phone='932233445',
#             about='test_about',
#             image='test_image.png'
#         )
#         return branch
#
#     @pytest.fixture
#     def room(self, branch):
#         room = Room.objects.create(
#             name='test_name',
#             branch=branch
#         )
#         return room
#
#     def test_room_model(self, room, branch):
#         assert room.name == 'test_name'
#         assert room.branch == branch
#         assert str(room) == room.name
#
#
# @pytest.mark.django_db
# class TestCourseModel:
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(name='test_name')
#         return company
#
#     @pytest.fixture
#     def course(self, company):
#         course = Course.objects.create(
#             name='test_name',
#             price=500,
#             description='test_description',
#             image='test_image.png',
#             lesson_duration=3,
#             course_duration=6,
#             company=company
#         )
#         return course
#
#     def test_course_model(self, company, course):
#         assert course.name == 'test_name'
#         assert course.price == 500
#         assert course.description == 'test_description'
#         assert course.image == 'test_image.png'
#         assert course.lesson_duration == 3
#         assert course.course_duration == 6
#         assert course.company == company
#         assert str(course) == course.name
#
#
# @pytest.mark.django_db
# class TestHolidayModel:
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(name='test_company')
#         return company
#
#     @pytest.fixture
#     def branch(self, company):
#         branch = Branch.objects.create(
#             name='test_name',
#             address='test_address',
#             company=company,
#             phone='933432343',
#             about='test_about',
#             image='test_image.png',
#         )
#         return branch
#
#     @pytest.fixture
#     def holiday(self, branch):
#         holiday = Holiday.objects.create(
#             name='test_name',
#             holiday_date='2000-12-20',
#             affect_payment=False,
#             branch=branch
#         )
#         return holiday
#
#     def test_holiday_model(self, holiday, branch):
#         assert holiday.name == 'test_name'
#         assert holiday.holiday_date == '2000-12-20'
#         assert not holiday.affect_payment
#         assert branch == branch
#         assert str(holiday) == holiday.name
