#!/usr/bin/env python3
"""把 bioinfo-tutor/ 打包成 bioinfo-tutor.zip，給 Claude 應用程式上傳用。

用法（在倉庫根目錄執行）：

    python build_zip.py            重新產生 bioinfo-tutor.zip
    python build_zip.py --check    只比對、不寫入；zip 與資料夾內容不一致時以非 0 結束

bioinfo-tutor.zip 是產物，不要手改。SKILL.md 改過之後重跑一次，兩個檔案一起 commit。
只用 Python 標準函式庫，Windows、macOS、Linux 都能執行。
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

SKILL_NAME = "bioinfo-tutor"
ROOT = Path(__file__).resolve().parent
SKILL_DIR = ROOT / SKILL_NAME
ZIP_PATH = ROOT / (SKILL_NAME + ".zip")

# 不打包的雜物
SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
SKIP_DIRS = {"__pycache__", ".git"}
# 視為文字檔的副檔名：打包時統一成 LF 換行，在 Windows 上產生的 zip 才會和其他平台一致
TEXT_SUFFIXES = {".md", ".txt", ".py", ".r", ".json", ".yaml", ".yml", ".csv", ".tsv"}
# 固定的時間戳：內容沒變，重跑出來的 zip 就不變
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def collect() -> dict[str, bytes]:
    """回傳 {zip 內的路徑: 內容}。zip 的根是 Skill 資料夾本身，這是上傳時要求的結構。"""
    entries: dict[str, bytes] = {}
    if not SKILL_DIR.is_dir():
        return entries
    for path in sorted(SKILL_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(SKILL_DIR)
        if path.name in SKIP_NAMES or path.name.startswith("~$") or path.suffix == ".pyc":
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        data = path.read_bytes()
        if path.suffix.lower() in TEXT_SUFFIXES:
            data = data.replace(b"\r\n", b"\n")
        entries[SKILL_NAME + "/" + rel.as_posix()] = data
    return entries


def _field(front: str, key: str) -> str | None:
    """取出 frontmatter 裡單行的欄位值，去掉外層引號。"""
    m = re.search(r"^%s:[ \t]*(.*)$" % re.escape(key), front, re.M)
    if not m:
        return None
    value = m.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def problems(entries: dict[str, bytes]) -> list[str]:
    """檢查上傳時會被擋下來的幾件事。回傳問題清單，空的代表沒問題。"""
    key = SKILL_NAME + "/SKILL.md"
    if key not in entries:
        return ["找不到 %s/SKILL.md" % SKILL_NAME]

    found: list[str] = []
    extra = sorted(k for k in entries if k != key and k.endswith("/SKILL.md"))
    if extra:
        found.append("一個 Skill 只能有一份 SKILL.md，多出來的：" + ", ".join(extra))

    try:
        text = entries[key].decode("utf-8")
    except UnicodeDecodeError:
        return found + ["SKILL.md 不是 UTF-8 編碼"]

    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return found + ["SKILL.md 的第一行必須是 ---，並用另一行 --- 結束 frontmatter"]
    front = m.group(1)

    name = _field(front, "name")
    if not name:
        found.append("frontmatter 缺 name")
    else:
        if name != SKILL_NAME:
            found.append("name 是 %r，必須和資料夾名稱 %r 相同" % (name, SKILL_NAME))
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
            found.append("name 只能用小寫英數與連字號，最長 64 個字元")

    description = _field(front, "description")
    if not description:
        found.append("frontmatter 缺 description（要寫在同一行）")
    else:
        if len(description) > 1024:
            found.append("description 有 %d 個字元，上限是 1024" % len(description))
        if "<" in description or ">" in description:
            found.append("description 不能有角括號 < >")
    return found


def build(entries: dict[str, bytes]) -> None:
    with zipfile.ZipFile(ZIP_PATH, "w") as zf:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # 不同作業系統寫出相同的檔頭
            info.external_attr = 0o100644 << 16
            zf.writestr(info, entries[name])


def check(entries: dict[str, bytes]) -> int:
    if not ZIP_PATH.is_file():
        print("[不一致] 找不到 %s，請執行 python build_zip.py" % ZIP_PATH.name)
        return 1
    with zipfile.ZipFile(ZIP_PATH) as zf:
        packed = {n: zf.read(n) for n in zf.namelist() if not n.endswith("/")}
    missing = sorted(set(entries) - set(packed))
    extra = sorted(set(packed) - set(entries))
    changed = sorted(n for n in entries if n in packed and entries[n] != packed[n])
    if not (missing or extra or changed):
        print("[一致] %s 與 %s/ 的內容相同（%d 個檔案）" % (ZIP_PATH.name, SKILL_NAME, len(entries)))
        return 0
    for label, names in (("zip 裡缺少", missing), ("zip 裡多出", extra), ("內容不同", changed)):
        for n in names:
            print("[不一致] %s：%s" % (label, n))
    print("請執行 python build_zip.py 重新產生，再把 zip 一起 commit。")
    return 1


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = argv[1:]
    if args not in ([], ["--check"]):
        print(__doc__)
        return 2

    entries = collect()
    found = problems(entries)
    if found:
        for p in found:
            print("[問題] " + p)
        return 1

    if args == ["--check"]:
        return check(entries)

    build(entries)
    print("[完成] 已產生 %s（%d 個檔案，%d bytes）" % (ZIP_PATH.name, len(entries), ZIP_PATH.stat().st_size))
    for n in sorted(entries):
        print("        " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
