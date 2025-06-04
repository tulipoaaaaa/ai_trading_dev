# CryptoFinance Corpus Builder

A professional-grade PyQt6 desktop application for building, managing, and analyzing large-scale cryptocurrency research corpora.

---

## Key Features

- **Automated Data Collection** from 9+ sources (ISDA, GitHub, Anna's Archive, arXiv, FRED, BitMEX, Quantopian, SciDB, Web)
- **Advanced Document Processing**: PDF, text, batch, OCR, deduplication, domain classification, quality control, analytics
- **Corpus Management**: File browser, metadata editing, batch operations, domain balancing, real-time statistics
- **Modern UI/UX**: Consistent, web-inspired design, dark/light themes, iconography, sound and visual notifications
- **Extensible & Modular**: Easily add new collectors, processors, or analytics modules

---

## Quickstart

### Prerequisites

- Python 3.8+
- Windows 10/11
- Virtual environment (recommended: `G:\venv\ai_trading_dev_1`)
- 4GB+ RAM, 10GB+ disk

### Installation

```bash
git clone https://github.com/your-org/CryptoFinanceCorpusBuilder.git
cd CryptoFinanceCorpusBuilder
python -m venv G:\venv\ai_trading_dev_1
G:\venv\ai_trading_dev_1\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Launch

```bash
python app/main.py
```
or double-click `launch_app.bat` (Windows)

---

## Usage Overview

1. **Configure**: Set up API keys, directories, and environment in the Configuration tab.
2. **Collect**: Use the Collectors tab to gather documents from multiple sources.
3. **Process**: Batch process files in the Processors tab.
4. **Manage**: Organize, search, and edit your corpus in the Corpus Manager.
5. **Balance**: Use the Balancer tab to optimize domain distribution.
6. **Analyze**: Explore analytics and trends in the Analytics tab.
7. **Logs**: Monitor real-time logs and errors in the Logs tab.

---

## Documentation

- [User Guide](./USER_GUIDE.md)
- [Admin Guide](./ADMIN_GUIDE.md)
- [Developer Guide](./DEVELOPER_GUIDE.md)
- [Architecture](./ARCHITECTURE.md)
- [Troubleshooting & FAQ](./TROUBLESHOOTING.md)
- [Changelog](./CHANGELOG.md)

---

## Support

- For issues, please use GitHub Issues or contact support@yourcompany.com

---

## License

MIT License. See [LICENSE](./LICENSE) for details.
