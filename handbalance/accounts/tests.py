from django.contrib.auth.models import User
from django.test import TestCase
from .models import TaskList, TaskBlock
from datetime import date


class TaskListTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(id=42, username='abc', password='12345')
        TaskList.objects.create(user=test_user, balance=5, last_activity="2021-02-20")
        self.test_user = TaskList.objects.get(user=test_user)
        self.MAX_BALANCE = 25

    def test_balance_value(self):
        self.assertLess(self.test_user.balance, self.MAX_BALANCE)
        self.assertGreater(self.test_user.balance, 0)

    def test_last_activity_type(self):
        self.assertEqual(type(self.test_user.last_activity), date)

    def test_user_type(self):
        self.assertEqual(type(self.test_user.user), User)


class TaskBlockTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(id=42, username='abc', password='12345')
        TaskBlock.objects.create(user=test_user, block_id=1, tasks=2, tasks_count=3)
        self.test_block = TaskBlock.objects.get(user=test_user)
        self.MAX_TASKS = 12

    def test_tasks(self):
        self.assertLess(self.test_block.tasks, 12)
