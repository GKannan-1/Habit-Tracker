from django.test import TestCase
from django.db.models import QuerySet
from django.contrib.auth.models import User
from ..models import Habit, HabitTrackerUser


class HabitModelTestCase(TestCase):
    def setUp(self) -> None:
        user1: User = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.habit_tracker_user_1: HabitTrackerUser = HabitTrackerUser.objects.create(
            author=user1
        )

        user2: User = User.objects.create_user(
            username="testuser2",
            password="password",
        )
        self.habit_tracker_user_2: HabitTrackerUser = HabitTrackerUser.objects.create(
            author=user2
        )

        # habit_tracker_user_1 habits
        Habit.objects.create(
            title="Exercise",
            text="Do 30 minutes of exercise daily",
            owner=self.habit_tracker_user_1,
        )
        Habit.objects.create(
            title="Read",
            text="Do 30 minutes of reading daily",
            owner=self.habit_tracker_user_1,
        )

        # habit_tracker_user_2 habits
        Habit.objects.create(
            title="Clean",
            text="Clean your room daily",
            owner=self.habit_tracker_user_2,
        )
        Habit.objects.create(
            title="Build",
            text="Build your dollhouse for an hour daily",
            owner=self.habit_tracker_user_2,
        )

    def test_data_integrity_and_relationship_constraints(self) -> None:
        user_1_query_set: QuerySet[Habit] = Habit.objects.filter(
            owner=self.habit_tracker_user_1
        )
        user_2_query_set: QuerySet[Habit] = Habit.objects.filter(
            owner=self.habit_tracker_user_2
        )

        list_of_strings_user_1: list[str] = [str(habit) for habit in user_1_query_set]
        list_of_strings_user_1.sort()

        list_of_strings_user_2: list[str] = [str(habit) for habit in user_2_query_set]
        list_of_strings_user_2.sort()

        self.assertListEqual(["Habit: Exercise", "Habit: Read"], list_of_strings_user_1)
        self.assertListEqual(["Habit: Build", "Habit: Clean"], list_of_strings_user_2)

        user_1_query_set_reversed: QuerySet[Habit] = (
            self.habit_tracker_user_1.habits.all()
        )
        user_2_query_set_reversed: QuerySet[Habit] = (
            self.habit_tracker_user_2.habits.all()
        )

        list_of_strings_user_1_reversed: list[str] = [
            str(habit) for habit in user_1_query_set_reversed
        ]
        list_of_strings_user_1_reversed.sort()

        list_of_strings_user_2_reversed: list[str] = [
            str(habit) for habit in user_2_query_set_reversed
        ]
        list_of_strings_user_2_reversed.sort()

        self.assertListEqual(
            ["Habit: Exercise", "Habit: Read"],
            list_of_strings_user_1_reversed,
        )
        self.assertListEqual(
            ["Habit: Build", "Habit: Clean"],
            list_of_strings_user_2_reversed,
        )
