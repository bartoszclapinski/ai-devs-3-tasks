# AI Devs 3 - Tasks UI

A web application for solving tasks from the AI Devs 3 course, starting with the Robot Login task. 
The project includes a user interface and solution implementation using LLM models.

## 🚀 Features

- LLM models for solving questions
- Answer caching system
- Automatic flag saving
- Firmware file downloading and saving
- User-friendly Streamlit interface

## 📋 Requirements

- Python 3.8+
- OpenAI API key

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/ai-devs-3-tasks.git
cd ai-devs-3-tasks
```
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Set OpenAI API key:
```bash
OPENAI_API_KEY="your-api-key"
```

## 🎮 Running

Start the Streamlit app:
```bash
streamlit run ui/app.py
```

The application will be available at: `http://localhost:8000`

## 📁 Project Structure

AI-Devs-3/
├── ui/                         # Streamlit user interface  
│   ├── app.py                  # Main application  
│   ├── components/             # Components (flags, files)  
│   └── views/                  # Task views  
├── tasks/                      # Solution logic  
│   └── week1/  
│       └── episode01/  
│           └── robot_login/  
│               ├── models/     # Main logic  
│               ├── services/   # Services (web, llm, files)  
│               └── parsers/    # HTML parsers  
├── services/                   # Shared services  
│   └── llm/                    # LLM models handling  
└── files_storage/              # Storage for downloaded files  
    ├── flags.md                # Found flags  
    ├── home_page/              # UI assets  
    └── week1/                  # Week 1 files  
        └── episode01/          # Episode 1 files  


## ⚙️ Configuration

Configuration available in files:
- `.env` - OpenAI API key
- `.streamlit/config.toml` - Streamlit configuration
- `tasks/week1/episode01/robot_login/config.py` - Task configuration

## 📝 License

This project is available under the MIT license.