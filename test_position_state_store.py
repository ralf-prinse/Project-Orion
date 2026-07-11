from pathlib import Path


def run():
    path = Path("services/position_state_store.py")
    assert not path.exists(), (
        "Legacy PositionStateStore file still exists."
    )
    print("POSITION STATE STORE REMOVAL: PASS")


if __name__ == "__main__":
    run()
