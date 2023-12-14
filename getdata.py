# -*- coding: utf-8 -*-

from os import system as sh
from pathlib import Path
from json import load, dumps
jsonconfig = dict(
    indent=4, sort_keys=True, ensure_ascii=True
)
path = Path(__file__).parent
giturl = "https://github.com/circuitalmynds/music_z5"
videos = path.joinpath("videos")
info = path.joinpath("info.json")


def getinfo():
    return load(info.open())


def save_info(data):
    info.open("w").write(dumps(
        data, **jsonconfig
    ))


def getfiles():
    urlfile, totalsize, content = f"{giturl}/raw/main/videos", 0.0, []
    sh(
        f"cd {str(path)} && find ./videos* -iname '*.mp4' -size -95M | cat > files.txt"
    )
    listfiles = []
    raw = "".join([giturl.replace("github.com", "raw.githubusercontent.com"), "/main/videos"])
    for fn in path.joinpath("files.txt").open().readlines():
        listfiles.append(fn.strip().replace("./videos", raw))
    path.joinpath("files.txt").open("w").write("\n".join(listfiles))
    files = list(
        fi for fi in videos.iterdir()
        if fi.suffix == ".mp4"
    )
    for file in files:
        filename = file.name
        fileid = filename.split(".mp4")[0].replace("[", "").replace("]", "")[-11:]
        size = file.stat().st_size * 1.0e-6
        content.append(dict(
            name=filename,
            id=fileid,
            size=size,
            path=str(file),
            url=f"{urlfile}/{filename}"
        ))
        totalsize += size
    return dict(
        content=content,
        total_size=totalsize,
        available_space=totalsize < 9.5e2
    )


if __name__ == "__main__":
    save_info(getfiles())
    # print(getinfo())
