class CourseClass:
    # ID counter used to assign IDs automatically
    _next_class_id = 0
    
    def __init__(self, professor, course, requires_lab, duration, groups):
        self.Id = CourseClass._next_class_id
        CourseClass._next_class_id += 1
        self.Professor = professor
        self.Course = course
        self.NumberOfSeats = 0
        self.LabRequired = requires_lab
        self.Duration = duration
        self.Groups = set(groups)

        self.Professor.addCourseClass(self)

        for grp in self.Groups:  # self.groups:
            grp.addClass(self)
            self.NumberOfSeats += grp.NumberOfStudents

    # Returns TRUE if another class has one or overlapping student groups.
    def groupsOverlap(self, c):
        return len(self.Groups & c.Groups) > 0

    # Returns TRUE if another class has same professor.
    def professorOverlaps(self, c):
        return self.Professor == c.Professor

    def __hash__(self):
        return hash(self.Id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (self == other)

    # Restarts ID assigments
    @staticmethod
    def restartIDs() -> None:
        CourseClass._next_class_id = 0
