"""BM25 trên các đoạn transcript. Chỉ dùng thư viện chuẩn.

Tiếng Việt tách theo âm tiết nên ngoài từ đơn còn đánh chỉ mục cặp âm tiết liền nhau
("context window", "học máy") để khớp cụm tốt hơn.
"""
import math
import re
from collections import Counter

STOP = set("""
và là của có cho các những một được thì mà này đó để với trong khi từ ra vào lại cũng như
không nó các bạn mình chúng ta thế nào gì đây đấy nhé ạ à ừ ờ thôi rồi sẽ đã đang nếu vì
nên hay hoặc bị theo về trên dưới hơn rất cái con người thì là the a an of to is in and or
""".split())


def tokenize(text):
    words = [w for w in re.findall(r"\w+", text.lower()) if not w.isdigit()]
    unigrams = [w for w in words if w not in STOP and len(w) > 1]
    bigrams = [f"{a}_{b}" for a, b in zip(words, words[1:]) if a not in STOP or b not in STOP]
    return unigrams + bigrams


class Index:
    def __init__(self, segments, k1=1.4, b=0.75):
        self.segments = segments
        self.k1, self.b = k1, b
        self.docs = [Counter(tokenize(s["section"] + " " + s["text"])) for s in segments]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter()
        for d in self.docs:
            df.update(d.keys())
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.by_id = {s["id"]: s for s in segments}

    def search(self, query, transcripts=None, k=8):
        q = Counter(tokenize(query))
        scored = []
        for i, (doc, dl) in enumerate(zip(self.docs, self.lens)):
            seg = self.segments[i]
            if transcripts and seg["transcript"] not in transcripts:
                continue
            score = 0.0
            for t, qtf in q.items():
                tf = doc.get(t)
                if tf:
                    score += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * dl / self.avg))
            if score > 0:
                scored.append((score, seg))
        scored.sort(key=lambda x: -x[0])
        return [dict(seg, score=round(s, 2)) for s, seg in scored[:k]]
