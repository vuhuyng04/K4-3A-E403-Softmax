"""Rebuild aggregate evidence and anonymized survey log; standard library only."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research'

def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def main():
    source = ROOT / 'data/vlearn-pack/chatlog/tutor_turns.csv'
    rows = read_csv(source)
    k4 = [r for r in rows if r['cohort_hint'] == 'K4']
    free = [r for r in k4 if r['is_preset'].lower() == 'false']
    # Signals, not human-validated intent labels. Context prefix deliberately retained.
    rules = {
        'quiz_context': r'quiz|trắc nghiệm|ôn toàn bộ câu hỏi|luyện theo đề xuất',
        'answer_terms': r'đáp án',
        'explain_terms': r'tại sao|vì sao|giải thích|không hiểu',
        'practice_request': r'(?:cho|tạo|đặt|xin|thêm).{0,30}(?:bài tập|câu hỏi luyện|câu hỏi cho)',
        'check_request': r'đúng không|kiểm tra.{0,30}(?:câu trả lời|đáp án)|chấm.{0,10}bài',
    }
    matches = {name: [r for r in free if re.search(pattern, r['student_question'], re.I)] for name, pattern in rules.items()}
    matches['quiz_and_explain'] = [r for r in matches['quiz_context'] if re.search(rules['explain_terms'], r['student_question'], re.I)]
    summary = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
               'all_turns': len(rows), 'k4_turns': len(k4),
               'k4_students': len({r['student'] for r in k4}),
               'k4_nonpreset': len(free), 'k4_preset': len(k4)-len(free), 'rules': rules,
               'signals': {name: {'turns': len(rs), 'students': len({r['student'] for r in rs}),
                                 'pct_nonpreset': round(100*len(rs)/len(free), 2),
                                 'turn_ids': [r['turn_id'] for r in rs]} for name, rs in matches.items()}}
    (OUT/'mining-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    survey = read_csv(ROOT/'Thông tin liên hệ.csv')
    columns = list(survey[0])
    excluded = {'Đào Ngọc Bình Thiên', 'Phong Nguyễn nguyên'}
    external = [r for r in survey if r['Tên'].strip() not in excluded]
    with (OUT/'survey-anonymized.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['respondent_id', 'practice', 'difficulty', 'ai_help', 'willing'])
        for i, r in enumerate(external, 1):
            writer.writerow([f'R{i:02}']+[r[c] for c in columns[4:8]])
    stats = {'total': len(survey), 'excluded_team': len(survey)-len(external), 'external_provisional': len(external),
             'questions': dict(zip(['practice','difficulty','ai_help','willing'], columns[4:8])),
             'answers': {key: {value: sum(r[col].strip().casefold()==value for r in external)
                              for value in sorted({r[col].strip().casefold() for r in external})}
                         for key, col in zip(['practice','difficulty','ai_help','willing'], columns[4:8])}}
    (OUT/'survey-summary.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['signals','rules']}, ensure_ascii=False))
    print(json.dumps({k:{a:b for a,b in v.items() if a!='turn_ids'} for k,v in summary['signals'].items()}, ensure_ascii=False))
    print(json.dumps(stats, ensure_ascii=False))

if __name__ == '__main__':
    main()
