import re

class Tester(object):
    """
    TS tester.
    """

    def __init__(self, ts):
        self._ts = ts
        self._test_cases = []

    def add_test_case(self, input_tape, output_tape):
        """
        Adds test case.
        input_tape - input tape
        output_tape - output tape (regular expression)
        """
        self._test_cases.append([input_tape, output_tape])

    def run_test(self):
        """
        Runs all tests and prints results.
        """
        verbose = self._ts.verbose
        self._ts.verbose = False
        counter = 0
        ok_counter = 0
        for case in self._test_cases:
            self._ts.test(case[0])
            if re.match(case[1], self._ts.tape):
                ok_counter += 1
            else:
                print "Error for input: ", case[0]
                print "Expected: ", case[1]
                print "Your result: ", self._ts.tape, "\n"
            counter += 1
        self._ts.verbose = verbose
        print "Result: ", ok_counter, "/", counter, " OK      :( NOT BAD"
