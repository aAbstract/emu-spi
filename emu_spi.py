import time
import json
import socket
import webview


vspi_socket: socket.socket
web_window: webview.Window = None


def vspi_connect():
    global vspi_socket

    VSPI_IP = '192.168.122.17'
    VSPI_PORT = 6543
    VSPI_ADDR = (VSPI_IP, VSPI_PORT)
    CONNECTION_TIMEOUT = 10
    vspi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vspi_socket.setblocking(False)
    web_window.evaluate_js(f"add_log('', 'INFO', 'connecting to VSPI address: {VSPI_ADDR}')")
    for _ in range(CONNECTION_TIMEOUT):
        try:
            vspi_socket.connect(VSPI_ADDR)
            web_window.evaluate_js(f"add_log('', 'INFO', 'connected')")
            return
        except (BlockingIOError, OSError):
            pass
        time.sleep(1)
    web_window.evaluate_js(f"add_log('', 'ERROR', 'error connecting to VSPI')")


def soc_write_json():
    json_obj = {
        'topic': 'test_topic',
        'payload': 'test_msg',
        'retain': False,
    }
    data = json.dumps(json_obj)
    web_window.evaluate_js(f"add_log('', 'ERROR', 'writing: {data}')")
    try:
        vspi_socket.send(data.encode())
    except Exception as err:
        web_window.evaluate_js(f"add_log('', 'ERROR', 'err sending data: {err}')")


def soc_write_json_retain():
    json_obj = {
        'topic': 'test_topic_retain',
        'payload': 'test_msg_retain',
        'retain': True,
    }
    data = json.dumps(json_obj)
    web_window.evaluate_js(f"add_log('', 'ERROR', 'writing: {data}')")
    try:
        vspi_socket.send(data.encode())
    except Exception as err:
        pass
        web_window.evaluate_js(f"add_log('', 'ERROR', 'err sending data: {err}')")


def exec_cmd(cmd: str):
    cmd_map = {
        'wjs': soc_write_json,
        'wjsr': soc_write_json_retain,
    }
    if cmd not in cmd_map:
        web_window.evaluate_js(f"add_log('', 'ERROR', 'unknown command, cmd={cmd}')")
        return
    cmd_map[cmd]()


class Ipc:
    def vspi_connect(self):
        vspi_connect()


ipc = Ipc()
web_window = webview.create_window('EmuSpi', './emu_spi_gui.html', js_api=ipc, min_size=(600, 450))
webview.start(gui='gtk')
