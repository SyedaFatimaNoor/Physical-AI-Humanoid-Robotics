---
sidebar_position: 3
---

# ROS 2 Fundamentals

## Nodes, Topics, Services
ROS 2 is the middleware for robotics.

### Nodes
A node is a process that performs computation.
```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Hello ROS 2!')
```

### Topics
Nodes communicate via topics (Pub/Sub).

### Services
Request/Response communication.

## Lab: Create a Publisher
Write a Python node that publishes "Hello World" every second.
