# AI Devs 3 - Tasks UI

A web application for solving tasks from the AI Devs 3 course, starting with the Robot Login task. 
The project includes a user interface and solution implementation using LLM models.

## 🚀 Features

- LLM models integration (OpenAI GPT-4)
- Multi-language support (PL/ENG)
- Answer caching system
- Automatic flag detection and saving
- Firmware file downloading and saving
- User-friendly Streamlit interface
- Dark mode support

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Streamlit
- BeautifulSoup4
- Requests

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/username/AI-Devs-3-Solutions-App.git
cd AI-Devs-3-Solutions-App
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```

4. Run the application:
```bash
streamlit run ui/app.py
```

## 🏗️ Project Structure

```
AI-Devs-3-Solutions-App/
├── ui/                      # User interface
│   ├── app.py              # Main application file
│   ├── styles/             # CSS styles
│   ├── components/         # Reusable UI components
│   ├── views/              # View components
│   └── services/           # UI-related services
├── tasks/                  # Task implementations
│   └── week1/             
│       └── episode01/      # Robot Login task
├── services/              
│   └── llm/               # LLM service implementations
├── translations/           # Language files
│   ├── common/            # Shared translations
│   └── week1/             # Task-specific translations
└── files_storage/         # Downloaded files storage
```

## 🔧 Configuration

Available in:
- `.env` - OpenAI API key
- `.streamlit/config.toml` - Streamlit configuration
- `tasks/week1/episode01/robot_login/config.py` - Task configuration

## 🌍 Translations

The application supports two languages:
- Polish (default)
- English

Language files are stored in the `translations/` directory.

## 📝 License

This project is available under the MIT license.
