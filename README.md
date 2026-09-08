# Government Portal Network Study

Browser-based performance experiments for government web portals under different
network conditions. The current implementation automates the
[myScheme](https://www.myscheme.gov.in/) scheme-discovery flow with Playwright
and records basic workflow timings.

## Project status

Implemented:

- Firefox automation through Playwright.
- myScheme profile-driven scheme discovery.
- Navigation, workflow, and recommended-scheme load timings.
- Request/response and failed-request instrumentation in `framework/metrics.py`.
- YAML-based user profiles and network configuration models.

The network configuration models are present, but network emulation is not yet
wired into the experiment runner. The current `scripts/run_experiment.py`
therefore runs against the active network connection.

## Requirements

- Python 3.10 or newer
- Firefox, installed through Playwright
- Network access to `https://www.myscheme.gov.in/`

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies and Playwright browser:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install firefox
```

## Run the experiment

From the repository root:

```bash
python scripts/run_experiment.py
```

The default profile is
`config/profiles/user1.yaml`. The browser runs in headed mode so the flow can
be observed, and the script prints:

- Homepage load time
- End-to-end workflow time
- Recommended scheme load time
- Total time

Press Enter when prompted to close the browser.

## Configuration

Edit `config/profiles/user1.yaml` to change the answers used by the automated
flow. The committed profile contains synthetic example data only; do not store
real credentials, identity details, or other sensitive personal information in
the repository.

```yaml
name: Example User
gender: Female
age: 30
state: Maharashtra
location: Rural
category: General
disability: false
minority: true
student: false
bpl: false
family_income: 250000
parent_income: 300000
```

Network profiles are stored under `config/networks/`. Their schema is defined
by `framework.models.NetworkConfig`.

## Repository layout

```text
config/                 YAML profiles and network definitions
framework/              Browser, configuration, models, and metrics helpers
portals/                Portal-specific automation flows
scripts/                Experiment entry points
test_firefox.py         Minimal browser connectivity diagnostic
```

## Troubleshooting

If Firefox is missing, run:

```bash
python -m playwright install firefox
```

If the initial myScheme action appears unresponsive under a throttled network,
the flow waits for the next workflow control rather than using a fixed sleep.
This makes synchronization event-driven while still allowing the page's
client-side application to finish initializing.

## Responsible use

Run experiments only against sites you are authorized to test. Keep request
rates reasonable and avoid submitting sensitive personal information.