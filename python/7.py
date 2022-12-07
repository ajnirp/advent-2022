with open('7.txt', 'r') as f:
    data = [line.strip() for line in f.readlines()]

# Object representing a file or directory in the filesystem
class Node:
    def __init__(self, path, size=0):
        self.path = path
        self.size = size
        self.children = []
        self.parent = None

    def name(self):
        if self.path == '':
            return '/'
        return self.path.split('/')[-1]

# Object that holds state as we move around inside the filesystem
class Config:
    CUTOFF = 100_000
    ROOT_NAME = '/'
    TOTAL_SPACE = 70_000_000
    UNUSED_REQUIRED = 30_000_000

    def __init__(self):
        # Root node '/''
        self.root = Node(Config.ROOT_NAME)

        # Map of paths to Nodes
        self.nodes = {Config.ROOT_NAME: self.root}

        # Current working directory
        self.cwd = [Config.ROOT_NAME]

        # Set of directories with size under CUTOFF. Updated as soon as new data
        # is available rather than on-demand
        self.smol_dirs = set([self.root])

    def is_root_path(self, path):
        return path == ''

    # Return the current working dir's absolute path
    # For the root this is the empty string
    def get_cwd_path(self):
        return '/'.join(self.cwd[1:])

    # Return a file's absolute path
    def get_path(self, name):
        if len(self.cwd) == 1:
            return name
        return self.get_cwd_path() + '/' + name

    # Change current working directory to root
    def cd_root(self):
        self.cwd = [Config.ROOT_NAME]

    # Change current working directory
    def cd(self, target_dir):
        if target_dir == '/':
            self.cd_root()
        elif target_dir == '..' and len(self.cwd) > 0:
            self.cwd.pop()
        else:
            self.cwd.append(target_dir)

    # Create a Node, insert it into the map and return it
    def insert_node(self, path, size=0):
        node = Node(path, size)
        self.nodes[path] = node
        return node

    # Lookup a Node from the map
    def get_node(self, path):
        if self.is_root_path(path):
            return self.get_node(Config.ROOT_NAME)
        return self.nodes[path]

    def maybe_create_dir(self, name):
        path = self.get_path(name)
        if path not in self.nodes:
            self.create_dir(path)

    def create_dir(self, path):
        node = self.insert_node(path)
        parent = self.get_node(self.get_cwd_path())
        parent.children.append(node)
        node.parent = parent
        self.smol_dirs.add(node)

    def maybe_create_file(self, name, size):
        path = self.get_path(name)
        if path not in self.nodes:
            self.create_file(path, size)

    def create_file(self, path, size):
        node = self.insert_node(path, size)
        parent = self.get_node(self.get_cwd_path())
        parent.children.append(node)
        node.parent = parent

        parent.size += size
        if parent.size > Config.CUTOFF and parent in self.smol_dirs:
            self.smol_dirs.remove(parent)

        curr_node = parent.parent
        while curr_node:
            curr_node.size += node.size
            if curr_node.size > Config.CUTOFF and curr_node in self.smol_dirs:
                self.smol_dirs.remove(curr_node)
            curr_node = curr_node.parent

# Process file input
def process_data(data, config):
    for line in data:
        if line[0] == '$':
            instruction = line.split()[1]
            if instruction == 'cd':
                target_dir = line.split()[-1]
                config.cd(target_dir)
        elif line[:3] == 'dir':
            name = line.split()[1]
            config.maybe_create_dir(name)
        elif line[0] in '0123456789':
            size, name = line.split()
            size = int(size)
            config.maybe_create_file(name, size)

# Calculate how much space we need to free up
def extra_space_needed(root):
    return Config.UNUSED_REQUIRED + root.size - Config.TOTAL_SPACE

def size_of_smallest_dir_to_delete(root):
    def preorder_traversal(node, result_array):
        result_array.append(node)
        for child in node.children:
            preorder_traversal(child, result_array)
    traversal = []
    preorder_traversal(root, traversal)

    space_needed = extra_space_needed(root)
    min_so_far = root.size
    for node in traversal:
        if len(node.children) == 0:
            continue
        if node.size > space_needed and node.size < min_so_far:
            min_so_far = node.size
    return min_so_far

config = Config()
process_data(data, config)
print(sum(d.size for d in config.smol_dirs))
print(size_of_smallest_dir_to_delete(config.root))
