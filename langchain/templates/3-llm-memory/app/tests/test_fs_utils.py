import time
import unittest

from services.fs_utils import get_safe_file_name


class TestFsUtils(unittest.TestCase):
    def test_get_safe_file_name(self):
        file_name = "This is A test "
        current_timestamp = int(time.time())
        expected_file_name = f"this_is_a_test-{current_timestamp}.txt"
        real_file_name = get_safe_file_name(file_name)

        self.assertEqual(expected_file_name, real_file_name, "The file name is wrong.")

    def test_get_safe_file_name_with_extension(self):
        file_name = "This is A test "
        file_extension = ".md"
        current_timestamp = int(time.time())
        expected_file_name = f"this_is_a_test-{current_timestamp}{file_extension}"
        real_file_name = get_safe_file_name(file_name, file_extension)

        self.assertEqual(expected_file_name, real_file_name, "The file name is wrong.")


if __name__ == "__main__":
    unittest.main()
