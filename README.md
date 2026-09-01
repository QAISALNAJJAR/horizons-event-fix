# 🎯 Horizons Event Checker

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Security-Obfuscated-red.svg" alt="Security">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

<p align="center">
  <b>Check your event registration status on horizons-pal.net with one click</b>
</p>

---

## 🚀 Quick Start

### Windows
1. Download [`install.bat`](install/install.bat)
2. Double-click to run

### macOS/Linux
1. Download [`install.sh`](install/install.sh)
2. Run in terminal:
```bash
chmod +x install.sh
./install.sh
```

### Manual (Any Platform)
```bash
pip install requests browser-cookie3
python main.py
```

---

## 🔒 Security

This application is **obfuscated** to protect against:
- **Reverse engineering** - Source code cannot be easily recovered
- **Man-in-the-middle attacks** - SSL verification enforced
- **Code tampering** - Integrity verification built-in

---

## 📋 Requirements

| Requirement | Auto-Installed |
|-------------|----------------|
| Python 3.8+ | ✅ Yes |
| requests | ✅ Yes |
| browser-cookie3 | ✅ Yes |

---

## 📁 Project Structure

```
horizons-event-fix/
├── main.py                    # Obfuscated code (public)
├── events.json                # Current events data
├── requirements.txt           # Python dependencies
├── run.py                     # Run script
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

## ❓ FAQ

**Q: Do I need to install Python?**  
A: Yes, Python is required. The install script can help install it.

**Q: Is my data safe?**  
A: Yes! The app only reads your browser cookies locally. Nothing is shared.

**Q: What browsers are supported?**  
A: Chrome, Firefox, Safari, Edge, Brave, Opera, Chromium

**Q: Why is the code obfuscated?**  
A: To protect against reverse engineering and ensure code integrity.

---

## 📄 License

MIT License - Free to use and modify.

---

<p align="center">
  Made with ❤️ for horizons-pal.net
</p>
