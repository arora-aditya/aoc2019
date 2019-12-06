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

# https://www.geeksforgeeks.org/find-distance-between-two-nodes-of-a-binary-tree/
def pathToNode(root, path, k): 
  
    # base case handling 
    if root is None: 
        return False
  
     # append the node value in path 
    path.append(root.val) 
   
    # See if the k is same as root's val 
    if root.val == k : 
        return True
   
    # Check if k is found in left or right  
    # sub-tree 
    if ((root.left != None and pathToNode(root.left, path, k)) or
            (root.right!= None and pathToNode(root.right, path, k))): 
        return True
   
    # If not present in subtree rooted with root,  
    # remove root from path and return False  
    path.pop() 
    return False
  
def distance(root, val1, val2): 
    if root: 
        # store path corresponding to node: val1 
        path1 = [] 
        pathToNode(root, path1, val1) 
  
        # store path corresponding to node: val2 
        path2 = [] 
        pathToNode(root, path2, val2) 
  
        # iterate through the paths to find the  
        # common path length 
        i=0
        while i<len(path1) and i<len(path2): 
            # get out as soon as the path differs  
            # or any path's length get exhausted 
            if path1[i] != path2[i]: 
                break
            i = i+1
  
        # get the path length by deducting the  
        # intersecting path length (or till LCA) 
        return (len(path1)+len(path2)-2*i) 
    else: 
        return 0


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
    print(distance(planet_to_node['COM'], 'SAN', 'YOU') - 2)

# 496
    
    