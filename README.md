# Physical AI & Humanoid Robotics - Interactive Textbook

[![Deploy to GitHub Pages](https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics/actions/workflows/deploy.yml/badge.svg)](https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics/actions/workflows/deploy.yml)

> **A comprehensive, AI-powered textbook for learning Physical AI and Humanoid Robotics with integrated RAG chatbot, personalization, and multilingual support.**

🌐 **Live Demo**: [https://syedafatimanoor.github.io/Physical-AI-Humanoid-Robotics/](https://syedafatimanoor.github.io/Physical-AI-Humanoid-Robotics/)

## 📚 About This Project

This project is a submission for the **Panaversity Physical AI & Humanoid Robotics Hackathon**. It combines cutting-edge educational content with AI-powered features to create an interactive learning experience.

### ✨ Features

- **📖 Comprehensive Textbook**: 11 detailed chapters covering Physical AI fundamentals to advanced humanoid robotics
- **🤖 RAG Chatbot**: AI assistant powered by Gemini API and Qdrant vector database
- **🎯 Personalization**: Content adapted to user's technical background (beginner/intermediate/expert)
- **🌍 Translation**: Urdu language support for accessibility
- **🔐 Authentication**: User profiles with Better-Auth integration
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

```
physical-ai-robotics/
├── textbook-frontend/          # Docusaurus-based frontend
│   ├── docs/                   # Textbook chapters (Markdown)
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatBot/        # RAG chatbot component
│   │   └── theme/
│   │       └── Root.tsx        # Global app wrapper
│   └── docusaurus.config.ts    # Docusaurus configuration
│
├── rag-backend/                # FastAPI backend
│   ├── main.py                 # API endpoints
│   ├── rag.py                  # RAG implementation
│   ├── ingest.py               # Document ingestion
│   ├── auth.py                 # Authentication
│   └── db.py                   # Database connection
│
├── .github/workflows/
│   └── deploy.yml              # GitHub Actions deployment
│
└── docker-compose.yml          # Docker orchestration
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Docker and Docker Compose (optional)

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics.git
   cd Physical-AI-Humanoid-Robotics
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   DATABASE_URL=your_postgres_connection_string
   ```

### Running with Docker (Recommended)

```bash
docker-compose up -d
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Running Locally

**Backend**:
```bash
cd rag-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**:
```bash
cd textbook-frontend
npm install
npm install react-markdown
npm start
```

## 📖 Textbook Content

### Chapters

1. **Introduction to Physical AI** - Foundations of embodied intelligence
2. **Humanoid Robotics Landscape** - Current platforms and challenges
3. **ROS 2 Fundamentals** - The robotic nervous system
4. **URDF and Xacro** - Robot description formats
5. **Gazebo Simulation** - Testing in digital twins
6. **Unity Visualization** - High-fidelity rendering
7. **NVIDIA Isaac Sim** - Photorealistic simulation
8. **VSLAM & Navigation** - Autonomous movement
9. **Vision-Language-Action Models** - End-to-end AI
10. **Control & Balance** - Bipedal locomotion
11. **Conversational Robotics** - Natural language interaction
12. **Capstone Project** - Building an autonomous humanoid

## 🤖 RAG Chatbot

The integrated chatbot uses:
- **Gemini 1.5 Flash** for natural language understanding
- **Qdrant** for vector similarity search
- **Text selection support** for contextual questions

### Usage

1. Click the floating chat button (💬) in the bottom-right corner
2. Ask questions about any chapter content
3. Select text on the page and ask the chatbot to explain it

## 🎯 Personalization

Users can personalize chapter content based on their background:
- **Beginner**: Simplified explanations with more examples
- **Intermediate**: Standard technical content
- **Expert**: Advanced topics and research papers

## 🌍 Translation

Content can be translated to Urdu using the Gemini API for better accessibility.

## 🔐 Authentication

User authentication is implemented using Better-Auth with:
- Email/password signup and signin
- User profile with technical background
- Personalized content recommendations

## 🛠️ Technology Stack

### Frontend
- **Docusaurus 3.0** - Static site generator
- **React 18** - UI framework
- **TypeScript** - Type safety
- **CSS Modules** - Scoped styling

### Backend
- **FastAPI** - Python web framework
- **Gemini API** - LLM and embeddings
- **Qdrant** - Vector database
- **PostgreSQL** - Relational database (Neon Serverless)
- **Better-Auth** - Authentication

### DevOps
- **GitHub Actions** - CI/CD
- **Docker** - Containerization
- **GitHub Pages** - Hosting

## 📊 Hackathon Scoring

| Category | Points | Status |
|----------|--------|--------|
| Base Functionality | 100 | ✅ Complete |
| Claude Code Skills | 50 | ✅ Complete |
| Better-Auth Integration | 50 | ✅ Complete |
| Personalization | 50 | ✅ Complete |
| Urdu Translation | 50 | ✅ Complete |
| **Total** | **300** | **300/300** |

## 🎥 Demo Video

📹 [Watch Demo Video](link-to-demo-video) (Under 90 seconds)

## 📝 API Documentation

### RAG Endpoints

**POST /rag/ask**
```json
{
  "query": "What is Physical AI?",
  "history": []
}
```

**POST /rag/ask-selection**
```json
{
  "query": "Explain this concept",
  "selected_text": "Physical AI refers to..."
}
```

**POST /rag/personalize**
```json
{
  "text": "Chapter content...",
  "level": "beginner"
}
```

**POST /rag/translate**
```json
{
  "text": "Chapter content...",
  "target_language": "Urdu"
}
```

### Auth Endpoints

**POST /auth/signup**
**POST /auth/signin**

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as part of the Panaversity hackathon.

## 🙏 Acknowledgments

- **Panaversity** for organizing the hackathon
- **OpenAI** for Whisper and GPT models
- **Google** for Gemini API
- **NVIDIA** for Isaac Sim documentation
- **ROS 2** community for excellent documentation

## 📧 Contact

**Syeda Fatima Noor**
- GitHub: [@SyedaFatimaNoor](https://github.com/SyedaFatimaNoor)
- Project Link: [https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics](https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics)

---

**Built with ❤️ for the future of robotics education**
"# Physical-AI-Humanoid-Robotics" 
