def update():
    print("Updating 2b2t-RPC...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "pypresence"])


def main():
    from datetime import date, datetime, time
    from pathlib import Path
    from platform import system
    from time import sleep
    from pypresence import Client

    print("Starting RPC...")
    rpc = Client(673133177274892290)
    rpc.start()

    start = None
    pos = []
    est = "None"
    user = ""
    state = 0

    sys = system()
    if sys == "Windows":
        file = Path("AppData") / "Roaming" / ".minecraft"
    elif sys == "Darwin":
        file = Path("Library") / "Application Support" / "minecraft"
    elif sys == "Linux":
        file = ".minecraft"

    with open(Path.home() / file / "logs" / "latest.log") as f:
        while True:
            line = f.readline()
            if line:
                text = line[11:-1]
                try:
                    t = datetime.combine(date.today(), time.fromisoformat(line[1:9])).timestamp()
                    if text.startswith("[main/INFO]: Setting user: "):
                        user = text[27:]
                    elif text.startswith("[main/INFO]: Connecting to "):
                        start = None
                        pos = []
                        state = 1
                    elif text == "[main/INFO]: [CHAT] 2b2t is full":
                        start = int(t)
                        state = 2
                    elif text.startswith("[main/INFO]: [CHAT] Position in queue: "):
                        p = int(text[39:])
                        pos.append((t, p))
                        if len(pos) == 61:
                            pos[0:1] = []

                        if len(pos) == 60:
                            est = ""
                            seconds = (t - pos[0][0]) / (pos[0][1] - p)
                            seconds = int(seconds * p)
                            days = seconds // 86400
                            if days:
                                est += f"{days}d "
                            hours = seconds % 86400 // 3600
                            if hours:
                                est += f"{hours}h "
                            est += f"{seconds % 3600 // 60}m"

                        state = 3
                    elif text == "[main/INFO]: [CHAT] Connecting to the server...":
                        pos = []
                        start = int(t)
                        state = 4
                except ValueError:
                    pass
            else:
                if state == 1:
                    rpc.set_activity(large_image="image", large_text="2b2t.org", details="Connecting...")
                elif state == 2:
                    rpc.set_activity(large_image="image", large_text="2b2t.org", details="Waiting in queue", start=start)
                elif state == 3:
                    rpc.set_activity(large_image="image", large_text="2b2t.org", details=f"Position in queue: {pos[-1][1]}", state="Estimated time: " + est, start=start)
                    sleep(10)
                elif state == 4:
                    rpc.set_activity(large_image="image", large_text="2b2t.org", details="Playing", start=start)


if __name__ == '__main__':
    import subprocess
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == "--noupdate":
        main()
    elif len(sys.argv) != 1:
        print("Usage: python main.py [--noupdate]")
    update()
    subprocess.check_call([sys.executable, sys.argv[0], "--noupdate"])
