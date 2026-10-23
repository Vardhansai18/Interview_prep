import fcntl
import os
import signal
import sys
import time


def _derive_lock_path(status_file: str) -> str:
    """Derive the lock file path from the status file path."""
    return status_file + ".lock"


# ── Python API ────────────────────────────────────────────────────────────────

def exclusive_lock(status_file: str, timeout: int = 30):
    """
    Acquires an exclusive cross-user flock on the lock file derived from status_file.

    Returns the open file object (lock_fd).
    Caller MUST keep this reference alive and pass it to exclusive_unlock().
    Raises TimeoutError if lock is not acquired within `timeout` seconds.
    """
    lock_path = _derive_lock_path(status_file)
    os.makedirs(os.path.dirname(lock_path), exist_ok=True)
    lock_fd = open(lock_path, "w")
    try:
        os.chmod(lock_path, 0o666)
    except PermissionError:
        # Lock file was created by a different user (already has 0666 perms).
        # Only the owner can chmod — safe to skip since the file is world-writable.
        pass
    deadline = time.monotonic() + timeout

    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lock_fd
        except BlockingIOError:
            if time.monotonic() >= deadline:
                lock_fd.close()
                raise TimeoutError(
                    f"[PID {os.getpid()}] Could not acquire lock on "
                    f"'{lock_path}' within {timeout}s. "
                    "Another agent instance may be holding it."
                )
            time.sleep(0.5)


def exclusive_unlock(lock_fd) -> None:
    """
    Releases the exclusive flock and closes the file descriptor.
    Always call this in a finally block to guarantee release.
    """
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
    finally:
        lock_fd.close()


# ── Shell / Bash CLI Support ──────────────────────────────────────────────────

def _locker_daemon(status_file: str, timeout: int) -> None:
    """
    Child process: acquires the flock and holds it until SIGTERM.
    Detaches from the terminal so the parent's $() returns immediately.
    """
    os.setsid()

    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 0)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    os.close(devnull)

    write_pipe = int(os.environ["_LOCK_PIPE_FD"])

    try:
        lock_fd = exclusive_lock(status_file, timeout)
        os.write(write_pipe, b"ok\n")
    except TimeoutError:
        os.write(write_pipe, b"timeout\n")
        os.close(write_pipe)
        sys.exit(1)

    os.close(write_pipe)

    signal.signal(signal.SIGTERM, lambda sig, frame: sys.exit(0))
    while True:
        time.sleep(1)


def lock_for_shell(status_file: str, timeout: int = 30) -> int:
    """
    Forks a background daemon process that holds the flock.
    Returns the PID of the daemon — pass this to unlock_for_shell().
    """
    read_pipe, write_pipe = os.pipe()

    pid = os.fork()

    if pid == 0:
        os.close(read_pipe)
        os.environ["_LOCK_PIPE_FD"] = str(write_pipe)
        _locker_daemon(status_file, timeout)
        sys.exit(0)
    else:
        os.close(write_pipe)
        response = os.read(read_pipe, 16).decode().strip()
        os.close(read_pipe)

        if response == "ok":
            return pid
        else:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            raise TimeoutError(
                f"Could not acquire lock on '{_derive_lock_path(status_file)}' "
                f"within {timeout}s"
            )


def unlock_for_shell(locker_pid: int) -> None:
    """
    Sends SIGTERM to the background locker daemon, releasing the flock.
    """
    try:
        os.kill(locker_pid, signal.SIGTERM)
        os.waitpid(locker_pid, 0)
    except (ProcessLookupError, ChildProcessError):
        pass


# ── Entry Point (bash CLI) ────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            f"Usage:\n"
            f"  {sys.argv[0]} lock   <status_file> [timeout]\n"
            f"  {sys.argv[0]} unlock <PID>",
            file=sys.stderr,
        )
        sys.exit(1)

    command = sys.argv[1]

    if command == "lock":
        status_file = sys.argv[2]
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        try:
            daemon_pid = lock_for_shell(status_file, timeout)
            print(daemon_pid)
            sys.exit(0)
        except TimeoutError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    elif command == "unlock":
        locker_pid = int(sys.argv[2])
        unlock_for_shell(locker_pid)
        sys.exit(0)

    else:
        print(f"ERROR: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)
