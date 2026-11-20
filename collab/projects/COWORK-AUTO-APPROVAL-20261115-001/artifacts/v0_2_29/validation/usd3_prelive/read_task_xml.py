import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
base = pathlib.Path(__file__).parent / "rehearsal" / "bundle"
for name in ("task_SKILL-COLLAB-GitHub-Watcher.xml", "task_SKILL-COLLAB-Notifier.xml"):
    raw = (base / name).read_bytes()
    for enc in ("utf-16", "utf-8", "cp949"):
        try:
            text = raw.decode(enc)
            if "<Task" in text:
                break
        except UnicodeError:
            continue
    print("==", name, enc, len(text))
    for tag in ("Command", "Arguments", "WorkingDirectory", "LogonType", "RunLevel", "MultipleInstancesPolicy", "Enabled", "ExecutionTimeLimit", "Interval", "Count", "StopIfGoingOnBatteries"):
        for m in re.findall(rf"<{tag}>(.*?)</{tag}>", text, flags=re.S):
            m = re.sub(r'--config "[^"]*"', '--config "<cfg>"', m.strip())
            print(f"  {tag}: {m[:170]}")
    print("  triggers:", re.findall(r"<(LogonTrigger|TimeTrigger|BootTrigger|CalendarTrigger)", text))
