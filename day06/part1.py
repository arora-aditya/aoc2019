from collections import defaultdict


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
    
    def assign_children(self, moons):
        assert len(moons) <= 2, "Only 2 Moons per PLANET!"
        if len(moons) == 0:
            return 
        elif len(moons) == 1:
            self.left = moons[0]
        elif len(moons) == 2:
            self.left = moons[0]
            self.right = moons[1]


def prettyPrintTree(node, prefix="", isLeft=True):
    if not node:
        print("Empty Tree")
        return

    if node.right:
        prettyPrintTree(node.right, prefix + ("│   " if isLeft else "    "), False)

    print(prefix + ("└── " if isLeft else "┌── ") + str(node.val))

    if node.left:
        prettyPrintTree(node.left, prefix + ("    " if isLeft else "│   "), True)


with open('input.txt') as f:
    lines = f.readlines()
    L = list(map(lambda x: x.strip().split(')'), lines))

    di = defaultdict(set)
    for [planet, moon] in L:
        di[planet].add(moon)
    
    # counts = defaultdict(int)
    # for [planet, moon] in L:
    #     counts[planet] += 1
    #     counts[moon] -= 3
    # for planet in counts:
    #     if counts[planet] > 0:
    #         print(planet, counts[planet])
    
    planet_to_node = {}
    for planet in di:
        if planet not in planet_to_node:
            planet_to_node[planet] = TreeNode(planet)            
        for moon in di[planet]:
            if moon not in planet_to_node:
                planet_to_node[moon] = TreeNode(moon)
        moons = [planet_to_node[moon] for moon in di[planet]]
        planet_to_node[planet].assign_children(moons)

    ans, level = 0, [planet_to_node['COM']]
    counter = 0
    while level:
        temp = []
        for node in level:
            ans += counter
            temp.extend([node.left, node.right])
        level = [leaf for leaf in temp if leaf]
        counter += 1
        
        # print(ans, temp, level)
    print(ans)
# 322508 
        
