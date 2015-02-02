import contextlib
import json
import os
import sys
import tempfile

__all__ = ['MockCommand', 'assert_calls']

commands_dir = None
recording_dir = None

def prepend_to_path(dir):
    os.environ['PATH'] = dir + os.pathsep + os.environ['PATH']

def remove_from_path(dir):
    path_dirs = os.environ['PATH'].split(os.pathsep)
    path_dirs.remove(dir)
    os.environ['PATH'] = os.pathsep.join(path_dirs)


_record_run = """#!{python}
import os, sys
import json

cmd = os.path.basename(__file__)
with open(os.path.join({recording_dir!r}, cmd), 'a') as f:
    json.dump({{'env': dict(os.environ),
               'argv': sys.argv,
               'cwd': os.getcwd()}},
              f)
    f.write('\x1e') # ASCII record separator
"""

# TODO: Overlapping calls to the same command may interleave writes.

class MockCommand(object):
    """Context manager to mock a system command.
    
    The mock command will be written to a directory at the front of $PATH,
    taking precedence over any existing command with the same name.
    
    By specifying content as a string, you can determine what running the
    command will do. The default content records each time the command is
    called and exits: you can access these records with mockcmd.get_calls().
    
    On Windows, the specified content will be run by the Python interpreter in
    use. On Unix, it should start with a shebang (``#!/path/to/interpreter``).
    """
    def __init__(self, name, content=None):
        self.name = name
        self.content = content
    
    def _write_cmd_file(self):
        c = '"{python}" "%~dp0\{pyfile}" %*\r\n'
        path = os.path.join(commands_dir, self.name+'.cmd')
        with open(path, 'w') as f:
            f.write(c.format(python=sys.executable, pyfile=self.name+'.py'))

    @property
    def _cmd_path(self):
        # Can only be used once commands_dir has been set
        p = os.path.join(commands_dir, self.name)
        if os.name == 'nt':
            p += '.py'
        return p

    def __enter__(self):
        global commands_dir, recording_dir
        if commands_dir is None:
            commands_dir = tempfile.mkdtemp()
        if recording_dir is None:
            recording_dir = tempfile.mkdtemp()

        if os.path.isfile(self._cmd_path):
            raise EnvironmentError("Command %r already exists at %s" %
                                            (self.name, self._cmd_path))
        
        if commands_dir not in os.environ['PATH'].split(os.pathsep):
            prepend_to_path(commands_dir)
        
        if self.content is None:
            self.content = _record_run.format(python=sys.executable,
                                              recording_dir=recording_dir)

        with open(self._cmd_path, 'w') as f:
            f.write(self.content)
        
        if os.name == 'nt':
            self._write_cmd_file()
        else:
            os.chmod(self._cmd_path, 0o755) # Set executable bit
        
        return self
    
    def __exit__(self, etype, evalue, tb):
        os.remove(self._cmd_path)
        if os.name == 'nt':
            os.remove(os.path.join(commands_dir, self.name+'.cmd'))
        if not os.listdir(commands_dir):
            remove_from_path(commands_dir)

    def get_calls(self):
        """Get a list of calls made to this mocked command.
        
        This relies on the default script content, so it will return an
        empty list if you specified a different content parameter.
        
        For each time the command was run, the list will contain a dictionary
        with keys argv, env and cwd.
        """
        if recording_dir is None:
            return []
        record_file = os.path.join(recording_dir, self.name)
        if not os.path.isfile(record_file):
            return []
        
        with open(record_file, 'r') as f:
            # 1E is ASCII record separator, last chunk is empty
            chunks = f.read().split('\x1e')[:-1]
        
        return [json.loads(c) for c in chunks]


@contextlib.contextmanager
def assert_calls(cmd, args=None):
    """Assert that a block of code runs the given command.
    
    If args is passed, also check that it was called at least once with the
    given arguments (not including the command name).
    
    Use as a context manager, e.g.::
    
        with assert_calls('git'):
            some_function_wrapping_git()
            
        with assert_calls('git', ['add', myfile]):
            some_other_function()
    """
    with MockCommand(cmd) as mc:
        yield
    
    calls = mc.get_calls()
    assert calls != [], "Command %r was not called" % cmd

    if args is not None:
        if not any(args == c['argv'][1:] for c in calls):
            msg = ["Command %r was not called with specified args (%r)" %
                            (cmd, args),
                   "It was called with these arguments: "]
            for c in calls:
                msg.append('  %r' % c['argv'][1:])
            raise AssertionError('\n'.join(msg))
