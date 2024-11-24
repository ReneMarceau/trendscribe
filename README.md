# TrendScribe

An AI-powered content generation tool that transforms TechCrunch articles into engaging LinkedIn posts.

## 🚀 Features

- **Smart RSS Processing**: Automatically fetches and processes TechCrunch articles
- **AI Analysis**: Leverages Perplexity API for deep content analysis
- **LinkedIn Post Generation**: Creates professional posts using GPT-4
- **Duplicate Prevention**: Smart tracking of processed articles using SQLAlchemy
- **Rich CLI Interface**: Interactive and beautifully formatted terminal output

## 🛠️ Technical Stack

- **Python 3.8+**
- **SQLAlchemy**: ORM for database management
- **OpenAI GPT-4**: AI content generation
- **Perplexity API**: Content analysis
- **Rich**: Terminal formatting
- **BeautifulSoup4**: HTML processing

## 📋 Prerequisites

- Python 3.8 or higher
- Perplexity API key
- OpenAI API key

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trendscribe.git
   cd trendscribe
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🚀 Usage

Run the application:
```bash
python main.py
```

## 📁 Project Structure

```
trendscribe/
├── main.py           # Application entry point
├── database.py       # SQLAlchemy database models
├── rss_handler.py    # RSS feed processing
├── api_client.py     # API integrations
├── requirements.txt  # Project dependencies
└── .env             # Environment configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
