# Physical AI & Humanoid Robotics - Textbook Specification

## Project Overview
A comprehensive, interactive textbook for teaching Physical AI and Humanoid Robotics, featuring a RAG chatbot, personalization, and multilingual support.

## Course Outline

### Module 1: Foundations
1. **Physical AI foundations**: Embodied intelligence, sensors, actuators.
2. **ROS 2 (3 weeks)**: Nodes, topics, services, actions, rclpy, launch files.
3. **Gazebo simulation**: Worlds, models, plugins, physics engines.
4. **Unity visualization**: URDF import, ROS-TCP connector, high-fidelity rendering.
5. **NVIDIA Isaac Sim & Isaac ROS**: Photorealistic sim, GEMs, replicator.

### Module 2: Advanced Control & Learning
6. **Reinforcement learning for robots**: OpenAI Gym, stable-baselines3, reward shaping.
7. **Humanoid kinematics & locomotion**: FK/IK, gait generation, ZMP, inverted pendulum.
8. **Manipulation**: Grasping, motion planning (MoveIt), pick and place.
9. **VLA (Vision Language Action)**: RT-1, RT-2, multimodal transformers.

### Module 3: Interaction & Integration
10. **Conversational robotics with GPT models**: LLM integration, prompt engineering, voice I/O.
11. **Capstone: Autonomous Humanoid Robot**: Full system integration, nav + manipulation + chat.

## Agent Commands (Claude Code)

### Generate Chapter
```bash
/run-skill Chapter Writer --topic "ROS 2 Fundamentals" --slug "ros2-fundamentals" --level "Intermediate"
```

### Generate Lab
```bash
/run-skill Lab Generator --topic "Gazebo World Creation" --tools ["Gazebo", "URDF"]
```

### Robot Mentor
```bash
/run-skill Robot Mentor Agent --task "Generate a URDF for a 2-DOF arm" --context "Use simple cylinders and revolute joints"
```

## Architecture
- **Frontend**: Docusaurus + React + TypeScript
- **Backend**: FastAPI + Python
- **Database**: Qdrant (Vector), Postgres (User Data)
- **AI**: Gemini 1.5 Flash
