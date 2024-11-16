import json
import sys
from ortools.sat.python import cp_model


class Unit:
    def __init__(self, name, credits, available, type, prerequisites=None):
        self.name = name
        self.credits = credits
        self.available = available
        self.type = type
        self.prerequisites = prerequisites or []


class Scheduler:
    def __init__(self, units, prerequisites):
        self.units = units
        self.prerequisites = prerequisites
        self.model = cp_model.CpModel()
        self.unit_vars = {}
        self.setup_variables()
        self.add_constraints()

    def setup_variables(self):
        for unit in self.units.values():
            domain_values = []
            for term in unit.available:
                if term == 1:
                    domain_values.extend([1, 2, 3, 4, 9, 10, 11, 12])
                elif term == 2:
                    domain_values.extend([5, 6, 7, 8, 13, 14, 15, 16])
            self.unit_vars[unit.name] = self.model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain_values),
                                                                       unit.name)

    def add_constraints(self):
        self.add_prerequisite_constraints()
        self.add_no_repeating_units_constraint()
        self.add_credit_constraints()

    def add_prerequisite_constraints(self):
        for course, prereqs in self.prerequisites.items():
            for prereq in prereqs:
                self.model.Add(self.unit_vars[prereq] < self.unit_vars[course])

    def add_no_repeating_units_constraint(self):
        self.model.AddAllDifferent(self.unit_vars.values())

    def add_credit_constraints(self):
        periods = [(1, 4), (5, 8), (9, 12), (13, 16)]
        credit_limit_per_period = 12
        for start_period, end_period in periods:
            for period in range(start_period, end_period + 1):
                period_credits = []
                for course in self.units.values():
                    in_period_var = self.model.NewBoolVar(f'{course.name}in_period{period}')
                    period_credits.append(course.credits * in_period_var)
                    self.model.Add(self.unit_vars[course.name] == period).OnlyEnforceIf(in_period_var)
                    self.model.Add(self.unit_vars[course.name] != period).OnlyEnforceIf(in_period_var.Not())
                self.model.Add(sum(period_credits) <= credit_limit_per_period)

    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            semesters = {1: [], 2: [], 3: [], 4: []}
            for course_name, variable in self.unit_vars.items():
                value = solver.Value(variable)
                if 1 <= value <= 4:
                    semesters[1].append(course_name)
                elif 5 <= value <= 8:
                    semesters[2].append(course_name)
                elif 9 <= value <= 12:
                    semesters[3].append(course_name)
                elif 13 <= value <= 16:
                    semesters[4].append(course_name)
            return semesters
        else:
            return 'No solution found.'


def main(course_code):
    try:
        with open(f'{course_code}.json', 'r') as file:
            data = json.load(file)

        units_data = data['units']
        prerequisites_data = data['prerequisites']

        courses = {name: Unit(name, **props) for name, props in units_data.items()}
        scheduler = Scheduler(courses, prerequisites_data)
        schedule = scheduler.solve()

        if isinstance(schedule, str):
            print(schedule)
        else:
            for semester, units in schedule.items():
                print(f'Semester {semester}: {", ".join(units)}')

    except FileNotFoundError:
        print(f'No course plan found.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('<div style="color: black;">Usage: python app.py &lt;course_code&gt;</div>')
        sys.exit(1)
    course_code = sys.argv[1]
    main(course_code)
