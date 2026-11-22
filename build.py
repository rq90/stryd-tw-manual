"""Build the self-contained manual with Python's standard library."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
CHAPTERS = [
    ("watch", "確認跑錶支援哪些功能", "選跑錶", "查即時瓦數、Stryd 課表與 RQ 記錄"),
    ("charge", "替 Stryd 充電", "充電", "依型號辨認充電座與電量燈號"),
    ("phone", "用手機設定 Stryd", "手機設定", "加入裝置，確認單顆或 Duo"),
    ("shoe", "把 Stryd 扣上跑鞋", "安裝鞋扣", "確認扣夾方向與風孔位置"),
    ("pair", "把 Stryd 配對到跑錶", "跑錶配對", "按品牌設定跑步模式與功率欄位"),
    ("run", "記錄第一次跑步", "第一次跑步", "看見瓦特、儲存活動，再確認功率曲線"),
    ("help", "遇到問題怎麼辦", "故障排除", "從燈號、連線或紀錄異常開始查"),
]


def nav_links():
    return "\n".join(
        f'<a href="#{key}"><span class="number">{i:02}</span>{short}</a>'
        for i, (key, _, short, _) in enumerate(CHAPTERS, 1)
    )


def home_links():
    return "\n".join(
        f'<li><a href="#{key}"><span class="number">{i:02}</span>'
        f'<span><strong>{title}</strong><small>{hint}</small></span>'
        '<span class="arrow" aria-hidden="true">→</span></a></li>'
        for i, (key, title, _, hint) in enumerate(CHAPTERS, 1)
    )


def chapter(index, chapter):
    key, title, _, hint = chapter
    previous = CHAPTERS[index - 1] if index else None
    following = CHAPTERS[index + 1] if index + 1 < len(CHAPTERS) else None
    previous_link = (f'<a href="#{previous[0]}">← {previous[2]}</a>'
                     if previous else '<a href="#home">← 手冊首頁</a>')
    next_link = (f'<a class="next" href="#{following[0]}">下一步・{following[2]} →</a>'
                 if following else '<a class="next" href="#home">回手冊首頁 →</a>')
    body = (CONTENT / f"{key}.html").read_text(encoding="utf-8")
    if key == "shoe":
        body = ('<figure class="shoe"><img src="assets/shoe-orientation.png" '
                'width="1000" height="630" alt="從鞋面上方看，扣夾厚端朝小腿，前端壓扣朝鞋尖。">'
                '<figcaption>扣夾方向示意。以穿鞋者的腳為準。</figcaption></figure>\n' + body)
    return f'''<article id="{key}" class="chapter" aria-labelledby="title-{key}">
<div class="chapter-meta">安裝與使用手冊 <span>/</span> {index + 1:02}・共 07 節</div>
<h2 id="title-{key}" tabindex="-1">{escape(title)}</h2><p class="dek">{escape(hint)}。</p>
{body}
<nav class="paging" aria-label="前後章節">{previous_link}{next_link}</nav></article>'''


def build():
    template = (CONTENT / "template.html").read_text(encoding="utf-8")
    values = {"@@NAV@@": nav_links(), "@@HOME@@": home_links(),
              "@@CHAPTERS@@": "\n".join(chapter(i, c) for i, c in enumerate(CHAPTERS))}
    for key, value in values.items():
        template = template.replace(key, value)
    (ROOT / "docs" / "index.html").write_bytes(template.encode("utf-8"))


if __name__ == "__main__":
    build()
