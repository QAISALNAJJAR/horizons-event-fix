# Horizons Event Registration Checker

## Setup

### 1. Deploy Dashboard to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
cd "Horizons fix"
vercel
```

3. After deployment, update `DASHBOARD_URL` in `main.py`:
```python
DASHBOARD_URL = 'https://your-actual-project.vercel.app/api/event'
```

### 2. Dashboard Password

Default password: `horizons2026`

To change it, edit `dashboard/index.html`:
```javascript
const PASSWORD = 'your-new-password';
```

### 3. Run the Script

```bash
python3 main.py
```

## Dashboard Features

- **Password protected** login
- Add/remove events
- Set active event
- View all events

## How It Works

1. Admin logs into dashboard at `https://your-project.vercel.app`
2. Adds events and sets one as active
3. User runs `python3 main.py`
4. Script fetches active event from Vercel API
5. Script extracts browser cookies and checks registration
6. Results sent to ntfy.sh
# horizons-event-fix
