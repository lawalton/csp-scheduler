from collections import OrderedDict
class CSP:
    # your code here#
    def __init__(self, courses, rooms, domain):
        self.domain = domain
        self.courses = courses
        self.rooms = rooms
        self.num_backtrack = 0

"""
considerations for the final exam scheduler:
- day - provide monday-friday list of variables
- time - 8am - 7pm?
    - pick a length of time to assume all finals - 1 hour? 2 hours?
- room size 
- can't have classes at the different times have finals at the same time
"""

"""
list/dictionary of rooms
room name - occupancy
{"ECEE 156": 130, "MATH 100": 200}

list of classes: info needed:
    name, time, number of students
"""

"""
domain - date/time combos
["M", 9], ["M", 10], etc. 
"""

def backtracking_search(csp):
    return recursive_backtracking(OrderedDict(), csp)

def check_constraints(course, final_assignment, csp, assignment):
    # check room size
    room_name = final_assignment[2]
    room_occupancy = csp.rooms[room_name]
    num_students = csp.courses[course][2]

    # check if that room and time is already reserved
    for course_assigned in assignment:
        # that slot and room has already been taken
        if final_assignment == assignment[course_assigned]:
            return False

    if room_occupancy < num_students:
        return False
                
    # check for time conflicts

    return True
    
def find_next_node(csp, assignment):
    for course in csp.courses:
        if course not in assignment:
            return course
    return False
    
def recursive_backtracking(assignment, csp):
    # Your code here #

    if len(assignment) == len(csp.courses):
        return assignment

    course = find_next_node(csp, assignment)

    for final_date in csp.domain:
        if check_constraints(course, final_date, csp, assignment):
            assignment[course] = final_date
            # get next state
            result = recursive_backtracking(assignment, csp)
            if result:
                return result
            else:
                del assignment[course]
    return False

# create the possible domains for monday - friday, 8am - 5pm, two hour block
days = ["M", "T", "W", "R", "F"]
times = [8, 10, 12, 2, 4]
rooms = {"ECEE 156": 130, "MATH 100": 300, "CHEM 140": 400, "HLMS 70": 150}
domain = []
for day in days:
    for time in times:
        for room in rooms:
            domain.append([day, time, room])

# for now, assuming classes are mwf, and tr
# m designates mwf and t designates t/r
courses = OrderedDict([
    ("CSCI 1300", ["M", 1, 300]),
    ("CSCI 2270", ["T", 12, 350]),
    ("CSCI 3202", ["M", 4, 70]), 
    ("APPM 1400", ["M", 1, 130]),
    ("APPM 1300", ["T", 2, 200])
 ])

csp = CSP(courses, rooms, domain)
a = backtracking_search(csp)
print("=================")
print(a)