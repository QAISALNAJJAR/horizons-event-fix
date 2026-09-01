# 🎯 Horizons Event Checker

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Security-Compiled%20Binary-red.svg" alt="Security">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

<p align="center">
  <b>Check your event registration status on horizons-pal.net with one click</b>
</p>

---

## 🚀 Quick Start

### One-Click Install (Recommended)

| Platform | Command |
|----------|---------|
| Windows | Double-click `install/install.bat` |
| macOS/Linux | Run `./install/install.sh` |

### Manual Install

```bash
pip install -r requirements.txt
python run.py
```

---

## 🔒 Security

This application is compiled to a binary extension to protect against:
- **Reverse engineering** - Source code cannot be recovered
- **Man-in-the-middle attacks** - SSL verification enforced
- **Tampering** - Code integrity verification

---

## 📁 Project Structure

```
horizons-event-fix/
├── run.py                     # Run the compiled application
├── main.cpython-314-darwin.so # Compiled binary (macOS)
├── events.json                # Current events data
├── requirements.txt           # Python dependencies
├── vercel.json                # Vercel deployment config
│
├── api/                       # Vercel serverless API
│   └── event.py              # GET active event
│
├── dashboard/                 # Web dashboard
│   └── index.html            # Admin dashboard UI
│
├── install/                   # One-click installers
│   ├── install.sh            # macOS/Linux installer
│   └── install.bat           # Windows installer
│
└── README.md                  # This file
```

---

## 🔧 How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Admin manages  │────▶│  Push to GitHub │────▶│ Vercel deploys  │
│  events via API │     │  (auto)         │     │ (auto)          │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐                             ┌─────────────────┐
│  Show result:   │◀──── User runs run.py ──────│  Fetch active   │
│  ✅ Registered  │                             │  event from API │
│  ❌ Not Registered│                            └─────────────────┘
└─────────────────┘
```

---

## 📋 Requirements

| Requirement | Auto-Installed |
|-------------|----------------|
| Python 3.8+ | ✅ Yes |
| requests | ✅ Yes |
| browser-cookie3 | ✅ Yes |

---

## ❓ FAQ

**Q: Is my data safe?**  
A: Yes! The script only reads your browser cookies locally. Nothing is shared.

**Q: What browsers are supported?**  
A: Chrome, Firefox, Safari, Edge, Brave, Opera, Chromium

**Q: Do I need to install Python?**  
A: No! The install script does everything for you.

**Q: Why is the code compiled?**  
A: To protect against reverse engineering and ensure code integrity.

---

## 📄 License

MIT License - Free to use and modify.

---

<p align="center">
  Made with ❤️ for horizons-pal.net
</p>
