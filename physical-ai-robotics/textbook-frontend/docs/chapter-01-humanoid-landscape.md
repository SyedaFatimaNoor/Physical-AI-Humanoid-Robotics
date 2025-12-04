---
sidebar_position: 2
---

# Humanoid Robotics Landscape

## Overview
Humanoid robots are designed to resemble the human body. This allows them to operate in environments built for humans (stairs, doors, tools).

## Leading Platforms
| Robot | Company | Key Features |
|-------|---------|--------------|
| Optimus | Tesla | Mass manufacturing focus, VLA |
| Atlas | Boston Dynamics | Hydraulic (retired), Electric (new) |
| Figure 01 | Figure | OpenAI integration |
| Digit | Agility Robotics | Logistics focus |

## Challenges
- **Balance**: Bipedal locomotion is unstable.
- **Power**: Battery life is limited.
- **Cost**: Actuators and sensors are expensive.

## Lab: Analyze a URDF
We will look at a simple Humanoid URDF file.
```xml
<robot name="simple_humanoid">
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.1 0.5"/>
      </geometry>
    </visual>
  </link>
</robot>
```
