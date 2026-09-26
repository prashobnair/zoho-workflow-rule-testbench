import argparse
import json
from pathlib import Path
from engine import simulate

def main():
    parser = argparse.ArgumentParser(description='Trace fictional CRM workflow rules offline')
    parser.add_argument('fixture')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.fixture).read_text(encoding='utf-8'))
        print(json.dumps(simulate(data['rules'], data['record'], data.get('initial_event', 'deal_created')), indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Input error: {exc}\n')

if __name__ == '__main__':
    main()
