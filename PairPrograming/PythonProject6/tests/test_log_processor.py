import unittest
import tempfile
import os
import zipfile
from src.file_handling.file_reader import LogProcessor

class TestLogProcessor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.processor = LogProcessor(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def create_txt_file(self, filename, lines):
        file_path = os.path.join(self.test_dir.name, filename)
        with open(file_path, 'w') as f:
            f.write("\n".join(lines))
        return file_path

    def test_valid_txt_file(self):
        lines = [
            "HEADER,20250101",
            "INFO Starting application",
            "WARNING Low memory",
            "ERROR Failed to connect",
            "3"
        ]
        self.create_txt_file("valid.log", lines)
        summaries = self.processor.process_files()
        self.assertEqual(len(summaries), 1)
        counts, filename = summaries[0]
        self.assertEqual(counts['INFO'], 1)
        self.assertEqual(counts['WARNING'], 1)
        self.assertEqual(counts['ERROR'], 1)

    def test_invalid_header(self):
        lines = [
            "BADHEADER,xxx",
            "INFO test",
            "1"
        ]
        self.create_txt_file("bad_header.txt", lines)
        summaries = self.processor.process_files()
        self.assertEqual(summaries, [])

    def test_invalid_footer(self):
        lines = [
            "HEADER,20250101",
            "INFO test",
            "not_a_number"
        ]
        self.create_txt_file("bad_footer.txt", lines)
        summaries = self.processor.process_files()
        self.assertEqual(summaries, [])

    def test_empty_file(self):
        self.create_txt_file("empty.log", [])
        summaries = self.processor.process_files()
        self.assertEqual(summaries, [])

    def test_zip_with_valid_txt(self):
        txt_lines = [
            "HEADER,20250101",
            "INFO ok",
            "1"
        ]
        txt_path = os.path.join(self.test_dir.name, "inside.txt")
        with open(txt_path, "w") as f:
            f.write("\n".join(txt_lines))

        zip_path = os.path.join(self.test_dir.name, "logs.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(txt_path, arcname="inside.txt")

        os.remove(txt_path)  

        summaries = self.processor.process_files()
        self.assertEqual(len(summaries), 1)
        counts, _ = summaries[0]
        self.assertEqual(counts['INFO'], 1)

    def test_zip_with_non_txt(self):
        bad_file = os.path.join(self.test_dir.name, "not_txt.csv")
        with open(bad_file, "w") as f:
            f.write("HEADER,20250101\nINFO test\n1")

        zip_path = os.path.join(self.test_dir.name, "badlogs.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(bad_file, arcname="not_txt.csv")

        os.remove(bad_file)

        summaries = self.processor.process_files()
        self.assertEqual(summaries, [])

    def test_nonexistent_directory(self):
        processor = LogProcessor("non_existent_dir")
        summaries = processor.process_files()
        self.assertEqual(summaries, [])  

if __name__ == '__main__':
    unittest.main()


