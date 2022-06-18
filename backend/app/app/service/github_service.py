#!/usr/bin/env python3
# coding=utf-8
# *******************************************************************
# ***  ***
# * Author:
#   Shaik Saddam Hussain Basha <sk.saddam007>
# *******************************************************************

# Modules
import json
import os
try:
    import queue
except ImportError:
    import Queue as queue
import threading
import time

import git
import requests
from sys import exit
from concurrent.futures import ProcessPoolExecutor
from functools import partial



class getReposURLs:
    def __init__(self, api_prefix, exclude_repos=None):
        self.user_agent = "Github Cloner Agent"
        self.headers = {'User-Agent': self.user_agent, 'Accept': '*/*'}
        self.timeout = 30
        self.api_prefix = api_prefix
        self.excluded_repos_list = [] if exclude_repos is None else\
            exclude_repos

    def filter_excluded_repos(self, url):
        '''
        True only if the url doesn't contain any string from
        `self.excluded_repos_list`
        '''
        return not any((excluded_repo in url
                        for excluded_repo in self.excluded_repos_list))

    def append_response(self, URLs, resp, key, exclude_forked=False):
        '''Append the urls from response from a given criteria'''
        for i, _ in enumerate(resp):
            if exclude_forked and resp[i]['fork']:
                continue
            resp_i_key = resp[i][key]
            if self.filter_excluded_repos(resp_i_key):
                URLs.append(resp_i_key)

    def UserGists(self, user, username=None, token=None):
        """
        Returns a list of GIT URLs for accessible gists.
        Input:-
        user: Github user.
        Optional Input:-
        username: Github username.
        token: Github token or password.
        Output:-
        a list of Github gist repositories URLs.
        """

        URLs = []
        resp = []
        current_page = 1
        while (len(resp) != 0 or current_page == 1):
            API = "{0}/users/{1}/gists?page={2}".format(
                self.api_prefix, user, current_page)
            if (username or token) is None:
                resp = requests.get(API, headers=self.headers,
                                    timeout=self.timeout).text
            else:
                resp = requests.get(
                    API, headers=self.headers,
                    timeout=self.timeout,
                    auth=(username, token)).text
            resp = json.loads(resp)

            if self.checkResponse(resp) != 0:
                return []

            self.append_response(URLs, resp, "git_pull_url")
            current_page += 1
        return URLs

    def AuthenticatedGists(self, username, token):
        """
        Returns a list of gists of an authenticated user.
        Input:-
        username: Github username.
        token: Github token or password.
        Output:-
        a list of Github gist repositories URLs.
        """

        URLs = []
        resp = []
        current_page = 1
        while (len(resp) != 0 or current_page == 1):
            API = "{0}/gists?page={1}".format(self.api_prefix, current_page)
            resp = requests.get(API,
                                headers=self.headers,
                                timeout=self.timeout,
                                auth=(username, token)).text
            resp = json.loads(resp)
            self.append_response(URLs, resp, "git_pull_url")
            current_page += 1

        return URLs

    def fromUser(self, user, username=None, token=None, include_gists=False, exclude_forked=False):
        """
        Retrieves a list of repositories for a Github user.
        Input:-
        user: Github username.
        Optional Input:-
        username: Github username.
        token: Github token or password.
        Output:-
        a list of Github repositories URLs.
        """

        URLs = []
        resp = []
        current_page = 1
        while (len(resp) != 0 or current_page == 1):
            API = "{0}/users/{1}/repos?per_page=40000000&page={2}".format(
                self.api_prefix, user, current_page)

            if (username or token) is None:
                resp = requests.get(API, headers=self.headers,
                                    timeout=self.timeout).text
            else:
                resp = requests.get(
                    API,
                    headers=self.headers,
                    timeout=self.timeout,
                    auth=(username, token)).text
            resp = json.loads(resp)

            if self.checkResponse(resp) != 0:
                return []

            self.append_response(URLs, resp, "git_url", exclude_forked)

            if include_gists is True:
                URLs.extend(self.UserGists(
                    user, username=username, token=token))
            current_page += 1
        return URLs

    def fromOrg(self, org_name, username=None, token=None, exclude_forked=False):
        """
        Retrieves a list of repositories for a Github organization.
        Input:-
        org_name: Github organization name.
        Optional Input:-
        username: Github username.
        token: Github token or password.
        Output:-
        a list of Github repositories URLs.
        """

        URLs = []
        resp = []
        current_page = 1
        while (len(resp) != 0 or current_page == 1):
            API = "{0}/orgs/{1}/repos?per_page=40000000&page={2}".format(
                self.api_prefix, org_name, current_page)
            if (username or token) is None:
                resp = requests.get(API, headers=self.headers,
                                    timeout=self.timeout).text
            else:
                resp = requests.get(
                    API,
                    headers=self.headers,
                    timeout=self.timeout,
                    auth=(username, token)).text
            resp = json.loads(resp)

            if self.checkResponse(resp) != 0:
                return []

            self.append_response(URLs, resp, "git_url", exclude_forked)
            current_page += 1
        return URLs

    def fromOrgIncludeUsers(self,
                            org_name,
                            username=None,
                            token=None,
                            include_gists=False,
                            exclude_forked=False):
        """
        Retrieves a list of repositories for a Github organization
        and repositories of the Github organization's members.
        Input:-
        org_name: Github organization name.
        Optional Input:-
        username: Github username.
        token: Github token or password.
        Output:-
        a list of Github repositories URLs.
        """

        URLs = []
        members = []
        resp = []
        current_page = 1
        URLs.extend(self.fromOrg(org_name, username=username, token=token))

        while (len(resp) != 0 or current_page == 1):
            API = "{0}/orgs/{1}/members?per_page=40000000&page={2}".format(
                self.api_prefix, org_name, current_page)
            if (username or token) is None:
                resp = requests.get(API,
                                    headers=self.headers,
                                    timeout=self.timeout).text
            else:
                resp = requests.get(API,
                                    headers=self.headers,
                                    timeout=self.timeout,
                                    auth=(username, token)).text
            resp = json.loads(resp)

            if self.checkResponse(resp) != 0:
                return []

            current_page += 1
            for i in range(len(resp)):
                members.append(resp[i]["login"])

        for member in members:
            URLs.extend(self.fromUser(member,
                                      username=username,
                                      token=token,
                                      include_gists=include_gists))

        return URLs

    def checkAuthentication(self, username, token):
        """
        Checks whether an authentication credentials are valid or not.
        Input:-
        username: Github username.
        token: Github token or password.
        Output:-
        True: if the authentication credentials are valid.
        False: if the authentication credentials are invalid.
        """

        API = "{0}/user".format(self.api_prefix)
        resp = requests.get(API,
                            auth=(username, token),
                            timeout=self.timeout,
                            headers=self.headers)
        return resp.status_code == 200

    def checkResponse(self, response):
        """
        Validates whether there an error in the response.
        """
        try:
            if "API rate limit exceeded" in response["message"]:
                print('[!] Error: Github API rate limit exceeded')
                return 1
        except TypeError:
            pass

        try:
            if (response["message"] == "Not Found"):
                return 2  # The organization does not exist
        except TypeError:
            pass

        return 0

    def fromAuthenticatedUser(self, username, token, exclude_forked):
        """
        Retrieves a list of Github repositories than an authenticated user
        has access to.
        Input:-
        username: Github username.
        token: Github token or password.
        Output:-
        a list of Github repositories URLs.
        """
        URLs = []
        resp = []
        current_page = 1

        while (len(resp) != 0 or current_page == 1):
            API = "{0}/user/repos?per_page=40000000&type=all&page={1}".format(
                self.api_prefix, current_page)
            resp = requests.get(API,
                                headers=self.headers,
                                timeout=self.timeout,
                                auth=(username, token)).text
            resp = json.loads(resp)

            self.append_response(URLs, resp, "git_url", exclude_forked)
            current_page += 1
        return URLs


def parseGitURL(URL, username=None, token=None):
    """
    This function parses the GIT URL.
    """

    URL = URL.replace("git://", "https://")
    if (username or token) is not None:
        URL = URL.replace(
            "https://", "https://{0}:{1}@".format(username, token))
    return URL


def get_repopath(repo_username, repo_name, prefix_mode):
    """
    Returns a string of the repo path.
    """
    if prefix_mode == "none":
        repopath = repo_name
    elif prefix_mode == "underscore":
        repopath = repo_username + "_" + repo_name
    elif prefix_mode == "directory":
        repopath = repo_username + "/" + repo_name
    return repopath


def cloneRepo(URL,
              cloningpath,
              username=None,
              token=None,
              prefix_mode="underscore"):
    """
    Clones a single GIT repository.
    Input:-
    URL: GIT repository URL.
    cloningPath: the directory that the repository will be cloned at.
    Optional Input:-
    username: Github username.
    token: Github token or password.
    """

    try:
        try:
            if not os.path.exists(cloningpath):
                os.mkdir(cloningpath)
            if prefix_mode == "directory":
                repo_username = URL.split("/")[-2]
                if not os.path.exists(cloningpath + "/" + repo_username):
                    os.mkdir(cloningpath + "/" + repo_username)
        except Exception:
            print("Error: There is an error in creating directories")

        print(f'the args we got URL = {URL}, cloningpath = {cloningpath}, username = {username}, token = {token}, prefix_mode = {prefix_mode}')
        URL = parseGitURL(URL, username=username, token=token)

        repo_username = URL.split("/")[-2]
        repo_name = URL.split("/")[-1]

        repopath = get_repopath(repo_username, repo_name, prefix_mode)

        if repopath.endswith(".git"):
            repopath = repopath[:-4]

        if '@' in repopath:
            repopath = repopath.replace(repopath[:repopath.index("@") + 1], "")

        fullpath = cloningpath + "/" + repopath
        with threading.Lock():
            print(fullpath)

        if os.path.exists(fullpath):
            git.Repo(fullpath).remote().pull()
        else:
            git.Repo.clone_from(URL, fullpath)
    except Exception as e:
        print(e)
        print("Error: There was an error in cloning [{}]".format(URL))


def cloneBulkRepos(URLs,
                   cloningPath,
                   threads_limit=5,
                   username=None,
                   token=None,
                   prefix_mode="underscore"):
    """
    Clones a bulk of GIT repositories.
    Input:-
    URLs: A list of GIT repository URLs.
    cloningPath: the directory that the repository will be cloned at.
    Optional Input:-
    threads_limit: The limit of working threads.
    username: Github username.
    token: Github token or password.
    """
    ts = time.time()
    Q = queue.Queue()
    threads_state = []
    for URL in URLs:
        Q.put(URL)
    while Q.empty() is False:
        if threading.active_count() < (threads_limit + 1):
            t = threading.Thread(target=cloneRepo, args=(Q.get(), cloningPath,),
                                 kwargs={"username": username,
                                         "token": token,
                                         "prefix_mode": prefix_mode})
            t.daemon = True
            t.start()
        else:
            time.sleep(0.5)

            threads_state.append(t)
    for _ in threads_state:
        _.join()
    print(f'Thread Took {time.time() - ts} seconds')



def cloneBulkReposProcess(URLs,
                   cloningPath,
                   username=None,
                   token=None,
                   prefix_mode="underscore"):
    """
    Clones a bulk of GIT repositories.
    Input:-
    URLs: A list of GIT repository URLs.
    cloningPath: the directory that the repository will be cloned at.
    Optional Input:-
    username: Github username.
    token: Github token or password.
    """
    ts = time.time()
    repoclone_args = partial(cloneRepo, cloningpath=cloningPath, username=username, token=token, prefix_mode=prefix_mode)
    with ProcessPoolExecutor() as executor:
        executor.map(repoclone_args, URLs)
    print(f'Process Took {time.time() - ts} seconds')


def git_actions(users=None, organizations=None, include_organization_members=False,output_path='/Users/zakirhussainbashask/Documents/learning/blue_avenir_test/repos', threads_limit=5, authentication=None, include_authenticated_repos=False, include_gists=False, echo_urls=True, prefix_mode='underscore', api_prefix='https://api.github.com', exclude_repos=[], exclude_forked=True, use_threading=False, use_process=False):
    """
    starting of git clone process
    """
    if threads_limit > 10:
        print("Error: Using more than 10 threads may cause errors."
              "\nDecrease the amount of used threads.")
        print("\nExiting....")
        return

    if (not output_path) and (not echo_urls):
        print("Error: The output path is not specified.")
        print("\nExiting...")
        return

    if not (users or organizations):
        print("Error: Both Github users and Github organizations are not specified.")
        print("\nExiting...")
        return

    if str.isdigit(str(threads_limit)) is False:
        print("Error: Specified threads specified is invalid.")
        print("\nExiting...")
        return

    if not echo_urls:
        try:
            if not os.path.exists(output_path):
                os.mkdir(output_path)
        except Exception as error:
            print("Error: There is an error creating output directory.")
            print(repr(error))
            return

    if authentication is not None:
        if ':' not in authentication:
            print('[!] Error: Incorrect authentication value, must be:'
                  ' <username>:<password_or_personal_access_token>')
            print('\nExiting...')
            return
        if getReposURLs(api_prefix,
                        exclude_repos).checkAuthentication(
                            authentication.split(":")[0],
                            authentication.split(":")[1]) is False:
            print("Error: authentication failed.")
            print("\nExiting...")
            return
        else:
            username = authentication.split(":")[0]
            token = authentication.split(":")[1]
    else:
        username = None
        token = None

    if (include_authenticated_repos is True) and (authentication is None):
        print("Error: --include-authenticated-repos is used and --authentication is not provided.")
        print("\nExiting...")
        return

    if prefix_mode not in ["none", "underscore", "directory"]:
        print("Error: prefix_mode must be one of: \"none\", \"underscore\", \"directory\".")
        print("\nExiting...")
        return

    URLs = []

    if include_authenticated_repos is True:
        URLs.extend(getReposURLs(
            api_prefix, exclude_repos).fromAuthenticatedUser(username, token, exclude_forked))
        if include_gists is True:
            URLs.extend(getReposURLs(
                api_prefix, exclude_repos).AuthenticatedGists(username, token))

    if users is not None:
        for user in users:
            URLs.extend(getReposURLs(api_prefix, exclude_repos).fromUser(
                user,
                username=username,
                token=token,
                include_gists=include_gists,
                exclude_forked=exclude_forked))

    if organizations is not None:

        for organization in organizations:
            if include_organization_members is False:
                URLs.extend(getReposURLs(api_prefix, exclude_repos).fromOrg(
                    organization,
                    username=username,
                    token=token,
                    exclude_forked=exclude_forked))
            else:
                URLs.extend(getReposURLs(api_prefix,
                                         exclude_repos).fromOrgIncludeUsers(
                    organization,
                    username=username,
                    token=token,
                    include_gists=include_gists,
                    exclude_forked=exclude_forked))

    URLs = list(set(URLs))
    if echo_urls is True:
        for URL in URLs:
            print(parseGitURL(URL, username=username, token=token))
        return "no model", [i for i in URLs]
    if use_threading:
        cloneBulkRepos(URLs, output_path+'/threads', threads_limit=threads_limit, 
            username=username, token=token, prefix_mode=prefix_mode)
        return "threaded", set(URLs)
    if use_process:
        cloneBulkReposProcess(URLs, output_path+'/process', 
            username=username, token=token, prefix_mode=prefix_mode)
        return "process", set(URLs)
    return "none", set(URLs)
