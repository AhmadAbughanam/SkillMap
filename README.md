# SkillMap-Flask 🚀

**AI-Powered Personal Skill Development Tracker**

SkillMap-Flask is a comprehensive self-improvement platform that helps you track your learning journey with intelligent insights. Create skills, log milestones, and receive AI-powered guidance to accelerate your personal development.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-v1.4+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 🎯 Skill Management
- **Create & Organize**: Build your skill portfolio with categories and detailed descriptions
- **Progress Tracking**: Monitor your development journey over time
- **Flexible Categories**: Organize skills by domain (technical, creative, personal, etc.)

### 📈 Milestone System
- **Progress Logging**: Record achievements and learning milestones with timestamps
- **Detailed Notes**: Add context and reflections to each milestone
- **Visual Timeline**: Track your learning progression chronologically

### 🤖 AI-Powered Insights
- **Automatic Generation**: Get intelligent insights when creating skills or adding milestones
- **Local LLM Processing**: Privacy-first approach using locally hosted Mistral 7B model
- **Personalized Recommendations**: Receive tailored advice based on your progress patterns

### 📊 Insight Dashboard
- **Centralized View**: Access all AI-generated insights in one place
- **Smart Filtering**: Filter insights by skill, section, or generation time
- **Learning Analytics**: Understand your development patterns and trends

### 🛠️ Technical Stack
- **Backend**: Flask with SQLAlchemy ORM
- **Frontend**: Bootstrap for responsive design
- **AI Engine**: llama-cpp-python with Mistral 7B Instruct GGUF
- **Database**: SQLite (easily configurable for other databases)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM (recommended for optimal LLM performance)
- AVX-compatible CPU (for llama-cpp-python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/SkillMap-Flask.git
   cd SkillMap-Flask
   ```

2. **Set up virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download and configure LLM model**
   ```bash
   # Create models directory
   mkdir models
   
   # Download Mistral 7B Instruct GGUF model
   # Place mistral-7b-instruct-v0.1.Q2_K.gguf in the models/ directory
   
   # Update model path in app/utils/llm_client.py if needed
   ```

5. **Initialize the database**
   ```bash
   # The database will be created automatically on first run
   flask run
   # or
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📖 Usage Guide

### Getting Started

1. **Create Your First Skill**
   - Navigate to the skills section
   - Add a new skill with category and description
   - The AI will automatically generate initial insights

2. **Track Your Progress**
   - Add milestones as you learn and improve
   - Include detailed notes about your achievements
   - View your progress timeline

3. **Leverage AI Insights**
   - Review AI-generated recommendations in the dashboard
   - Use insights to plan your next learning steps
   - Filter insights by skill or time period

### Best Practices

- **Be Specific**: Write detailed skill descriptions for better AI insights
- **Regular Updates**: Log milestones frequently to track consistent progress
- **Reflect on Insights**: Use AI recommendations to guide your learning strategy

## 🏗️ Project Structure

```
SkillMap-Flask/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # SQLAlchemy models
│   ├── routes/              # Flask blueprints
│   │   ├── __init__.py
│   │   ├── skills.py        # Skill management routes
│   │   └── llm.py           # LLM insight routes
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── skills/
│   │   └── insights/
│   ├── static/              # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/               # Utility modules
│       └── llm_client.py    # LLM integration logic
├── models/                  # LLM model files
│   └── mistral-7b-instruct-v0.1.Q2_K.gguf
├── venv/                    # Virtual environment
├── config.py                # Application configuration
├── run.py                   # Application entry point
├── test.py                  # Manual testing utilities
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🤖 LLM Integration Deep Dive

### How It Works
- **Trigger Points**: Insights generate automatically when skills are created or milestones are added
- **Local Processing**: All AI processing happens on your machine - no data leaves your system
- **Context Aware**: The AI considers your skill history and progress patterns

### Model Configuration
```python
# Example: Manual insight generation
from app.utils.llm_client import generate_llm_insight
from app.models import Skill

with app.app_context():
    skill = Skill.query.first()
    insights = generate_llm_insight(skill)
    print(insights)
```

### Performance Optimization
- **CPU Optimization**: Configured for CPU inference with optimal thread usage
- **Memory Management**: Efficient model loading and memory cleanup
- **Response Caching**: Avoid regenerating identical insights

## 🛠️ Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
flask run --debug
```

### Testing LLM Integration
```bash
# Test model loading and generation
python test.py
```

### Database Operations
```bash
# Access Flask shell for database operations
flask shell

# Example: Query skills
>>> from app.models import Skill
>>> skills = Skill.query.all()
>>> print(skills)
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with proper testing
4. **Update documentation** as needed
5. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update the README for significant changes
- Test LLM integration thoroughly

## 📋 Roadmap

### Short Term
- [ ] **Enhanced UI/UX** - Modern, responsive design improvements
- [ ] **Export Functionality** - Export skills and progress data
- [ ] **Goal Setting** - Set and track learning objectives

### Medium Term
- [ ] **Multiple LLM Support** - Support for different local models
- [ ] **Progress Analytics** - Advanced charts and progress visualization
- [ ] **Social Features** - Share achievements and compare progress

### Long Term
- [ ] **Mobile App** - Native mobile application
- [ ] **Team Features** - Collaborative skill development
- [ ] **Integration APIs** - Connect with external learning platforms

## ⚠️ System Requirements

### Minimum Requirements
- **RAM**: 4GB (8GB recommended)
- **CPU**: AVX-compatible processor
- **Storage**: 5GB free space (for model and data)
- **OS**: Windows 10+, macOS 10.14+, or modern Linux

### GPU Support (Optional)
For faster inference, GPU support can be enabled:
```bash
# Install CUDA-enabled version
pip install llama-cpp-python[cuda]
```

## 🐛 Troubleshooting

### Common Issues

**Model Loading Errors**
- Ensure your CPU supports AVX instructions
- Verify the model file is in the correct directory
- Check available RAM (minimum 4GB required)

**Flask Application Errors**
- Activate your virtual environment
- Install all requirements: `pip install -r requirements.txt`
- Check Python version compatibility

**Performance Issues**
- Reduce model quantization level for faster inference
- Close other memory-intensive applications
- Consider upgrading RAM for better performance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask Community** - For the excellent web framework
- **Mistral AI** - For the powerful open-source language model
- **llama.cpp** - For efficient local LLM inference
- **Bootstrap** - For responsive UI components

---

**Built with ❤️ by Ahmad Abughanam**

*Empowering personal growth through AI-assisted skill tracking and intelligent insights.*

## 📞 Support

Need help or have questions?
- 🐛 [Report Issues](https://github.com/your-username/SkillMap-Flask/issues)
- 💬 [Discussions](https://github.com/your-username/SkillMap-Flask/discussions)
- 📧 [Contact Developer](mailto:your-email@example.com)
