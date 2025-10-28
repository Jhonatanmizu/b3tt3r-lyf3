from django.test import TestCase

from users.models import CustomUser


class UserModelTestCase(TestCase):
    def test_user_creation(self):
        user: CustomUser = CustomUser.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            password="testpassword",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.xp, 0)
        self.assertEqual(user.level, 1)

    def test_add_xp_and_level_up(self):
        user = CustomUser.objects.create(
            username="levelupuser",
            first_name="Level",
            last_name="Up",
            password="leveluppassword",
        )
        user.add_xp(250)
        self.assertEqual(user.xp, 250)
        self.assertEqual(user.level, 3)

    def test_fullname_method(self):
        user = CustomUser.objects.create(
            username="fullnameuser",
            first_name="Full",
            last_name="Name",
            password="fullnamenpassword",
        )
        self.assertEqual(user.fullname(), "Full Name")
        self.assertEqual(user.fullname(), "Full Name")

    def test_delete_method(self):
        user = CustomUser.objects.create(
            username="deleteuser",
            first_name="Delete",
            last_name="User",
            password="deletepassword",
        )
        user_id = user.id
        user.delete()
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

    def test_restore_method(self):
        user = CustomUser.objects.create(
            username="restoreuser",
            first_name="Restore",
            last_name="User",
            password="restorepassword",
        )
        user_id = user.id
        user.delete()
        restored_user = CustomUser.all_objects.filter(is_deleted=True).get(id=user_id)
        restored_user.restore()
        self.assertIsNotNone(CustomUser.objects.get(id=user_id))
