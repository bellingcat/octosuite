import os
import csv
import logging
from rich import print as xprint
from octosuite.log_roller import prompt_log_csv, logged_to_csv
from octosuite.message_prefixes import PROMPT, WARNING, POSITIVE, NEGATIVE, INFO


# csv_loggers.py
# This file holds the functions for creating .csv files of each functionality in main
def log_org_profile(response):
    org_profile_fields = ['Profile photo', 'Name', 'Username', 'ID', 'Node ID', 'Email', 'About', 'Location', 'Blog',
                          'Followers', 'Following', 'Twitter handle', 'Gists', 'Repositories', 'Account type',
                          'Is verified?', 'Has organization projects?', 'Has repository projects?', 'Created at',
                          'Updated at']
    org_profile_row = [response.json()['avatar_url'], response.json()['name'], response.json()['login'],
                       response.json()['id'], response.json()['node_id'], response.json()['email'],
                       response.json()['description'], response.json()['location'], response.json()['blog'],
                       response.json()['followers'], response.json()['following'], response.json()['twitter_username'],
                       response.json()['public_gists'], response.json()['public_repos'], response.json()['type'],
                       response.json()['is_verified'], response.json()['has_organization_projects'],
                       response.json()['has_repository_projects'], response.json()['created_at'],
                       response.json()['updated_at']]
    
    with open(os.path.join("output", f"{response.json()['name']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(org_profile_fields)
        write_csv.writerow(org_profile_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Creating a .csv file of a user' profile
def log_user_profile(response):
    user_profile_fields = ['Profile photo', 'Name', 'Username', 'ID', 'Node ID', 'Bio', 'Blog', 'Location', 'Followers',
                           'Following', 'Twitter handle', 'Gists', 'Repositories', 'Organization', 'Is hireable?',
                           'Is site admin?', 'Joined at', 'Updated at']
    user_profile_row = [response.json()['avatar_url'], response.json()['name'], response.json()['login'],
                        response.json()['id'], response.json()['node_id'], response.json()['bio'],
                        response.json()['blog'], response.json()['location'], response.json()['followers'],
                        response.json()['following'], response.json()['twitter_username'],
                        response.json()['public_gists'], response.json()['public_repos'], response.json()['company'],
                        response.json()['hireable'], response.json()['site_admin'], response.json()['created_at'],
                        response.json()['updated_at']]
    
    with open(os.path.join("output", f"{response.json()['login']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_profile_fields)
        write_csv.writerow(user_profile_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")


# create .csv for repository profile
def log_repo_profile(response):
    repo_profile_fields = ['Name', 'ID', 'About', 'Forks', 'Stars', 'Watchers', 'License', 'Branch', 'Visibility',
                           'Language(s)', 'Open issues', 'Topics', 'Homepage', 'Clone URL', 'SSH URL', 'Is fork?',
                           'Is forkable?', 'Is private?', 'Is archived?', 'Is template?', 'Has wiki?', 'Has pages?',
                           'Has projects?', 'Has issues?', 'Has downloads?', 'Pushed at', 'Created at', 'Updated at']
    repo_profile_row = [response.json()['name'], response.json()['id'], response.json()['description'],
                        response.json()['forks'], response.json()['stargazers_count'], response.json()['watchers'],
                        response.json()['license'], response.json()['default_branch'], response.json()['visibility'],
                        response.json()['language'], response.json()['open_issues'], response.json()['topics'],
                        response.json()['homepage'], response.json()['clone_url'], response.json()['ssh_url'],
                        response.json()['fork'], response.json()['allow_forking'], response.json()['private'],
                        response.json()['archived'], response.json()['is_template'], response.json()['has_wiki'],
                        response.json()['has_pages'], response.json()['has_projects'], response.json()['has_issues'],
                        response.json()['has_downloads'], response.json()['pushed_at'], response.json()['created_at'],
                        response.json()['updated_at']]
    
    with open(os.path.join("output", f"{response.json()['name']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(repo_profile_fields)
        write_csv.writerow(repo_profile_row)
            
        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")
    

# create .csv for repository path contents
def log_repo_path_contents(content, repo_name):
    path_content_fields = ['Filename', 'Size (bytes)', 'Type', 'Path', 'SHA', 'URL']
    path_content_row = [content['name'], content['size'], content['type'], content['path'], content['sha'],
                        content['html_url']]
    
    with open(os.path.join("output", f"{content['name']}_content_from_{repo_name}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(path_content_fields)
        write_csv.writerow(path_content_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# create .csv for repository stargazer
def log_repo_stargazers(stargazer, repo_name):
    user_follower_fields = ['Profile photo', 'Username', 'ID', 'Node ID', 'Gravatar ID', 'Account type',
                            'Is site admin?', 'URL']
    user_follower_row = [stargazer['avatar_url'], stargazer['login'], stargazer['id'], stargazer['node_id'],
                         stargazer['gravatar_id'], stargazer['type'], stargazer['site_admin'], stargazer['html_url']]
    
    with open(os.path.join("output", f"{stargazer['login']}_stargazer_of_{repo_name}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_follower_fields)
        write_csv.writerow(user_follower_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

 # create .csv for repository forks
def log_repo_forks(fork, count):
    repo_fork_fields = ['Name', 'ID', 'About', 'Forks', 'Stars', 'Watchers', 'License', 'Branch', 'Visibility',
                        'Language(s)', 'Open issues', 'Topics', 'Homepage', 'Clone URL', 'SSH URL', 'Is fork?',
                        'Is forkable?', 'Is private?', 'Is archived?', 'Is template?', 'Has wiki?', 'Has pages?',
                        'Has projects?', 'Has issues?', 'Has downloads?', 'Pushed at', 'Created at', 'Updated at']
    repo_fork_row = [fork['full_name'], fork['id'], fork['description'], fork['forks'], fork['stargazers_count'],
                     fork['watchers'], fork['license'], fork['default_branch'], fork['visibility'], fork['language'],
                     fork['open_issues'], fork['topics'], fork['homepage'], fork['clone_url'], fork['ssh_url'],
                     fork['fork'], fork['allow_forking'], fork['private'], fork['archived'], fork['is_template'],
                     fork['has_wiki'], fork['has_pages'], fork['has_projects'], fork['has_issues'],
                     fork['has_downloads'], fork['pushed_at'], fork['created_at'], fork['updated_at']]
    
    with open(os.path.join("output", f"{fork['name']}_fork_{count}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(repo_fork_fields)
        write_csv.writerow(repo_fork_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# create .csv for repository issues
def log_repo_issues(issue, repo_name):
    repo_issue_fields = ['Title', 'ID', 'Node ID', 'Number', 'State', 'Reactions', 'Comments', 'Milestone', 'Assignee',
                         'Assignees', 'Author association', 'Labels', 'Is locked?', 'Lock reason', 'Closed at',
                         'Created at', 'Updated at']
    repo_issue_row = [issue['title'], issue['id'], issue['node_id'], issue['number'], issue['state'],
                      issue['reactions'], issue['comments'], issue['milestone'], issue['assignee'], issue['assignees'],
                      issue['author_association'], issue['labels'], issue['locked'], issue['active_lock_reason'],
                      issue['closed_at'], issue['created_at'], issue['updated_at']]
    
    with open(os.path.join("output", f"{repo_name}_issue_{issue['id']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(repo_issue_fields)
        write_csv.writerow(repo_issue_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# create .csv for repository releases
def log_repo_releases(release, repo_name):
    repo_release_fields = ['Name', 'ID', 'Node ID', 'Tag', 'Branch', 'Assets', 'Is draft?', 'Is prerelease?',
                           'Created at', 'Published at']
    repo_release_row = [release['name'], release['id'], release['node_id'], release['tag_name'],
                        release['target_commitish'], release['assets'], release['draft'], release['prerelease'],
                        release['created_at'], release['published_at']]
    
    with open(os.path.join("output", f"{repo_name}_release_{release['name']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(repo_release_fields)
        write_csv.writerow(repo_release_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Create .csv file for repository contributors
def log_repo_contributors(contributor, repo_name):
    repo_contributor_fields = ['Profile photo', 'Username', 'ID', 'Node ID', 'Gravatar ID', 'Account type',
                               'Is site admin?', 'URL']
    repo_contributor_row = [contributor['avatar_url'], contributor['login'], contributor['id'], contributor['node_id'],
                            contributor['gravatar_id'], contributor['type'], contributor['site_admin'],
                            contributor['html_url']]
    
    with open(os.path.join("output", f"{contributor['login']}_contributor_of_{repo_name}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(repo_contributor_fields)
        write_csv.writerow(repo_contributor_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

   
# Create .csv for organization' events
def log_repo_events(event, organization):
    org_event_fields = ['ID', 'Type', 'Created at', 'Payload']
    org_event_row = [event['id'], event['type'], event['created_at'], event['payload']]
    
    with open(os.path.join("output", f"{organization}_event_{event['id']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(org_event_fields)
        write_csv.writerow(org_event_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Create .csv for organization' repositories
def log_org_repos(repository, organization):
    org_repo_fields = ['Name', 'ID', 'About', 'Forks', 'Stars', 'Watchers', 'License', 'Branch', 'Visibility',
                       'Language(s)', 'Open issues', 'Topics', 'Homepage', 'Clone URL', 'SSH URL', 'Is fork?',
                       'Is forkable?', 'Is private?', 'Is archived?', 'Is template?', 'Has wiki?', 'Has pages?',
                       'Has projects?', 'Has issues?', 'Has downloads?', 'Pushed at', 'Created at', 'Updated at']
    org_repo_row = [repository['full_name'], repository['id'], repository['description'], repository['forks'],
                    repository['stargazers_count'], repository['watchers'], repository['license'],
                    repository['default_branch'], repository['visibility'], repository['language'],
                    repository['open_issues'], repository['topics'], repository['homepage'], repository['clone_url'],
                    repository['ssh_url'], repository['fork'], repository['allow_forking'], repository['private'],
                    repository['archived'], repository['is_template'], repository['has_wiki'], repository['has_pages'],
                    repository['has_projects'], repository['has_issues'], repository['has_downloads'],
                    repository['pushed_at'], repository['created_at'], repository['updated_at']]
    
    with open(os.path.join("output", f"{repository['name']}_repository_of_{organization}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(org_repo_fields)
        write_csv.writerow(org_repo_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# .csv for user' repositories
def log_user_repos(repository, username):
    user_repo_fields = ['Name', 'ID', 'About', 'Forks', 'Stars', 'Watchers', 'License', 'Branch', 'Visibility',
                        'Language(s)', 'Open issues', 'Topics', 'Homepage', 'Clone URL', 'SSH URL', 'Is fork?',
                        'Is forkable?', 'Is private?', 'Is archived?', 'Is template?', 'Has wiki?', 'Has pages?',
                        'Has projects?', 'Has issues?', 'Has downloads?', 'Pushed at', 'Created at', 'Updated at']
    user_repo_row = [repository['full_name'], repository['id'], repository['description'], repository['forks'],
                     repository['stargazers_count'], repository['watchers'], repository['license'],
                     repository['default_branch'], repository['visibility'], repository['language'],
                     repository['open_issues'], repository['topics'], repository['homepage'], repository['clone_url'],
                     repository['ssh_url'], repository['fork'], repository['allow_forking'], repository['private'],
                     repository['archived'], repository['is_template'], repository['has_wiki'], repository['has_pages'],
                     repository['has_projects'], repository['has_issues'], repository['has_downloads'],
                     repository['pushed_at'], repository['created_at'], repository['updated_at']]
    
    with open(os.path.join("output", f"{repository['name']}_{username}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_repo_fields)
        write_csv.writerow(user_repo_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# .csv for user events        
def log_user_events(event):
    user_event_fields = ['Actor', 'Type', 'Repository', 'Created at', 'Payload']
    user_event_row = [event['actor']['login'], event['type'], event['repo']['name'], event['created_at'],
                      event['payload']]
    
    with open(os.path.join("output", f"{event['actor']['login']}_event_{event['id']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_event_fields)
        write_csv.writerow(user_event_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# .csv for user gists        
def log_user_gists(gist):
    user_gist_fields = ['ID', 'Node ID', 'About', 'Comments', 'Files', 'Git Push URL', 'Is public?', 'Is truncated?',
                        'Updated at']
    user_gist_row = [gist['id'], gist['node_id'], gist['description'], gist['comments'], gist['files'],
                     gist['git_push_url'], gist['public'], gist['truncated'], gist['updated_at']]
    
    with open(os.path.join("output", f"{gist['id']}_gists_{gist['owner']['login']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_gist_fields)
        write_csv.writerow(user_gist_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# .csv for user followers
def log_user_followers(follower, username):
    user_follower_fields = ['Profile photo', 'Username', 'ID', 'Node ID', 'Gravatar ID', 'Account type',
                            'Is site admin?', 'URL']
    user_follower_row = [follower['avatar_url'], follower['login'], follower['id'], follower['node_id'],
                         follower['gravatar_id'], follower['type'], follower['site_admin'], follower['html_url']]
    
    with open(f"output/{follower['login']}_follower_of_{username}.csv", 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_follower_fields)
        write_csv.writerow(user_follower_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# .csv for user following
def log_user_following(user, username):
    user_following_fields = ['Profile photo', 'Username', 'ID', 'Node ID', 'Gravatar ID', 'Account type',
                             'Is site admin?', 'URL']
    user_following_row = [user['avatar_url'], user['login'], user['id'], user['node_id'], user['gravatar_id'],
                          user['type'], user['site_admin'], user['html_url']]
    
    with open(os.path.join("output", f"{user['login']}_followed_by_{username}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_following_fields)
        write_csv.writerow(user_following_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# .csv for user' subscriptions        
def log_user_subscriptions(repository, username):
    user_subscription_fields = ['Name', 'ID', 'About', 'Forks', 'Stars', 'Watchers', 'License', 'Branch', 'Visibility',
                                'Language(s)', 'Open issues', 'Topics', 'Homepage', 'Clone URL', 'SSH URL', 'Is fork?',
                                'Is forkable?', 'Is private?', 'Is archived?', 'Is template?', 'Has wiki?',
                                'Has pages?', 'Has projects?', 'Has issues?', 'Has downloads?', 'Pushed at',
                                'Created at', 'Updated at']
    user_subscription_row = [repository['name'], repository['id'], repository['description'], repository['forks'],
                             repository['stargazers_count'], repository['watchers'], repository['license'],
                             repository['default_branch'], repository['visibility'], repository['language'],
                             repository['open_issues'], repository['topics'], repository['homepage'],
                             repository['clone_url'], repository['ssh_url'], repository['fork'],
                             repository['allow_forking'], repository['private'], repository['archived'],
                             repository['is_template'], repository['has_wiki'], repository['has_pages'],
                             repository['has_projects'], repository['has_issues'], repository['has_downloads'],
                             repository['pushed_at'], repository['created_at'], repository['updated_at']]
    
    with open(os.path.join("output", f"{username}_subscriptions_{repository['name']}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_subscription_fields)
        write_csv.writerow(user_subscription_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# .csv for user organizations
def log_user_orgs(organization, username):
    user_org_fields = ['Profile photo', 'Name', 'ID', 'Node ID', 'URL', 'About']
    user_org_row = [organization['avatar_url'], organization['login'], organization['id'], organization['node_id'],
                    organization['url'], organization['description']]
    
    with open(os.path.join("output", f"{organization['login']}_{username}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_org_fields)
        write_csv.writerow(user_org_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Create .csv for user search
def log_users_search(user, query):
    user_search_fields = ['Profile photo', 'Username', 'ID', 'Node ID', 'Gravatar ID', 'Account type', 'Is site admin?',
                          'URL']
    user_search_row = [user['avatar_url'], user['login'], user['id'], user['node_id'], user['gravatar_id'],
                       user['type'], user['site_admin'], user['html_url']]
    
    with open(os.path.join("output", f"{user['login']}_user_search_result_for_{query}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(user_search_fields)
        write_csv.writerow(user_search_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Create .csv for repository search
def log_repos_search(repository, query):
    repo_search_fields = ['Name', 'ID', 'About', 'Forks', 'Stars', 'Watchers', 'License', 'Branch', 'Visibility',
                          'Language(s)', 'Open issues', 'Topics', 'Homepage', 'Clone URL', 'SSH URL', 'Is fork?',
                          'Is forkable?', 'Is private?', 'Is archived?', 'Is template?', 'Has wiki?', 'Has pages?',
                          'Has projects?', 'Has issues?', 'Has downloads?', 'Pushed at', 'Created at', 'Updated at']
    repo_search_row = [repository['full_name'], repository['id'], repository['description'], repository['forks'],
                       repository['stargazers_count'], repository['watchers'], repository['license'],
                       repository['default_branch'], repository['visibility'], repository['language'],
                       repository['open_issues'], repository['topics'], repository['homepage'], repository['clone_url'],
                       repository['ssh_url'], repository['fork'], repository['allow_forking'], repository['private'],
                       repository['archived'], repository['is_template'], repository['has_wiki'],
                       repository['has_pages'], repository['has_projects'], repository['has_issues'],
                       repository['has_downloads'], repository['pushed_at'], repository['created_at'],
                       repository['updated_at']]
    
    with open(os.path.join("output", f"{repository['name']}_repository_search_result_for_{query}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(repo_search_fields)
        write_csv.writerow(repo_search_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Create .csv for topic search
def log_topics_search(topic, query):
    topic_search_fields = ['Name', 'Score', 'Curated', 'Featured', 'Display name', 'Created by', 'Created at',
                           'Updated at']
    topic_search_row = [topic['name'], topic['score'], topic['curated'], topic['featured'], topic['display_name'],
                        topic['created_by'], topic['created_at'], topic['updated_at']]
    
    with open(os.path.join("output", f"{topic['name']}_topic_search_result_for_{query}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(topic_search_fields)
        write_csv.writerow(topic_search_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Create .csv for issues search
def log_issues_search(issue, query):
    issue_search_fields = ['Title', 'ID', 'Node ID', 'Number', 'State', 'Reactions', 'Comments', 'Milestone',
                           'Assignee', 'Assignees', 'Author association', 'Labels', 'Is locked?', 'Lock reason',
                           'Closed at', 'Created at', 'Updated at']
    issue_search_row = [issue['title'], issue['id'], issue['node_id'], issue['number'], issue['state'],
                        issue['reactions'], issue['comments'], issue['milestone'], issue['assignee'],
                        issue['assignees'], issue['author_association'], issue['labels'], issue['locked'],
                        issue['active_lock_reason'], issue['closed_at'], issue['created_at'], issue['updated_at']]
    
    with open(os.path.join("output", f"{issue['id']}_issue_search_result_for_{query}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(issue_search_fields)
        write_csv.writerow(issue_search_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")

    
# Create .csv for commits search
def log_commits_search(commit, query):
    commit_search_fields = ['SHA', 'Author', 'Username', 'Email', 'Committer', 'Repository', 'URL', 'Description']
    commit_search_row = [commit['commit']['tree']['sha'], commit['commit']['author']['name'], commit['author']['login'],
                         commit['commit']['author']['email'], commit['commit']['committer']['name'],
                         commit['repository']['full_name'], commit['html_url'], commit['commit']['message']]
    
    with open(os.path.join("output", f"{commit['commit']['tree']['sha']}_commit_search_result_for_{query}.csv"), 'w') as file:
        write_csv = csv.writer(file)
        write_csv.writerow(commit_search_fields)
        write_csv.writerow(commit_search_row)

        logging.info(logged_to_csv.format(file.name))
        xprint(f"{POSITIVE} {logged_to_csv.format(file.name)}")
