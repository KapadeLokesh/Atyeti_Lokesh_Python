class LogProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.readlines()
        except Exception as e:
            raise Exception(f"Error reading file: {e}")

    def process_data(self):
        lines = self.read_file()
        log_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
        for line in lines:
            if "INFO" in line:
                log_counts["INFO"] += 1
            elif "WARNING" in line:
                log_counts["WARNING"] += 1
            elif "ERROR" in line:
                log_counts["ERROR"] += 1
        return log_counts
