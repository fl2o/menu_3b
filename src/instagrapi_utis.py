from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import json
import tempfile
import logging

logger = logging.getLogger()


def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    if os.path.exists("./session.json"):
        session = cl.load_settings("session.json")
    elif os.environ.get("INSTAGRAM_SESSION"):
        with tempfile.NamedTemporaryFile(delete=True, mode="w") as tmp:
            session = json.dump(json.loads(os.environ["INSTAGRAM_SESSION"]), tmp)
            tmp.flush()
            session = cl.load_settings(tmp.name)
    else:
        session = None

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(os.environ["INSTAGRAM_USERNAME"], os.environ["INSTAGRAM_PASSWORD"])

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info(
                    "Session is invalid, need to login via username and password"
                )

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(
                    os.environ["INSTAGRAM_USERNAME"], os.environ["INSTAGRAM_PASSWORD"]
                )
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info(
                "Attempting to login via username and password. username: %s"
                % os.environ["INSTAGRAM_USERNAME"]
            )
            if cl.login(
                os.environ["INSTAGRAM_USERNAME"], os.environ["INSTAGRAM_PASSWORD"]
            ):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    cl.delay_range = [1, 3]
    return cl


def get_menu_highlight(client: Client):
    menu_highlight_title = "🍽"
    restaurant_id = "5526391192"
    highlights = client.user_highlights(restaurant_id)
    try:
        menu_highlight = next(
            highlight
            for highlight in highlights
            if highlight.title == menu_highlight_title
        )
        logger.info("Found the highlight for the menu")
    except StopIteration:
        logger.exception("Couldnt find the highlight for the menu")
    return menu_highlight


def get_new_menu_clips(client: Client, menu_already_processed=[]) -> list[int, str]:
    menu_highlight = get_menu_highlight(client)
    menu_highlight_infos = client.highlight_info(menu_highlight.pk)
    new_menu_clips = []
    for item in menu_highlight_infos.items:
        menu_id = item.pk
        dest_path = f"./data/clips/{menu_id}.mp4"
        if menu_id not in menu_already_processed:
            client.story_download_by_url(item.video_url, dest_path[:-4])
            new_menu_clips.append((menu_id, dest_path))
            logger.info(f"Found new menu, item_pk={menu_id}")
    return new_menu_clips
