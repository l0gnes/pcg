from typing import List, Union
from random import randint, choice

class Map(object):
    
    size : int # Maps are square so we will have the same size for length and height
    starting_node : "Node"
    visited_points : List[List[int]] = []
    index : int = 0

    @classmethod
    def generate(cls, size : int) -> "Map":

        m = cls()
        m.size = size # This is probably a horrible way of doing this

        n = Node.create_starting_node(
            map = m
        )

        m.starting_node = n

        m.starting_node.step()

        return m

    def register_node(self, node : "Node") -> None:
        self.visited_points.append(node.position)
        node.assign_value(self.index)

        self.index += 1

    def point_exceeds_map_boundaries(self, position : List[int]) -> bool:
        return (position[0] < 0 or position[0] >= self.size) or (position[1] < 0 or position[1] >= self.size)

class Node(object):

    is_dead : bool
    parent : "Node"
    value : int
    position : List[int]
    root_map : "Map"

    def __init__(self, parent : Union["Node", None], position : List[int], *, root_map : Union["Map", None] = None):
        self.root_map = root_map if isinstance(root_map, Map) else parent.root_map
        self.parent = parent
        self.position = position
        self.is_dead = False

    def assign_value(self, v : int) -> None:
        self.value = v

    @classmethod
    def create_starting_node(cls, map : "Map") -> "Node":
        n = cls(
            None,
            [
                randint(0, map.size),
                randint(0, map.size)
            ],
            root_map = map
        )

        map.register_node(n)

        return n


    @staticmethod
    def points_around_util(position : List[int]) -> List[List[int]]:
        t = []
        
        for x in range(0, 3, 2):
            t.append(
                [position[0] + (x-1), position[1]]
            )

        for y in range(0, 3, 2):
            t.append(
                [position[0], position[1] + (y-1)]
            )
        
        return t

    def free_space_check(self) -> List[List[int]]:
        return filter(
                lambda p: p not in self.root_map.visited_points and not self.root_map.point_exceeds_map_boundaries(p), 
                Node.points_around_util(self.position)
            )

    def step(self):

        if self.is_dead:
            self.parent.step()

        fsc = list(self.free_space_check())

        print(self.root_map.index)

        if len(fsc) > 0:

            next = Node(
                parent = self,
                position = choice(fsc)
            )

            self.root_map.register_node(next)

            next.step()

        else:
            self.is_dead = True

            if self.parent:
                self.parent.step()

            else:
                return

if __name__ == "__main__":
    new_map = Map.generate(5)
    print(new_map.index)
    