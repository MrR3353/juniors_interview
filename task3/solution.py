def appearance(intervals: dict[str, list[int]]) -> int:

    def merge_intervals(timestamps: list[int]):
        """Merge overlapping intervals."""
        intervals = sorted([[timestamps[i], timestamps[i + 1]] for i in range(0, len(timestamps), 2)])

        i = 1
        while i < len(intervals):
            if intervals[i - 1][0] <= intervals[i][0] <= intervals[i - 1][1]:
                if intervals[i][1] > intervals[i - 1][1]:
                    intervals[i - 1][1] = intervals[i][1]
                intervals.pop(i)
                continue
            i += 1
        timestamps = [timestamp for interval in intervals for timestamp in interval]
        return timestamps

    pupil = merge_intervals(intervals['pupil'])
    pupil = list(zip(pupil, 'P' * len(pupil)))
    tutor = merge_intervals(intervals['tutor'])
    tutor = list(zip(tutor, 'T' * len(tutor)))

    start_lesson, end_lesson = intervals['lesson']
    total_time = 0
    timestamps = sorted(pupil + tutor)
    pupil_online = tutor_online = False
    for i in range(len(timestamps)):
        timestamp, person = timestamps[i]
        if pupil_online and tutor_online:
            start = timestamps[i - 1][0]
            end = timestamp
            if start < start_lesson:
                start = start_lesson
            if end > end_lesson:
                end = end_lesson
                if end > start:
                    total_time += (end - start)
                break
            if end > start:
                total_time += (end - start)
        if person == 'P':
            pupil_online = not pupil_online
        if person == 'T':
            tutor_online = not tutor_online
    return total_time


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'