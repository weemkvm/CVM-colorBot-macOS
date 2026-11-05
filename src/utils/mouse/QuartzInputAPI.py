"""
macOS mouse/keyboard input backend using Quartz (CoreGraphics).
Drop-in replacement for SendInputAPI on macOS.
"""
from src.utils.debug_logger import log_print
from . import state

try:
    import Quartz
    from Quartz import (
        CGEventCreateMouseEvent,
        CGEventCreateKeyboardEvent,
        CGEventPost,
        CGEventGetLocation,
        CGEventCreate,
        kCGEventMouseMoved,
        kCGEventLeftMouseDown,
        kCGEventLeftMouseUp,
        kCGHIDEventTap,
        kCGEventKeyDown,
        kCGEventKeyUp,
    )
    HAS_QUARTZ = True
except ImportError:
    HAS_QUARTZ = False

_current_pos = [0.0, 0.0]


def _get_mouse_pos():
    try:
        event = CGEventCreate(None)
        point = CGEventGetLocation(event)
        _current_pos[0] = point.x
        _current_pos[1] = point.y
    except Exception:
        pass
    return _current_pos[0], _current_pos[1]


def connect():
    state.last_connect_error = ""
    if not HAS_QUARTZ:
        state.last_connect_error = "pyobjc-framework-Quartz not installed"
        state.set_connected(False, "SendInput")
        return False
    disconnect()
    _get_mouse_pos()
    state.set_connected(True, "SendInput")
    state.reset_button_states()
    log_print("[INFO] Quartz (macOS) input backend ready.")
    return True


def disconnect():
    state.set_connected(False, "SendInput")
    state.mask_applied_idx = None
    state.reset_button_states()


def is_button_pressed(idx: int) -> bool:
    try:
        import Quartz as Q
        buttons = Q.NSEvent.pressedMouseButtons()
        if idx == 0:
            return bool(buttons & (1 << 0))
        if idx == 1:
            return bool(buttons & (1 << 1))
        if idx == 2:
            return bool(buttons & (1 << 2))
        if idx == 3:
            return bool(buttons & (1 << 3))
        if idx == 4:
            return bool(buttons & (1 << 4))
    except Exception:
        pass
    return False


def is_key_pressed(key) -> bool:
    try:
        from .keycodes import to_vk_code
        import Quartz as Q
        vk = to_vk_code(key)
        if vk is None:
            return False
        return Q.CGEventSourceKeyState(Q.kCGEventSourceStateHIDSystemState, vk)
    except Exception:
        return False


def move(x: float, y: float):
    if not state.is_connected or state.active_backend != "SendInput":
        return
    cx, cy = _get_mouse_pos()
    nx = cx + float(x)
    ny = cy + float(y)
    _current_pos[0] = nx
    _current_pos[1] = ny
    try:
        event = CGEventCreateMouseEvent(
            None, kCGEventMouseMoved,
            Quartz.CGPointMake(nx, ny), 0
        )
        CGEventPost(kCGHIDEventTap, event)
    except Exception as e:
        state.last_connect_error = f"Quartz move failed: {e}"


def move_bezier(x: float, y: float, segments: int, ctrl_x: float, ctrl_y: float):
    move(x, y)


def left(isdown: int):
    if not state.is_connected or state.active_backend != "SendInput":
        return
    cx, cy = _get_mouse_pos()
    try:
        etype = kCGEventLeftMouseDown if isdown else kCGEventLeftMouseUp
        event = CGEventCreateMouseEvent(
            None, etype,
            Quartz.CGPointMake(cx, cy), 0
        )
        CGEventPost(kCGHIDEventTap, event)
    except Exception as e:
        state.last_connect_error = f"Quartz click failed: {e}"


def key_down(key):
    from .keycodes import to_vk_code
    vk = to_vk_code(key)
    if vk is None:
        return
    try:
        event = CGEventCreateKeyboardEvent(None, vk, True)
        CGEventPost(kCGHIDEventTap, event)
    except Exception:
        pass


def key_up(key):
    from .keycodes import to_vk_code
    vk = to_vk_code(key)
    if vk is None:
        return
    try:
        event = CGEventCreateKeyboardEvent(None, vk, False)
        CGEventPost(kCGHIDEventTap, event)
    except Exception:
        pass


def key_press(key):
    key_down(key)
    key_up(key)


def test_move():
    move(100, 100)
