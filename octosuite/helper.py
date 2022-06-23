import sys
from octosuite.colors import Color

"""
Help
This class holds the help text for available.
Almost everything in the methods from this class is hard coded
"""
class Help:
    usageText = 'Use {} to get started'
    usageText1 = 'Use {} to view all available subcommands.'
    
    def Org():
        sys.stdout.write(f"""
{Color.white}Note:
-------
     The '{Color.green}org{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:org')}{Color.reset}
     """)
     
    
    def Repo():
        sys.stdout.write(f"""
{Color.white}Note:
-----
     The '{Color.green}repo{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:repo')}{Color.reset}
     """)
    
      
    def User():
        sys.stdout.write(f"""
{Color.white}Note:
-----
     The '{Color.green}user{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:user')}{Color.reset}
     """)
     
    def Search():
        sys.stdout.write(f"""
{Color.white}Note:
-----
     The '{Color.green}search{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:search')}{Color.reset}
     """)
     
     
    def Source():
        sys.stdout.write(f"""
{Color.white}Note:
-----
     The '{Color.green}source{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:source')}{Color.reset}
     """)
     
    def Logs():
        sys.stdout.write(f"""
{Color.white}Note:
-----
     The '{Color.green}logs{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:logs')}{Color.reset}
     """)
     
    
    def Version():
        sys.stdout.write(f"""
{Color.white}Note:
-----
     The '{Color.green}version{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:version')}{Color.reset}
     """)
     
     
    def Csv():
        sys.stdout.write(f"""
{Color.white}Note:
-----
     The '{Color.green}csv{Color.white}' command works with subcommands.
     {Help.usageText1.format('help:csv')}{Color.reset}
     """)
     
     
    def versionCommand():
        sys.stdout.write(f"""
{Color.white}Version subcommands{Color.reset}
{'='*18}
{Help.usageText.format('version:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    check              Check for new release(s)
    info               Version info
    """)
    
    
    def sourceCommand():
        sys.stdout.write(f"""
{Color.white}Source subcommands{Color.reset}
{'='*18}
{Help.usageText.format('source:<subcommand>')}
    {Color.white}Command            Description{Color.reset}
    --------            -----------
    zipball            Download source code as zipball
    tarball            Download source code  as tarball
    """)
        
        
    def searchCommand():
        sys.stdout.write(f"""
{Color.white}Search subcommands{Color.reset}
{'='*18}
{Help.usageText.format('search:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    users              Search user(s)
    repos              Search repositor[yies]
    topics             Search topic(s)
    issues             Search issue(s)
    commits            Search commit(s)
    """)
            
            
    def userCommand():
        sys.stdout.write(f"""
{Color.white}User subcommands{Color.reset}
{'='*17}
{Help.usageText.format('user:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    profile            Get a user's profile info
    gists              Return a users's gists
    orgs               Return organizations that a user belongs to/owns
    repos              Return a user's repositories
    events             Return a user's events
    follows            Check if user(A) follows user(B)
    followers          Return a user's followers
    following          Return a list of users the target is following
    subscriptions      Return a user's subscriptions
    """)
        
        
    def orgCommand():
        sys.stdout.write(f"""
{Color.white}Org subcommands{Color.reset}
{'='*16}
{Help.usageText.format('org:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    profile            Get an organization's info
    repos              Return an organization's repositories
    events             Return an organization's events
    member             Check if a specified user is a public member of the target organization
    """)
            
            
    def repoCommand():
        sys.stdout.write(f"""
{Color.white}Repo subcommands{Color.reset}
{'='*17}
{Help.usageText.format('repo:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    profile            Get a repository's info
    issues             Return a repository's issues
    forks              Return a repository's forks
    releases           Return a repository's releases
    stargazers         Return a repository's stargazers
    pathcontents       List contents in a path of a repository
    """)
             
        
    def logsCommand():
        sys.stdout.write(f"""
{Color.white}Logs subcommands{Color.reset}
{'='*17}
{Help.usageText.format('logs:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    view               View logs
    read               Read log
    delete             Delete log
    """)
    
    def csvCommand():
        sys.stdout.write(f"""
{Color.white}Csv subcommands{Color.reset}
{'='*17}
{Help.usageText.format('csv:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    view               View csv files
    read               Read csv
    delete             Delete csv
    """)
                
            
    def helpCommand():      
        sys.stdout.write(f"""
{Color.white}Core commands{Color.reset}
{'='*13}

    {Color.white}Command               Description{Color.reset}
    -------               -----------
    help                  Help menu
    exit                  Close session
    clear                 Clear screen
    about                 Program' info
    author                Developer' info
 
       
{Color.white}Help subcommands{Color.reset}
{'='*16}
{Help.usageText.format('help:<subcommand>')}

    {Color.white}Command               Description{Color.reset}
    -------               -----------
    csv                   (coming soon)
    org                   List all organization investigation commands
    logs                  List all logs management commands
    repo                  List all repository investigation commands
    user                  List all users investigation commands
    search                List all target discovery commands
    source                (beta) List all source code download commands (for developers)
    version               List all version management commands
    """)
