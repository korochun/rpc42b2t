from datetime import date, datetime, time
from os import stat
from pathlib import Path
from platform import system
from time import sleep

from pypresence import Client as RPC


def main():
    print("Starting RPC...")
    rpc = RPC(673133177274892290)
    rpc.start()

    try:
        start = None
        end = None
        pos = []
        est = "None"
        state = 0

        sys = system()  # Find Minecraft game dir
        if sys == "Windows":
            file = Path("AppData") / "Roaming" / ".minecraft"
        elif sys == "Darwin":
            file = Path("Library") / "Application Support" / "minecraft"
        elif sys == "Linux":
            file = ".minecraft"
        else:
            print("Unknown system, unable to find game dir")
        file = Path.home() / file / "logs" / "latest.log"

        with open(file) as f:  # TODO: Read previous logs if data is insufficient.
            while True:
                line = f.readline()
                if line:
                    text = line[11:-1]
                    try:
                        t = datetime.combine(
                            date.today(), time.fromisoformat(line[1:9])
                        ).timestamp()
                        if text.startswith("[main/INFO]: Connecting to "):
                            end = None
                            est = "None"
                            state = 1
                        elif text == "[main/INFO]: [CHAT] 2b2t is full":
                            start = int(t)
                            pos = []
                            state = 2
                        elif text.startswith("[main/INFO]: [CHAT] Position in queue: "):
                            p = int(text[39:])
                            pos.append((t, p))
                            if len(pos) == 61:
                                pos[0:1] = []

                            if len(pos) == 60:
                                if pos[0][1] == p:
                                    est = "never"
                                else:
                                    est = ""
                                    seconds = (t - pos[0][0]) / (
                                        pos[0][1] - p
                                    )  # FIXME: Time is negative when you're a time traveller.
                                    seconds = int(
                                        seconds * p
                                    )  # TODO: Rework the estimations.
                                    days = seconds // 86400
                                    if days:
                                        est += f"{days}d "
                                    hours = seconds % 86400 // 3600
                                    if hours:
                                        est += f"{hours}h "
                                    est += f"{seconds % 3600 // 60}m"

                            if state == 2:
                                state = 3
                        elif (
                            text == "[main/INFO]: [CHAT] Connecting to the server..."
                            or text.startswith("[main/INFO]: Loaded ")
                        ):
                            pos = []
                            start = int(t)
                            state = 4
                        elif text.startswith(
                            "[main/INFO]: [CHAT] [SERVER] Server restarting in "
                        ):
                            if text.endswith(" minutes..."):
                                end = int(t) + 600 * int(text[50:-12])
                            elif text.endswith(" seconds..."):
                                end = int(t) + 10 * int(text[50:-11])
                            elif text.endswith(" second..."):
                                end = int(t) + 10 * int(text[50:-10])
                            state = 5
                        elif text == "[main/INFO]: Stopping!":
                            print("Hi!")
                            break
                    except ValueError:
                        pass
                else:
                    if state == 1:
                        rpc.set_activity(
                            large_image="image",
                            large_text="2b2t.org",
                            details="Connecting...",
                        )
                    elif state == 2:
                        rpc.set_activity(
                            large_image="image",
                            large_text="2b2t.org",
                            details="Waiting in queue",
                            start=start,
                        )
                    elif state == 3:
                        rpc.set_activity(
                            large_image="image",
                            large_text="2b2t.org",
                            details=f"Position in queue: {pos[-1][1]}",
                            state="Estimated time: " + est,
                            start=start,
                        )
                        sleep(10)
                    elif state == 4:
                        rpc.set_activity(
                            large_image="image",
                            large_text="2b2t.org",
                            details="Playing",
                            start=start,
                        )
                    elif state == 5:
                        rpc.set_activity(
                            large_image="image",
                            large_text="2b2t.org",
                            details=f"Waiting for restart...",
                            state=f"Position in queue: {pos[-1][1]}",
                            end=end,
                        )
                    if stat(f.fileno()).st_nlink == 0:
                        f.close()
                        f = open(file)
    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopping RPC...")
        rpc.close()
