import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import datetime
import fire
from src.instagrapi_utis import login_user, get_new_menu_clips
from src.clip_to_text import extract_text_from_mp4
from src.parse_video_text import parse_text_to_menu


def update_menu_md(new_menu, item_pk):
    today = datetime.datetime.today()
    today_str = today.strftime("%Y-%m-%d")
    with open("./MENU.md", "r") as f:
        lines = f.readlines()
    header_line = [lines[0]]
    old_menus_lines = lines[1:]
    new_menu_lines = [f"## New Menu, {today_str}, item_pk={item_pk}\n"] + [
        i + "\n" for i in new_menu.split("\n")
    ]
    new_lines = header_line + new_menu_lines + old_menus_lines
    with open("./MENU.md", "w") as f:
        f.writelines(new_lines)
    logger.info("updated menu.md with new menu")


def get_menus_already_processed():
    with open("./MENU.md", "r") as f:
        lines = f.readlines()
    # Parsing new_menu_lines i.e "#New Menu, <date>, item_pk=<menu_id>\n"
    menus_id = [l.split("item_pk=")[1][:-1] for l in lines if "item_pk=" in l]
    logger.info("Getting menus already processed")
    logger.debug(f"Menus already processed {menus_id}")
    return menus_id


def parse_menus():
    menu_already_processed = get_menus_already_processed()
    insta_client = login_user()
    new_clips = get_new_menu_clips(insta_client, menu_already_processed)
    for item_pk, clip_path in new_clips:
        text = extract_text_from_mp4(clip_path)
        with open(f"./data/extracted_text/{item_pk}.txt", "w") as f:
            f.write(text)
        menu = parse_text_to_menu(text)
        update_menu_md(menu, item_pk)


if __name__ == "__main__":
    fire.Fire(parse_menus)
