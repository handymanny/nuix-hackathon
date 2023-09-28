import os
from main.LLMClient import LLMClient
import logging

logging.basicConfig(level=logging.INFO, format='(%(threadName)-9s) %(message)s',)


class Summarizer:
    SUMMARY_PREFIXES = ["Sure! Here's a summary of the provided text in 100 words or less:", "Sure! Here is a summary of the provided text in 100 words or less:"]
    CONTEXT = 'Can you provide a comprehensive summary of the given text? The summary should cover all the key points and ' \
              'main ideas presented in the original text, while also condensing the information into a concise and ' \
              'easy-to-understand format. Please ensure that the summary includes relevant details and examples that ' \
              'support the main ideas, while avoiding any unnecessary information or repetition. The length of the ' \
              'summary should be no more than 100 words, providing a clear and accurate overview without omitting any ' \
              'important information.'

    def __init__(self, url, paths, summarized_path):
        super().__init__()
        self.file_paths = paths
        self.summaries = {}
        self.client = LLMClient(url)
        self.summarized_path = summarized_path
        logging.info("Starting Summarizing worker, for "+str(len(self.file_paths)) +" files")

    def get_text(self, file_path):
        data = None
        try:
            with open(file_path) as file:
                data = file.read()
        except Exception as e:
            logging.error('Cannot read file '+str(file_path) + ', ' +str(e))
            return None

        return data

    def can_summaraize(self, file_data):
        if file_data is None:
            return False

        if file_data.startswith('Attachment') and file_data.endswith('not found!'):
            return False

        return True

    def write_summary(self, file_name, summary):
        path = self.summarized_path + file_name
        try:
            f = open(path, "w")
            f.write(summary)
            f.close()
        except Exception as e:
            logging.error("Failed to write summary for file {file_name}, {e}")

    def generate_text_summary(self):
        for text_file_path in self.file_paths:
            file_name = os.path.basename(text_file_path)

            if os.path.exists(self.summarized_path+file_name):
                logging.info("Skipping summarization of "+str(file_name) +", file is already summarized")
                continue

            try:
                file_data = self.get_text(text_file_path)
                can_summarize = self.can_summaraize(file_data)

                if can_summarize:
                    logging.info("Summarizing "+str(file_name))
                    summary = self.client.generate_summary(self.CONTEXT, file_data)
                    summary = summary.replace(self.SUMMARY_PREFIXES[0], "")
                    summary = summary.replace(self.SUMMARY_PREFIXES[1], "")
                    summary = summary.replace("\n", "")

                    self.write_summary(file_name, summary)
                else:
                    logging.info("Skipping summarization of "+str(file_name)+", file is attachment")
            except Exception as e:
                logging.error("Failed to generate summary for "+str(text_file_path)+", " + str(e))

        return True
