"""import asyncio
import os
import sys

import git

from userbot.Config import Config
from LEGENDBOT.utils import admin_cmd
from . import *
# -- Constants -- #
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)
OFFICIAL_UPSTREAM_REPO = Config.UPSTREAM_REPO
BOT_IS_UP_TO_DATE = "**The LEGENDBOT** is up-to-date sir."
NEW_BOT_UP_DATE_FOUND = (
    "new update found for {branch_name}\n"
    "changelog: \n\n{changelog}\n"
    "updating your LEGENDBOT ..."
)
NEW_UP_DATE_FOUND = "New update found for {branch_name}\n" "`updating your LEGENDBOT...`"
REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
DIFF_MARKER = "HEAD..{remote_name}/{branch_name}"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
# -- Constants End -- #


@borg.on(admin_cmd("update ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="update$", allow_sudo=True))
async def updater(message):
    try:
        repo = git.Repo()
    except git.exc.InvalidGitRepositoryError as e:
        repo = git.Repo.init()
        origin = repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(IFFUCI_ACTIVE_BRANCH_NAME, origin.refs.master)
        repo.heads.master.checkout(True)

    active_branch_name = repo.active_branch.name
    if active_branch_name != IFFUCI_ACTIVE_BRANCH_NAME:
        await message.edit(
            IS_SELECTED_DIFFERENT_BRANCH.format(branch_name=active_branch_name)
        )
        return False

    try:
        repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
    except Exception as e:
        print(e)

    temp_upstream_remote = repo.remote(REPO_REMOTE_NAME)
    temp_upstream_remote.fetch(active_branch_name)

    changelog = generate_change_log(
        repo,
        DIFF_MARKER.format(
            remote_name=REPO_REMOTE_NAME, branch_name=active_branch_name
        ),
    )

    if not changelog:
        await message.edit("`⚡𝚁𝚞𝚔𝚘 𝙹𝚊𝚛𝚊 𝚜𝚊𝚋𝚛𝚊 𝚔𝚊𝚛𝚘 𝚞𝚙𝚍𝚊𝚝𝚎 𝙷𝚘 𝚗𝚎 𝚓𝚊 𝚛𝚑𝚊 𝚑😅😅`")
        await asyncio.sleep(5)

    message_one = NEW_BOT_UP_DATE_FOUND.format(
        branch_name=active_branch_name, changelog=changelog
    )
    message_two = NEW_UP_DATE_FOUND.format(branch_name=active_branch_name)

    if len(message_one) > 4095:
        with open("change.log", "w+", encoding="utf8") as out_file:
            out_file.write(str(message_one))
        await tgbot.send_message(
            message.chat_id, document="change.log", caption=message_two
        )
        os.remove("change.log")
    else:
        await message.edit(message_one)

    temp_upstream_remote.fetch(active_branch_name)
    repo.git.reset("--hard", "FETCH_HEAD")

    if Var.HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(Var.HEROKU_API_KEY)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            if Var.HEROKU_APP_NAME is not None:
                heroku_app = None
                for i in heroku_applications:
                    if i.name == Var.HEROKU_APP_NAME:
                        heroku_app = i
                if heroku_app is None:
                    await message.edit(
                        "Invalid APP Name. Please set the name of your bot in heroku in the var `HEROKU_APP_NAME.`"
                    )
                    return
                heroku_git_url = heroku_app.git_url.replace(
                    "https://", "https://api:" + Var.HEROKU_API_KEY + "@"
                )
                if "heroku" in repo.remotes:
                    remote = repo.remote("heroku")
                    remote.set_url(heroku_git_url)
                else:
                    remote = repo.create_remote("heroku", heroku_git_url)
                asyncio.get_event_loop().create_task(
                    deploy_start(tgbot, message, HEROKU_GIT_REF_SPEC, remote)
                )

            else:
                await message.edit(
                    "Please create the var `HEROKU_APP_NAME` as the key and the name of your bot in heroku as your value."
                )
                return
        else:
            await message.edit(NO_HEROKU_APP_CFGD)
    else:
        await message.edit("No heroku api key found in `HEROKU_API_KEY` var")


def generate_change_log(git_repo, diff_marker):
    out_put_str = ""
    d_form = "%d/%m/%y"
    for repo_change in git_repo.iter_commits(diff_marker):
        out_put_str += f"•[{repo_change.committed_datetime.strftime(d_form)}]: {repo_change.summary} <{repo_change.author}>\n"
    return out_put_str


async def deploy_start(tgbot, message, refspec, remote):
    await message.edit(RESTARTING_APP)
    await message.edit(
        f"🤟✞︎t͛ẞ̸ 𝖑𝖊ɠêɳ̃dẞø✞︎ 𝙸𝚜 𝚘𝚗 𝚞𝚙𝚍𝚊𝚝𝚒𝚗𝚐 𝚝𝚘 𝚕𝚊𝚝𝚎𝚜𝚝 {LEGENDversion} !!!\n𝚊𝚏𝚝𝚎𝚛 5 𝚖𝚒𝚗 𝚝𝚢𝚙𝚎 `.op` οя `.alive` το ϲнєϲκ ιƒ ι αм οи ѕιя ♣️"
    )
    await remote.push(refspec=refspec)
    await tgbot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
  
  """






import asyncio
import os
import sys
import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from userbot.Config import Config 
from userbot.cmdhelp import CmdHelp 
from userbot.helpers import runner
from . import *


HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = "LegendBot"

UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "LegendBot"
NO_HEROKU_APP_CFGD = "No Heroku App Found!"
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/LegendBot"
RESTARTING_APP = "Restarting Heroku App..."
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"🔥 **New UPDATE available for [{ac_br}]:\n\n📑 CHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Changelog is too big, view the file to see it.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
            thumb=legend_logo1,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "✅ Successfully updated Legendẞø†!\n\nBot is restarting please wait for a minute."
    )
    args = [sys.executable, "-m", "userbot"]
    os.execle(sys.executable, *args, os.environ)
    return

@bot.on(admin_cmd(outgoing=True, pattern=r"update(| now)$"))
@bot.on(sudo_cmd(pattern="update(| now)$", allow_sudo=True))
async def upstream(event):
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "`Checking for new updates...`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await edit_or_reply(
            event, "Set  `HEROKU_APP_NAME`  and  `HEROKU_API_KEY`  to update your bot 🥴"
        )
    try:
        txt = "😕 `Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error}  not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`The directory {error} "
                "does not seem to be a git repository.\n"
                "Fix that by force updating! Using "
                "`.update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("LegendBot", origin.refs.LegendBot)
        repo.heads.master.set_tracking_branch(origin.refs.LegendBot)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            f"`Looks like you are using your own custom git branch ( {ac_br} ). "
            "Please checkout to official branch that is ( LegendBot )`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if changelog == "" and not force_update:
        await event.edit(
            "\n**😎 Legendẞø† is UP-TO-DATE.**"
            f"\n\n**Version :**  {LEGENDVersion}"
            f"\n**Owner :**  {legend_mention}"
            f"\n**Git Branch :**  {UPSTREAM_REPO_BRANCH}\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond("🌚 Do `.update build` to update your **Legendẞø†** !!")

    if force_update:
        await event.edit(
            "`Force-Updating Legendẞø†. Please wait...`"
        )
    if conf == "now":
        await event.edit("`Update In Progress! Please Wait....`")
        await update(event, repo, ups_rem, ac_br)
    return


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "**Please set up**  `HEROKU_APP_NAME`  **to update!"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n" "`Invalid Heroku vars for updating."
            )
            return repo.__del__()
        await event.edit(
            "`Updating Userbot In Progress...Please wait upto 5 minutes.`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n**Error log:**\n`{error}`")
            return repo.__del__()
        build_status = app.builds(order_by="created_at", sort="desc")[0]
        if build_status.status == "failed":
            await event.edit(
                "`Build failed ⚠️`"
            )
            await asyncio.sleep(5)
            return await event.delete()
        await event.edit(f"**Your Legendßø† Is UpToDate**\n\n**Version :**  __{hell_ver}__\n**Oɯɳҽɾ :**  {hell_mention}")
    else:
        await event.edit("**Please set up**  `HEROKU_API_KEY`  **from heroku to update!**")
    return


@bot.on(legend_cmd(outgoing=True, pattern=r"update build$"))
@bot.on(sudo_cmd(pattern="update build$", allow_sudo=True))
async def upstream(event):
    event = await edit_or_reply(event, "`Hard-Update In Progress... \nPlease wait until docker build is finished...`")
    off_repo = "https://github.com/LEGEND-OS/LEGENDBOT"
    os.chdir("/app")
    git_hell = f"rm -rf .git"
    try:
        await runner.runcmd(git_hell)
    except BaseException:
        pass
    try:
        txt = "😕 `Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error}  not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("LegendBot", origin.refs.LegendBot)
        repo.heads.master.set_tracking_branch(origin.refs.LegendBot)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit(f"**Legendẞø† Docker Build In Progress... Type** `{hl}ping`  **after 5 mins to check if Bot is working!**")
    await deploy(event, repo, ups_rem, ac_br, txt)


CmdHelp("update").add_command(
  "update", None, "Checks if any new update is available."
).add_command(
  "update now", None, "Soft-Update Your Legendẞø†. Basically if you restart dyno it will go back to previous deploy."
).add_command(
  "update build", None, "Hard-Update Your Legendẞø†. This won't take you back to your previous deploy. This will be triggered even if there is no changelog."
).add_info(
  "Hêllẞø† Updater."
).add_warning(
  "✅ Harmless Module."
).add()
