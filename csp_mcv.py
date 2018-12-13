from collections import OrderedDict
class CSP:
    # your code here#
    def __init__(self, courses, rooms, domain):
        self.domain = domain
        self.courses = courses
        self.rooms = rooms
        self.num_backtrack = 0
        self.cost = 0

def backtracking_search(csp):
    return recursive_backtracking(OrderedDict(), csp)

def check_constraints(course, final_assignment, csp, assignment):
    # check room size
    room_name = final_assignment[2]
    room_occupancy = csp.rooms[room_name]
    num_students = csp.courses[course][2]

    if room_occupancy < num_students:
        return False

    course_day = csp.courses[course][0]
    course_time = csp.courses[course][1]
    final_assignment_day = final_assignment[0]
    final_assignment_time = final_assignment[1]

    # check if that room and time is already reserved
    for course_assigned in assignment:
        # that slot and room has already been taken
        if final_assignment == assignment[course_assigned]:
            return False

        # check for time conflicts
        assigned_course_day = csp.courses[course_assigned][0]
        assigned_course_time = csp.courses[course_assigned][1]
        assigned_final_day = assignment[course_assigned][0]
        assigned_final_time = assignment[course_assigned][1]

        if (final_assignment_day ==  assigned_final_day) and (final_assignment_time == assigned_final_time):
            # two finals were scheduled at the same time
            # this can only happen if the regular class periods are at the same time
            if ((course_day !=  assigned_course_day) or (course_time != assigned_course_time)):
                return False
        
    return True
    
def find_next_node(csp, assignment):
    for course in csp.courses:
        if course not in assignment:
            return course
    return False

def select_most_constraining_variable(csp, assignment):
    # select the course that has the largest number of students
    # the more students, the fewer room options
    largest_course = None
    max_num_students = float("-inf")
    for course in csp.courses:
        num_students = csp.courses[course][2]
        if (course not in assignment) and (num_students > max_num_students):
            largest_course = course
            max_num_students = num_students

    return largest_course
           
def recursive_backtracking(assignment, csp):

    if len(assignment) == len(csp.courses):
        return assignment

    course = select_most_constraining_variable(csp, assignment)

    for final_date in csp.domain:
        csp.cost = csp.cost + 1
        if check_constraints(course, final_date, csp, assignment):
            print("Assigned ", course, "to", final_date)
            assignment[course] = final_date
            # get next state
            result = recursive_backtracking(assignment, csp)
            if result:
                return result
            else:
                del assignment[course]
                csp.num_backtrack = csp.num_backtrack + 1
    return False

# create the possible domains for monday - friday, 8am - 5pm, two hour block
#days = ["M", "T", "W", "R", "F"]
days = ["M"]
#times = [8, 10, 12, 2, 4]
times = [8, 10, 12]
rooms = {"CHEM 140": 400, "ECEE 156": 130, "MATH 100": 250}
domain = []
for day in days:
    for time in times:
        for room in rooms:
            domain.append([day, time, room])

# for now, assuming classes are mwf, and tr
# m designates mwf and t designates t/r
courses = OrderedDict([
    ("CSCI 3202", ["M", 4, 70]), 
    ("PHYS 1000", ["M", 4, 360]),
    ("CSCI 1300", ["M", 1, 170]),
    ("CSCI 2270", ["T", 12, 350]),
    ("APPM 1400", ["M", 1, 130]),
    ("APPM 1300", ["T", 12, 200])
 ])

courses_desc = OrderedDict([
    ("PHYS 1000", ["M", 4, 360]),
    ("CSCI 2270", ["T", 12, 350]),
    ("APPM 1300", ["T", 12, 200]),
    ("CSCI 1300", ["M", 1, 170]),
    ("APPM 1400", ["M", 1, 130]),
    ("CSCI 3202", ["M", 4, 70])

 ])

courses_asc = OrderedDict([
    ("CSCI 3202", ["M", 4, 70]), 
    ("APPM 1400", ["M", 1, 130]),
    ("CSCI 1300", ["M", 1, 170]),
    ("APPM 1300", ["T", 12, 200]),
    ("CSCI 2270", ["T", 12, 350]),
    ("PHYS 1000", ["M", 4, 360])
   ])

#csp = CSP(courses, rooms, domain)
#csp = CSP(courses_desc, rooms, domain)
csp = CSP(courses_asc, rooms, domain)
a = backtracking_search(csp)
print("=================")
print(a)
print(csp.num_backtrack)
print(csp.cost)

