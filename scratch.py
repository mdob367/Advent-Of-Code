class Range4D:
    def __init__(self, a_range, b_range, c_range, d_range):
        self.a_range = a_range
        self.b_range = b_range
        self.c_range = c_range
        self.d_range = d_range

    def apply_rule(self, rule_range):
        # Intersect each range with the rule's range
        self.a_range = self.intersect_ranges(self.a_range, rule_range.a_range)
        self.b_range = self.intersect_ranges(self.b_range, rule_range.b_range)
        self.c_range = self.intersect_ranges(self.c_range, rule_range.c_range)
        self.d_range = self.intersect_ranges(self.d_range, rule_range.d_range)
        print('Size:', self.size())


    def size(self):
        # Return the size of the 4D space
        return (self.a_range[1] - self.a_range[0] + 1) * (self.b_range[1] - self.b_range[0] + 1) * (self.c_range[1] - self.c_range[0] + 1) * (self.d_range[1] - self.d_range[0] + 1)

    @staticmethod
    def intersect_ranges(range1, range2):
        # Find the intersection of two ranges
        return (max(range1[0], range2[0]), min(range1[1], range2[1]))

# Initialize the 4D space
space = Range4D((1, 4000), (1, 4000), (1, 4000), (1, 4000))

# Apply Rule 1
rule1 = Range4D((1, 100), (500, 1000), (1, 4000), (1, 4000))
space.apply_rule(rule1)

# Apply Rule 2
rule2 = Range4D((50, 500), (100, 200), (1000, 2000), (1, 10))
space.apply_rule(rule2)

# Apply Rule 2
rule2 = Range4D((1, 4000), (1, 4000), (1000, 2000), (1, 10))
space.apply_rule(rule2)

# Print the resulting ranges
print(f"Resulting Ranges: a={space.a_range}, b={space.b_range}, c={space.c_range}, d={space.d_range}")
