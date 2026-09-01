# 🎯 Horizons Event Checker

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

<p align="center">
  <b>Check your event registration status on horizons-pal.net with one click</b>
</p>

---

## 🚀 Quick Start

### Option 1: Easy Install (Recommended)

**Windows:**
1. Download [`install.bat`](install.bat)
2. Double-click to run
3. Done! 🎉

**macOS/Linux:**
1. Download [`install.sh`](install.sh)
2. Run in terminal:
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Manual Install

```bash
# Clone the repo
git clone https://github.com/QAISALNAJJAR/horizons-event-fix.git
cd horizons-event-fix

# Install dependencies
pip install requests browser-cookie3

# Run
python main.py
```

---

## 📋 Requirements

| Requirement | Auto-Installed? |
|-------------|-----------------|
| Python 3.8+ | ✅ Yes |
| requests | ✅ Yes |
| browser-cookie3 | ✅ Yes |

---

## 🔧 For Admins: Setting Up the Dashboard

### Step 1: Deploy to Vercel

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → Import your repo
3. Click Deploy

### Step 2: Update the URL

In `main.py`, change:
```python
DASHBOARD_URL = 'https://your-project.vercel.app/api/event'
```

### Step 3: Manage Events

1. Go to `https://your-project.vercel.app`
2. Login with password: `horizons2026`
3. Add events and set one as **Active**

---

## 🔐 Change Dashboard Password

Edit `dashboard/index.html`:
```javascript
const PASSWORD = 'your-new-password';
```

---

## 📱 How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Admin Panel   │────▶│  Vercel Hosted  │────▶│  User's Script  │
│   (Dashboard)   │     │     API         │     │   (main.py)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                               │
        │                                               ▼
        │                                       ┌─────────────────┐
        │                                       │  Check Browser  │
        │                                       │    Cookies      │
        │                                       └─────────────────┘
        │                                               │
        ▼                                               ▼
┌─────────────────┐                             ┌─────────────────┐
│  Set Active     │                             │  Show Result:   │
│  Event ID       │                             │  ✅ Registered  │
└─────────────────┘                             │  ❌ Not Registered│
                                                └─────────────────┘
```

---

## ❓ FAQ

**Q: Is my data safe?**  
A: Yes! The script only reads your browser cookies locally. Nothing is shared.

**Q: What browsers are supported?**  
A: Chrome, Firefox, Safari, Edge, Brave, Opera, Chromium

**Q: Do I need to install Python?**  
A: No! The install script does everything for you.

---

## 📄 License

MIT License - Free to use and modify.

---

<p align="center">
  Made with ❤️ for horizons-pal.net
</p>
