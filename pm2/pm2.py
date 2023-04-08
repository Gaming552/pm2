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

async def clean_runtime_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))

    if os.path.exists(os.path.join(path, "build")):
        shutil.rmtree(os.path.join(path, "build"))
    if os.path.exists(os.path.join(path, "dist")):
        shutil.rmtree(os.path.join(path, "dist"))

    requirements = os.path.join(path, "requirements.txt")
    if os.path.exists(requirements):
        with open(requirements, "r") as f:
            dependencies = f.read().splitlines()
            for dependency in dependencies:
                dependency = os.path.join(path, "venv", "lib", "python3.9", "site-packages", dependency)
                if os.path.exists(dependency):
                    for root, dirs, files in os.walk(dependency):
                        for file in files:
                            if file.endswith(".pyc"):
                                os.remove(os.path.join(root, file))
                    for root, dirs, files in os.walk(dependency):
                        for dir in dirs:
                            if dir == "__pycache__":
                                shutil.rmtree(os.path.join(root, dir))
                    if os.path.exists(os.path.join(dependency, "build")):
                        shutil.rmtree(os.path.join(dependency, "build"))
                    if os.path.exists(os.path.join(dependency, "dist")):
                        shutil.rmtree(os.path.join(dependency, "dist"))

async def reset_database(mysql, redis):
    import aiomysql, aioredis
    os.system("pip install aioredis aiomysql")
    mysql_conn = await aiomysql.connect(**mysql)

    async with mysql_conn.cursor() as cursor:
        await cursor.execute("DROP DATABASE IF EXISTS lisk")
        #await cursor.execute("CREATE DATABASE lisk")

    mysql_conn.close()

    redis_conn = await aioredis.create_redis_pool(**redis)

    await redis_conn.flushdb()

    redis_conn.close()
