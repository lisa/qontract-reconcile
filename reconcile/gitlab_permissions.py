import itertools
import logging
from typing import Any

from sretoolbox.utils import threaded

from reconcile import queries
from reconcile.utils import batches
from reconcile.utils.defer import defer
from reconcile.utils.gitlab_api import GitLabApi

QONTRACT_INTEGRATION = "gitlab-permissions"
PAGE_SIZE = 100


def get_members_to_add(repo, gl, app_sre):
    maintainers = get_all_app_sre_maintainers(repo, gl, app_sre)
    if maintainers is None:
        return []
    if gl.user.username not in maintainers:
        logging.error(
            "'{}' is not shared with {} as 'Maintainer'".format(repo, gl.user.username)
        )
        return []
    members_to_add = [
        {"user": u, "repo": repo} for u in app_sre if u.username not in maintainers
    ]
    return members_to_add


def get_all_app_sre_maintainers(repo, gl, app_sre):
    app_sre_user_ids = [user.id for user in app_sre]
    chunks = batches.batched(app_sre_user_ids, PAGE_SIZE)
    app_sre_maintainers = (
        gl.get_project_maintainers(repo, query=create_user_ids_query(chunk))
        for chunk in chunks
    )
    return list(itertools.chain.from_iterable(app_sre_maintainers))


def create_user_ids_query(ids):
    return {"user_ids": ",".join(str(id) for id in ids)}


@defer
def run(dry_run, thread_pool_size=10, defer=None):
    instance = queries.get_gitlab_instance()
    settings = queries.get_app_interface_settings()
    gl = GitLabApi(instance, settings=settings)
    if defer:
        defer(gl.cleanup)
    repos = queries.get_repos(server=gl.server, exclude_manage_permissions=True)
    app_sre = gl.get_app_sre_group_users()
    results = threaded.run(
        get_members_to_add, repos, thread_pool_size, gl=gl, app_sre=app_sre
    )
    members_to_add = list(itertools.chain.from_iterable(results))
    for m in members_to_add:
        logging.info(["add_maintainer", m["repo"], m["user"].username])
        if not dry_run:
            gl.add_project_member(m["repo"], m["user"])


def early_exit_desired_state(*args, **kwargs) -> dict[str, Any]:
    instance = queries.get_gitlab_instance()
    return {
        "instance": instance,
        "repos": queries.get_repos(server=instance["url"]),
    }
