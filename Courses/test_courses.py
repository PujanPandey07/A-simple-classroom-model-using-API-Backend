import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Enrollment, CourseInstructor

User = get_user_model()

# ─────────────────────────────────────────
# FIXTURES — reusable setup for your tests
# ─────────────────────────────────────────


@pytest.fixture
def api_client():
    # this gives every test a fresh APIClient (like a fresh Postman)
    return APIClient()


@pytest.fixture
def admin_user(db):
    # creates a real admin user in the test database
    return User.objects.create_superuser(
        username='admin',
        password='adminpass123',
        email='admin@test.com'
    )


@pytest.fixture
def student_user(db):
    # creates a regular student user
    return User.objects.create_user(
        username='student',
        password='studentpass123',
        email='student@test.com'
    )


@pytest.fixture
def instructor_user(db):
    # creates an instructor user
    return User.objects.create_user(
        username='instructor',
        password='instructorpass123',
        email='instructor@test.com'
    )


@pytest.fixture
def course(db):
    # creates a real course in the test database
    return Course.objects.create(
        title='Django REST Framework Course',
        description='Learn DRF from scratch',
        price=49.99,
        published=True
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    # returns an APIClient already logged in as admin
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def student_client(api_client, student_user):
    # returns an APIClient already logged in as student
    api_client.force_authenticate(user=student_user)
    return api_client


@pytest.fixture
def instructor_client(api_client, instructor_user):
    # returns an APIClient already logged in as instructor
    api_client.force_authenticate(user=instructor_user)
    return api_client

# ─────────────────────────────────────────
# COURSE TESTS
# ─────────────────────────────────────────


@pytest.mark.django_db
class TestCourseEndpoints:

    def test_anyone_can_list_courses(self, api_client, course):
        """
        Even unauthenticated users should be able
        to see the list of courses
        """
        response = api_client.get('/api/courses/')
        assert response.status_code == status.HTTP_200_OK

    def test_anyone_can_retrieve_single_course(self, api_client, course):
        """
        Anyone can view a single course detail
        """
        response = api_client.get(f'/api/courses/{course.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_create_course(self, admin_client):
        """
        Admin should be able to create a course
        """
        data = {
            'title': 'New Python Course',
            'description': 'Learn Python deeply',
            'price': 29.99,
            'published': True
        }
        response = admin_client.post('/api/courses/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.count() == 1  # confirm it was saved

    def test_student_cannot_create_course(self, student_client):
        """
        Students should get 403 when trying to create a course
        """
        data = {
            'title': 'Hacked Course',
            'description': 'I should not be able to do this',
            'price': 0,
            'published': True
        }
        response = student_client.post('/api/courses/', data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_user_cannot_create_course(self, api_client):
        """
        Unauthenticated users should get 401
        """
        data = {
            'title': 'Hacked Course',
            'description': 'Should not work',
            'price': 0,
            'published': True
        }
        response = api_client.post('/api/courses/', data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_can_delete_course(self, admin_client, course):
        """
        Admin should be able to delete a course
        """
        response = admin_client.delete(f'/api/courses/{course.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Course.objects.count() == 0  # confirm it was deleted

    def test_student_cannot_delete_course(self, student_client, course):
        """
        Students should get 403 when trying to delete a course
        """
        response = student_client.delete(f'/api/courses/{course.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


# ─────────────────────────────────────────
# ENROLLMENT TESTS
# ─────────────────────────────────────────

@pytest.mark.django_db
class TestEnrollmentEndpoints:

    def test_student_can_enroll_in_course(self, student_client, course):
        """
        A student should be able to enroll in a course
        """
        response = student_client.post(
            f'/api/courses/{course.id}/enrollments/'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_student_cannot_enroll_twice(self, student_client, student_user, course):
        """
        The unique_together constraint should prevent double enrollment
        """
        # enroll once
        student_client.post(f'/api/courses/{course.id}/enrollments/')
        # try to enroll again
        response = student_client.post(
            f'/api/courses/{course.id}/enrollments/'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_student_only_sees_own_enrollments(
        self, student_client, student_user, instructor_user, course
    ):
        """
        A student should only see their own enrollments
        not other students enrollments
        """
        # enroll the student
        Enrollment.objects.create(student=student_user, course=course)
        # enroll someone else too
        Enrollment.objects.create(student=instructor_user, course=course)

        response = student_client.get(
            f'/api/courses/{course.id}/enrollments/'
        )
        assert response.status_code == status.HTTP_200_OK
        # student should only see 1 enrollment (their own)
        assert len(response.data['results']) == 1


# ─────────────────────────────────────────
# AUTHENTICATION TESTS
# ─────────────────────────────────────────

@pytest.mark.django_db
class TestAuthentication:

    def test_user_can_login_and_get_token(self, api_client, student_user):
        """
        A valid user should get access and refresh tokens
        """
        response = api_client.post('/api/accounts/token/', {
            'username': 'student',
            'password': 'studentpass123'
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data   # token exists
        assert 'refresh' in response.data  # refresh token exists

    def test_wrong_password_cannot_login(self, api_client, student_user):
        """
        Wrong credentials should return 401
        """
        response = api_client.post('/api/accounts/token/', {
            'username': 'student',
            'password': 'wrongpassword'
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_requires_token(self, api_client, course):
        """
        Hitting a protected endpoint without token should return 401
        """
        response = api_client.get(
            f'/api/courses/{course.id}/enrollments/'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
