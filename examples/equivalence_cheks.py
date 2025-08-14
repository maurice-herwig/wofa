from wofa import SubmissionIterator, get_solution, FiniteAutomata
from collections import defaultdict

CORRECT = "correct"
INCORRECT = 'incorrect'
NOT_PARSEABLE = 'not_parseable'
ALL = 'all'
TASKS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']


def equivalence_check(tasks: list):
    """
    Check for each task in the given tasks list. How much of the submission are language equivalent to the solution and
    print the number to the console.

    Args:
        tasks: A list of Tasks for that we perform the check.

    Returns: None
    """

    # Create a result dict.
    res = {}

    # Iterate over all given tasks
    for task in tasks:

        # Get a solution for the current tasks and set the alphabet
        solution = get_solution(exercise=task)
        FiniteAutomata.set_alphabet(solution.calc_and_get_alphabet())

        # Crate an iterator object and a result dict for this tasks
        iterator = SubmissionIterator(task=task)
        task_res = defaultdict(int)

        # Iterate over all submission for the current tasks a check if the submission equivalent to the solution
        for sub in iterator:

            if sub:
                if solution.equivalence_test(other=sub):
                    task_res[CORRECT] += 1
                else:
                    task_res[INCORRECT] += 1
            else:
                task_res[NOT_PARSEABLE] += 1

        task_res[ALL] = task_res[INCORRECT] + task_res[CORRECT] + task_res[NOT_PARSEABLE]
        res[task] = task_res

        # Print the results
        print(f'---------{task}------------')
        print(f'{CORRECT}: {task_res[CORRECT]}     percentage: {task_res[CORRECT] / task_res[ALL]}')
        print(f'{INCORRECT}: {task_res[INCORRECT]}     percentage: {task_res[INCORRECT] / task_res[ALL]}')
        print(f'{NOT_PARSEABLE}: {task_res[NOT_PARSEABLE]}     percentage: {task_res[NOT_PARSEABLE] / task_res[ALL]}')
        print(f'Number of submissions {task_res[ALL]}')
        print()

    # Compute the results over all given tasks.
    all_tasks = defaultdict(int)
    for task in TASKS:
        all_tasks[CORRECT] += res[task][CORRECT]
        all_tasks[INCORRECT] += res[task][INCORRECT]
        all_tasks[NOT_PARSEABLE] += res[task][NOT_PARSEABLE]
        all_tasks[ALL] += res[task][ALL]

    # Print the results
    print(f'------------------ ALL TASKS --------------')
    print(f'{CORRECT}: {all_tasks[CORRECT]}     percentage: {all_tasks[CORRECT] / all_tasks[ALL]}')
    print(f'{INCORRECT}: {all_tasks[INCORRECT]}     percentage: {all_tasks[INCORRECT] / all_tasks[ALL]}')
    print(f'{NOT_PARSEABLE}: {all_tasks[NOT_PARSEABLE]}     percentage: {all_tasks[NOT_PARSEABLE] / all_tasks[ALL]}')
    print(f'Number of submissions {all_tasks[ALL]}')
    print()


if __name__ == "__main__":
    equivalence_check(tasks=TASKS)
