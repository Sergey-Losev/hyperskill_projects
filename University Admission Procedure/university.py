from statistics import mean


def stage_1_of_7():
    value1, value2, value3 = float(input()), float(input()), float(input())
    print(mean([value1, value2, value3]))
    print('Congratulations, you are accepted!')


def stage_2_of_7():
    score = [float(input()) for _ in range(3)]
    print(mean(score))
    if mean(score) >= 60:
        print('Congratulations, you are accepted!')
    else:
        print('We regret to inform you that we will not be able to offer you admission.')


def stage_3_of_7():
    number_of_applicants = int(input())
    to_be_accept = int(input())
    list_of_students = [input().split() for _ in range(number_of_applicants)]
    sorted_list = sorted(list_of_students, key=lambda x: (-float(x[2]), x[0], x[1]))
    print('Successful applicants:')
    for i in range(to_be_accept):
        print(sorted_list[i][0], sorted_list[i][1])


def stage_4_of_7():
    departments_dict = {"Biotech": [], "Chemistry": [], "Engineering": [], "Mathematics": [], "Physics": []}

    count_students = int(input())
    with open("applicant_list.txt", "r") as file:
        info_students = [students.split() for students in file]
    for departments in range(3, 6):
        info_students.sort(key=lambda students: (students[departments], -float(students[2]), students[0], students[1]))
        for students in info_students[:]:
            current_departments = departments_dict[students[departments]]
            if count_students > len(current_departments):
                current_departments.append([students[0], students[1], str(float(students[2]))])
                info_students.remove(students)
    for department in departments_dict:
        print(department)
        departments_dict[department].sort(key=lambda students: (-float(students[2]), students[0], students[1]))
        [print(*student, end="\n") for student in departments_dict[department]]


def stage_5_of_7():
    departments_dict = {"Biotech": [], "Chemistry": [], "Engineering": [], "Mathematics": [], "Physics": []}
    gpa_current = {"Biotech": 3, "Chemistry": 3, "Engineering": 5, "Mathematics": 4, "Physics": 2}
    count_students = int(input())
    with open("applicant_list_5.txt", "r") as file:
        info_students = [students.split() for students in file]
    for departments in range(6, 9):
        info_students.sort(
            key=lambda students: (students[departments], -float(students[gpa_current[students[departments]]]),
                                  students[0], students[1]))
        for students in info_students[:]:
            current_departments = departments_dict[students[departments]]
            if count_students > len(current_departments):
                current_departments.append(
                    [students[0], students[1], float(students[gpa_current[students[departments]]])])
                info_students.remove(students)
    for department in departments_dict:
        print(department)
        departments_dict[department].sort(key=lambda students: (-float(students[2]), students[0], students[1]))
        [print(*student, end="\n") for student in departments_dict[department]]


def stage_6_of_7():
    departments = {'Biotech': [], 'Chemistry': [], 'Engineering': [], 'Mathematics': [], 'Physics': []}
    # related exams fields indexes in input file
    exam = {'Biotech': (2, 3), 'Chemistry': (3, 3), 'Engineering': (4, 5), 'Mathematics': (4, 4), 'Physics': (2, 4)}

    max_accepted = int(input())
    with open('applicant_list_5.txt') as f:
        applicants = [line.split() for line in f]

    for i in range(6, 9):  # priority fields in input file
        for dep in departments.keys():
            applicants_sorted = sorted(applicants,
                                       key=lambda x: (-(int(x[exam[dep][0]]) + int(x[exam[dep][1]])), x[0], x[1]))
            for applicant in applicants_sorted:
                if applicant[i] == dep and len(departments[dep]) < max_accepted:
                    score = (int(applicant[exam[dep][0]]) + int(applicant[exam[dep][1]])) / 2
                    departments[dep].append([applicant[0], applicant[1], score])
                    applicants.remove(applicant)

    for dep in departments.keys():
        with open(f'{dep.lower()}.txt', 'w', encoding='utf-8') as f:
            for student in sorted(departments[dep], key=lambda x: (-x[2], x[0], x[1])):
                print(*student, file=f)


def stage_7_of_7():
    departments = {'Biotech': [], 'Chemistry': [], 'Engineering': [], 'Mathematics': [], 'Physics': []}
    # related exams fields indexes in input file
    exam = {'Biotech': (2, 3, 6), 'Chemistry': (3, 3, 6), 'Engineering': (4, 5, 6), 'Mathematics': (4, 4, 6),
            'Physics': (2, 4, 6)}
    max_accepted = int(input())
    with open('applicant_list_7.txt') as f:
        applicants = [line.split() for line in f]

    for i in range(7, 10):  # priority fields in input file
        for dep in departments.keys():
            applicants_sorted = sorted(applicants,
                                       key=lambda x: (-max(((int(x[exam[dep][0]]) + int(x[exam[dep][1]])) / 2),
                                                           int(x[exam[dep][2]])), x[0], x[1]))
            for applicant in applicants_sorted:
                if applicant[i] == dep and len(departments[dep]) < max_accepted:
                    if (int(applicant[exam[dep][0]]) + int(applicant[exam[dep][1]])) / 2 > int(applicant[exam[dep][2]]):
                        score = (int(applicant[exam[dep][0]]) + int(applicant[exam[dep][1]])) / 2
                    else:
                        score = int(applicant[exam[dep][2]])
                    departments[dep].append([applicant[0], applicant[1], score])
                    applicants.remove(applicant)

    for dep in departments.keys():
        with open(f'{dep.lower()}.txt', 'w', encoding='utf-8') as f:
            for student in sorted(departments[dep], key=lambda x: (-x[2], x[0], x[1])):
                print(*student, file=f)


if __name__ == "_main__":
  stage_7_of_7()
