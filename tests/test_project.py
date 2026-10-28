import unittest
import tempfile
import sys
from pathlib import Path

BACKEND_DIRECTORY = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIRECTORY))

# imports
import data
import chat_storage
from basic_info import read_basic_info
from keyword_manager import keyword_match, normalize_text, expand_user_input_with_language_terms


class KeywordManagerTests(unittest.TestCase):

    def test_normalize_text(self):
        text = normalize_text("Hello, OTH-Regensburg!")
        self.assertIn("hello", text)
        self.assertIn("oth", text)
        self.assertIn("regensburg", text)

    def test_basic_skill_is_detected(self):
        self.assertTrue(keyword_match("Where is building K at OTH Regensburg?", "BASIC"))

    def test_mensa_skill_is_detected(self):
        self.assertTrue(keyword_match("What can I eat tomorrow vegetarian in the Mensa?", "MENSA"))

    def test_stundenplan_skill_is_detected(self):
        self.assertTrue(keyword_match("Where is PG2 on Monday with Prof Schildgen?", "STUNDENPLAN"))

    def test_website_termine_skill_is_detected(self):
        self.assertTrue(keyword_match("When is the Rückmeldung deadline?", "WEB_TERMINE"))

    def test_website_pruefungen_skill_is_detected(self):
        self.assertTrue(keyword_match("When is Prüfungsanmeldung and Prüfungsabmeldung?", "WEB_PRUEFUNGEN"))

    def test_website_standort_skill_is_detected(self):
        self.assertTrue(keyword_match("Where can I find room plans and campus map?", "WEB_STANDORT"))

    def test_stuv_general_skill_is_detected(self):
        self.assertTrue(keyword_match("What is StuV and where is the Studierendenhaus?", "STUV_GENERAL"))

    def test_stuv_groups_skill_is_detected(self):
        self.assertTrue(keyword_match("Tell me about Hochschulgruppen and International Campus Friends", "STUV_GROUPS"))

    def test_stuv_fachschaften_skill_is_detected(self):
        self.assertTrue(keyword_match("What is FSIM and where can I find Altklausuren?", "STUV_FACHSCHAFTEN"))

    def test_stuv_campus_life_skill_is_detected(self):
        self.assertTrue(keyword_match("What is Nightline and Campusfest?", "STUV_CAMPUS_LIFE"))


class LanguageExpansionTests(unittest.TestCase):

    def test_ssp_expands_to_student_service_portal(self):
        expanded_input, words = expand_user_input_with_language_terms("What does SSP mean?")
        self.assertIn("student service portal", expanded_input)

    def test_transcript_triggers_abteilung_skill(self):
        self.assertTrue(keyword_match("Where can I get my transcript?", "WEB_ABTEILUNG"))

    def test_student_card_triggers_zulassung_skill(self):
        self.assertTrue(keyword_match("Where do I get my student card?", "WEB_ZULASSUNG"))

    def test_exchange_student_triggers_international_skill(self):
        self.assertTrue(keyword_match("I am an exchange student and need Erasmus information", "WEB_INTERNATIONAL"))

    def test_faculty_student_council_triggers_fachschaft_skill(self):
        self.assertTrue(keyword_match("What is the faculty student council for computer science?", "STUV_FACHSCHAFTEN"))


class ResourceTests(unittest.TestCase):

    def test_basic_info_file_can_be_read(self):
        text = read_basic_info()
        self.assertIn("Ostbayerische Technische Hochschule Regensburg", text)
        self.assertIn("Building K", text)

    def test_mensa_url_is_defined(self):
        self.assertTrue(data.MENSA_JSON_URL.startswith("https://"))
        self.assertIn("openmensa", data.MENSA_JSON_URL)

    def test_stundenplan_url_is_defined(self):
        self.assertTrue(data.STUNDENPLAN_JSON_URL.startswith("https://"))
        self.assertIn("timetable.json", data.STUNDENPLAN_JSON_URL)

    def test_website_pages_are_defined(self):
        self.assertGreater(len(data.WEBSITE_PAGES), 0)

        for page in data.WEBSITE_PAGES:
            self.assertIn("tag", page)
            self.assertIn("title", page)
            self.assertIn("url", page)
            self.assertTrue(page["url"].startswith("https://"))

    def test_stuv_pages_are_defined(self):
        self.assertGreater(len(data.STUV_PAGES), 0)

        for page in data.STUV_PAGES:
            self.assertIn("tag", page)
            self.assertIn("sources", page)

            for source in page["sources"]:
                self.assertIn("title", source)
                self.assertIn("url", source)
                self.assertTrue(source["url"].startswith("https://"))


class ChatStorageTests(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.original_chat_history_file = chat_storage.CHAT_HISTORY_FILE
        chat_storage.CHAT_HISTORY_FILE = Path(self.temp_directory.name) / "chat_history_test.json"
        chat_storage.CHAT_HISTORY_FILE.write_text("[]", encoding="utf-8")

    def tearDown(self):
        chat_storage.CHAT_HISTORY_FILE = self.original_chat_history_file
        self.temp_directory.cleanup()

    def test_empty_chat_history_returns_empty_list(self):
        self.assertEqual(chat_storage.load_chats(), [])

    def test_save_and_load_chat(self):
        messages = [
            {
                "role": "user",
                "content": "Hello"
            },
            {
                "role": "assistant",
                "content": "Hi"
            }
        ]

        chat_storage.save_chat(1, "Test chat", messages)

        loaded_chat = chat_storage.load_chat_by_id(1)

        self.assertIsNotNone(loaded_chat)
        self.assertEqual(loaded_chat["id"], 1)
        self.assertEqual(loaded_chat["title"], "Test chat")
        self.assertEqual(loaded_chat["messages"], messages)

    def test_load_chat_titles(self):
        chat_storage.save_chat(1, "First chat", [])
        chat_storage.save_chat(2, "Second chat", [])

        titles = chat_storage.load_chat_titles()

        self.assertEqual(titles, [
            {
                "id": 1,
                "title": "First chat"
            },
            {
                "id": 2,
                "title": "Second chat"
            }
        ])

    def test_get_next_chat_id(self):
        chat_storage.save_chat(1, "First chat", [])
        chat_storage.save_chat(2, "Second chat", [])

        self.assertEqual(chat_storage.get_next_chat_id(), 3)

    def test_delete_chat(self):
        chat_storage.save_chat(1, "Test chat", [])

        deleted = chat_storage.delete_chat(1)

        self.assertTrue(deleted)
        self.assertIsNone(chat_storage.load_chat_by_id(1))

    def test_delete_missing_chat_returns_false(self):
        deleted = chat_storage.delete_chat(999)

        self.assertFalse(deleted)


if __name__ == "__main__":
    unittest.main()