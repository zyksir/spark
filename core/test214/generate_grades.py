import random
students2id = {"Liu":16001, "Guan":16002, "Zhang":16003, "Zhaoyun":16004, "Ma":16005, "Huang":16006, "Zhu":16007, "Li":16008}
courses_count = ["CS111", "CS118", "CS130", "CS145", "CS146"]
with open("grades.csv", "w") as fw:
    fw.write("Name,Id,Class,Grade\n")
    for student, sid in students2id.items():
        for course in courses_count:
            grade = random.randint(80, 100)
            fw.write("%s,%d,%s,%d\n" % (student, sid, course, grade))

