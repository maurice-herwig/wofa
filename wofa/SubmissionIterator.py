from wofa import get_submission


class SubmissionIterator:
    """
    Iterator to iterate over all submission for a given task.
    """

    def __init__(self, task: str):
        self.task = task

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            while True:
                self.index += 1
                return get_submission(self.task, str(self.index))

        except FileNotFoundError:
            raise StopIteration
        except Exception as _:
            return None
