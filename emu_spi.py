import sys
import time
import json
import socket
import webview


vspi_socket: socket.socket
web_window: webview.Window = None


def vspi_connect():
    func_id = 'driver.vspi_connect'
    global vspi_socket

    VSPI_IP = '127.0.0.1'
    # VSPI_IP = '192.168.122.17'
    VSPI_PORT = 6543
    VSPI_ADDR = (VSPI_IP, VSPI_PORT)
    CONNECTION_TIMEOUT = 10
    vspi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vspi_socket.setblocking(False)
    web_window.evaluate_js(f"add_log('{func_id}', 'INFO', 'connecting to VSPI address: {VSPI_IP}:{VSPI_PORT}')")
    for _ in range(CONNECTION_TIMEOUT):
        try:
            vspi_socket.connect(VSPI_ADDR)
            web_window.evaluate_js(f"add_log('{func_id}', 'INFO', 'connected')")
            web_window.evaluate_js(f"change_vspi_addr('{VSPI_IP}:{VSPI_PORT}')")
            return
        except (BlockingIOError, OSError):
            pass
        time.sleep(1)
    web_window.evaluate_js(f"add_log('{func_id}', 'ERROR', 'error connecting to VSPI')")


def soc_write_json():
    func_id = 'driver.soc_write_json'
    json_obj = {
        'topic': 'test_topic',
        'payload': 'test_msg',
        'retain': False,
    }
    data = json.dumps(json_obj)
    log_msg = f"writing: {data}".replace("'", '')
    web_window.evaluate_js(f"add_log('{func_id}', 'INFO', '{log_msg}')")
    try:
        vspi_socket.send(data.encode())
    except Exception as err:
        log_msg = f"error sending data: {err}".replace("'", '')
        web_window.evaluate_js(f"add_log('{func_id}', 'ERROR', '{log_msg}')")


def soc_write_json_retain():
    func_id = 'driver.soc_write_json_retain'
    json_obj = {
        'topic': 'test_topic_retain',
        'payload': 'test_msg_retain',
        'retain': True,
    }
    data = json.dumps(json_obj)
    web_window.evaluate_js(f"add_log('{func_id}', 'ERROR', 'writing: {data}')")
    try:
        vspi_socket.send(data.encode())
    except Exception as err:
        pass
        web_window.evaluate_js(f"add_log('{func_id}', 'ERROR', 'err sending data: {err}')")


def soc_write_device_packet_wght():
    func_id = 'driver.soc_write_device_packet_wght'
    packet = bytearray([0x87, 0x87, 0x0F, 0x00, 0x00, 0xA2, 0x00, 0x89, 0x41, 0x10, 0x40, 0xA4, 0x1A, 0x0D, 0x0A])
    web_window.evaluate_js(f"add_log('{func_id}', 'INFO', 'writing: {list(packet)}')")
    vspi_socket.send(packet)


def soc_write_device_packet_err():
    func_id = 'driver.soc_write_device_packet_deverr'
    packet = bytearray([0x87, 0x87, 0x0C, 0x00, 0x00, 0x4E, 0x00, 0xF0, 0x8C, 0x45, 0x0D, 0x0A])
    web_window.evaluate_js(f"add_log('{func_id}', 'INFO', 'writing: {list(packet)}')")
    vspi_socket.send(packet)


def exit():
    sys.exit(0)


class PyJSAPI:
    def vspi_connect(self, _):
        vspi_connect()

    def soc_write_json(self, _):
        soc_write_json()

    def soc_write_json_retain(self, _):
        soc_write_json_retain()

    def soc_write_device_packet_wght(self, _):
        soc_write_device_packet_wght()

    def soc_write_device_packet_err(self, _):
        soc_write_device_packet_err()

    def exit(self, _):
        exit()


py_js_api = PyJSAPI()
web_window = webview.create_window('EmuSpi', './emu_spi_gui.html', js_api=py_js_api, min_size=(600, 450))
webview.start(gui='gtk')
