import subprocess, os, shutil

async def start(app):
    subprocess.run(["python", app])

async def stop(app):
    subprocess.run(["pkill", "-f", app])

async def restart(app):
    subprocess.run(["pkill", "-f", app])
    subprocess.run(["python", app])

async def delete(app):
    subprocess.run(["pkill", "-f", app])
    subprocess.run(["rm", app])

async def list():
    result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE)
    processes = result.stdout.decode().split("\n")
    apps = []
    for process in processes:
        if "python" in process and ".py" in process:
            app = process.split()[-1]
            apps.append(app)
    return apps

async def restart_all():
    for app in list():
        subprocess.run(["pkill", "-f", app])
        subprocess.run(["python", app])

async def info(app):
    result = subprocess.run(["ps", "-p", app, "-o", "pid,ppid,%cpu,%mem,cmd"], stdout=subprocess.PIPE)
    info = result.stdout.decode().split("\n")[1]
    pid, ppid, cpu, mem, cmd = info.split(maxsplit=4)
    return {"pid": pid, "ppid": ppid, "cpu": cpu, "mem": mem, "cmd": cmd}

async def logs(app):
    subprocess.run(["tail", "-f", f"{app}.log"])
