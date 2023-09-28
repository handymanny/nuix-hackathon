import glob
import logging
import concurrent.futures
from main.Summarizer import Summarizer

logging.basicConfig(level=logging.INFO, format='%(message)s',)

URI = ''

# Text directories
TEXT_DIR = 'C:/Users/ecunningham01/OneDrive - Nuix.com/Desktop/Chat to Code Base/Text/'
SUMMARIZED_DIR = 'C:/Users/ecunningham01/OneDrive - Nuix.com/Desktop/Chat to Code Base/Summarized/'


# Chunk text files into equal sized arrays
def chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


if __name__ == '__main__':
    text_files = glob.glob(TEXT_DIR + '*.txt')
    logging.info("Total files to summarize" + str(len(text_files)))

    # Split text files into 100 item chunks
    chunks = chunk(text_files, 100)

    # Create tasks for all the documents
    tasks = []
    for cnk in chunks:
        tasks.append(Summarizer(URI, cnk, SUMMARIZED_DIR))

    logging.info("Created " + str(len(tasks)) +" jobs")

    # Create thread pool executor to handle all of the files
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_task = {executor.submit(task.generate_text_summary): task for task in tasks}

        for future in concurrent.futures.as_completed(future_to_task):
            try:
                data = future.result()
            except Exception as exc:
                logging.error("Failed to generate summary for files, "+str(exc))
            else:
                logging.info("Successfully summarized batch of 100 documents")






