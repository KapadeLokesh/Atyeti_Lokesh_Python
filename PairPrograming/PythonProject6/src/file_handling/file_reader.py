import os
import zipfile
import datetime
import json
import time

class LogProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def process_files(self):
        log_summaries = []

        try:
            for filename in os.listdir(self.file_path):
                full_path = os.path.join(self.file_path, filename)

                if filename.endswith('.txt') or filename.endswith('.log'):
                    result = self.process_txt_file(full_path)
                    if result:
                        log_summaries.append(result)

                elif filename.endswith('.zip'):
                    extracted_txts = self.extract_zip(full_path)
                    for txt_file in extracted_txts:
                        result = self.process_txt_file(txt_file)
                        if result:
                            log_summaries.append(result)

        except FileNotFoundError as e:
            print(e)

        return log_summaries


    def is_valid_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False

    def extract_zip(self, zip_path):
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extract_dir = os.path.splitext(zip_path)[0]
            zip_ref.extractall(extract_dir)

            for root, _, files in os.walk(extract_dir):
                for f in files:
                    file_full_path = os.path.join(root, f)
                    if not f.endswith('.txt'):
                        print(f"Invalid File {f}, We are expecting only .txt files to process.")
                        continue
                    extracted_files.append(file_full_path)

        return extracted_files

    def process_txt_file(self, file_path):

        file_name = os.path.basename(file_path)
        log_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
        log_messages = {"INFO": [], "WARNING": [], "ERROR": []}

        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        if not lines:
            print(f"Empty file: {file_name}")
            return None

        header = lines[0].split(",")
        if len(header) != 2 or not self.is_valid_date(header[1]):
            print(f"Invalid header in file: {file_name}")
            return None

        try:
            expected_count = int(lines[-1])
        except ValueError:
            print(f"Invalid footer in file: {file_name}")
            return None

        content_lines = lines[1:-1]
        if expected_count != len(content_lines):
            print(f"Line count mismatch in file: {file_name}. Expected {expected_count}, Found {len(content_lines)}.")
            return None

        for line in content_lines:
            if "INFO" in line:
                log_counts["INFO"] += 1
                log_messages["INFO"].append(line)
            elif "WARNING" in line:
                log_counts["WARNING"] += 1
                log_messages["WARNING"].append(line)
            elif "ERROR" in line:
                log_counts["ERROR"] += 1
                log_messages["ERROR"].append(line)

        self.save_json_summary(log_counts, log_messages, os.path.basename(file_path))

        return log_counts, os.path.basename(file_path)

    def save_json_summary(self, log_counts, messages, log_file):
        output_dir = r"C:\Users\LokeshKapde\Documents\New folder\Python Tasks Repo\Python Practice\PairPrograming\PythonProject6\resources\output"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d%H%M%S")
        output_path = os.path.join(output_dir, f"{timestamp}_{log_file}.json")

        data = {
            "file_name": log_file,
            "date_of_creation": timestamp,
            "log_levels": {
                "info": {
                    "messages": messages.get("INFO", []),
                    "count": log_counts.get("INFO", 0)
                },
                "error": {
                    "messages": messages.get("ERROR", []),
                    "count": log_counts.get("ERROR", 0)
                },
                "warning": {
                    "messages": messages.get("WARNING", []),
                    "count": log_counts.get("WARNING", 0)
                }
            }
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"JSON summary saved to {log_file}")



