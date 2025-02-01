import libtmux
import time 
import logging
import subprocess
import pyautogui
from abc import ABC, abstractmethod
import core.keys as keys

class BaseSPFManager(ABC):

    def __init__(self, spf_path : str):
        self.spf_path = spf_path
        # _ denotes the internal variables, anyone should not directly read/modify
        self._is_spf_running : bool = False

    @abstractmethod
    def start_spf(self, start_dir : str = None) -> None:
        pass 
    
    @abstractmethod
    def send_text_input(self, text : str, all_at_once : bool = False) -> None:
        pass 

    @abstractmethod
    def send_special_input(self, key : keys.Keys) -> None:
        pass 

    @abstractmethod
    def get_rendered_output(self) -> str:
        pass
    
    
    @abstractmethod
    def is_spf_running(self) -> bool:
        """
        We allow using _is_spf_running variable for efficiency
        But this method should give the true state, although this might have some calculations
        """
        return self._is_spf_running
    
    @abstractmethod
    def close_spf(self) -> None:
        """
        Close spf if its running and cleanup any other resources
        """
    
    def runtime_info(self) -> str:
        return "[No runtime info]"


class TmuxSPFManager(BaseSPFManager):
    """
    Tmux based Manager
    After running spf, you can connect to the session via
    tmux -L superfile attach -t spf_session
    Wont work in windows
    """
    # Class variables
    SPF_START_DELAY : float = 0.1 # seconds
    SPF_SOCKET_NAME : str = "superfile"

    # Init should not allocate any resources
    def __init__(self, spf_path : str):
        super().__init__(spf_path)
        self.logger = logging.getLogger()
        self.server = libtmux.Server(socket_name=TmuxSPFManager.SPF_SOCKET_NAME)
        self.spf_session : libtmux.Session = None
        self.spf_pane : libtmux.Pane = None

    def start_spf(self, start_dir : str = None) -> None:
        self.spf_session= self.server.new_session('spf_session',
                window_command=self.spf_path, 
                start_directory=start_dir)
        time.sleep(TmuxSPFManager.SPF_START_DELAY)

        self.spf_pane = self.spf_session.active_pane
        self._is_spf_running = True

    def _send_key(self, key : str) -> None:
        self.spf_pane.send_keys(key, enter=False)

    def send_text_input(self, text : str, all_at_once : bool = True) -> None:
        if all_at_once:
            self._send_key(text)
        else:
            for c in text:
                self._send_key(c)

    def send_special_input(self, key : keys.Keys) -> str:
        if key.ascii_code != keys.NO_ASCII:
            self._send_key(chr(key.ascii_code))
        elif isinstance(key, keys.SpecialKeys):
            self._send_key(key.key_name)
        else:
            raise Exception(f"Unknown key : {key}") 
            
    def get_rendered_output(self) -> str:
        return "[Not supported yet]"

    def is_spf_running(self) -> bool:
        self._is_spf_running = (
            (self.spf_session is not None)
            and (self.server.sessions.count(self.spf_session) == 1))

        return self._is_spf_running

    def close_spf(self) -> None:
        if self.is_spf_running():
            self.server.kill_session(self.spf_session.name)

    # Override
    def runtime_info(self) -> str:
        return str(self.server.sessions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(server : {self.server}, " + \
            f"session : {self.spf_session}, running : {self._is_spf_running})"


class PyAutoGuiSPFManager(BaseSPFManager):
    """Manage SPF via subprocesses and pyautogui
    Cross platform, but it globally takes over the input, so you need the terminal 
    constantly on focus during test run
    """
    SPF_START_DELAY : float = 0.5
    def __init__(self, spf_path : str):
        super().__init__(spf_path)
        self.spf_process = None


    def start_spf(self, start_dir : str = None) -> None:
        self.spf_process = subprocess.Popen([self.spf_path, start_dir],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(PyAutoGuiSPFManager.SPF_START_DELAY)

        # Need to send a sample keypress otherwise it ignores first keypress
        self.send_text_input('x')
        
    
    def send_text_input(self, text : str, all_at_once : bool = False) -> None:
        if all_at_once :
            pyautogui.write(text)
        else:
            for c in text:
                pyautogui.write(c)

    def send_special_input(self, key : keys.Keys) -> None:
        if isinstance(key, keys.CtrlKeys):
            pyautogui.hotkey('ctrl', key.char)
        elif isinstance(key, keys.SpecialKeys):
            pyautogui.press(key.key_name.lower())
        else:
            raise Exception(f"Unknown key : {key}") 

    def get_rendered_output(self) -> str:
        return "[Not supported yet]" 
    
    
    def is_spf_running(self) -> bool:
        self._is_spf_running = (self.spf_process is not None) and (self.spf_process.poll() is None)
        return self._is_spf_running
    
    def close_spf(self) -> None:
        if self.spf_process is not None:
            self.spf_process.terminate()
    
    # Override
    def runtime_info(self) -> str:
        if self.spf_process is None:
            return "[No process]"
        else:
            return f"[PID : {self.spf_process.pid}, poll : {self.spf_process.poll()}]"  



