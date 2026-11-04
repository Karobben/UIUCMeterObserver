import csv, json
from pathlib import Path
p = Path(__file__).parent
rows = list(csv.DictReader((p/'parking_enforcement_unified.csv').open(encoding='utf-8-sig')))
template = (p/'dashboard_template.html').read_text()
(p/'parking_dashboard.html').write_text(template.replace('__DATA__', json.dumps(rows).replace('</', '<\\/')))
print(f'Embedded {len(rows)} records')
