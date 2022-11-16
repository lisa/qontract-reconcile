from typing import Optional

import pytest

from reconcile.cna.assets.asset import (
    AssetStatus,
    AssetType,
)
from reconcile.cna.assets.null import NullAsset
from reconcile.cna.state import State


def null_asset(
    name: str,
    href: Optional[str] = None,
    id: Optional[str] = None,
    addr_block: Optional[str] = None,
    status: Optional[AssetStatus] = None,
) -> NullAsset:
    return NullAsset(
        id=id,
        href=href,
        status=status,
        name=name,
        addr_block=addr_block,
        bindings=set(),
    )


@pytest.mark.parametrize(
    "a, b",
    [
        (
            # Empty states are equal
            State(assets={}),
            State(assets={}),
        ),
        (
            # Status does not count towards equality
            State(
                assets={
                    AssetType.NULL: {
                        "test": null_asset(
                            name="test",
                        ),
                        "test2": null_asset(
                            name="test2",
                            status=AssetStatus.RUNNING,
                        ),
                    }
                }
            ),
            State(
                assets={
                    AssetType.NULL: {
                        "test": null_asset(
                            name="test",
                        ),
                        "test2": null_asset(
                            name="test2",
                            status=AssetStatus.TERMINATED,
                        ),
                    }
                }
            ),
        ),
        (
            # id and href do not count towards equality
            State(
                assets={
                    AssetType.NULL: {
                        "test": null_asset(
                            name="test",
                        ),
                        "test2": null_asset(
                            name="test2",
                            status=AssetStatus.RUNNING,
                        ),
                    }
                }
            ),
            State(
                assets={
                    AssetType.NULL: {
                        "test": null_asset(
                            name="test",
                        ),
                        "test2": null_asset(
                            name="test2",
                            id="123",
                            href="/123",
                        ),
                    }
                }
            ),
        ),
    ],
    ids=[
        "Empty states are equal",
        "Status does not count towards equality",
        "id and href do not count towards equality",
    ],
)
def test_state_eq(a: State, b: State):
    assert a == b


@pytest.mark.parametrize(
    "a, b",
    [
        (
            # single element with different attribute
            State(
                assets={
                    AssetType.NULL: {
                        "test": null_asset(
                            name="test",
                        ),
                        "test2": null_asset(
                            name="test2",
                            status=AssetStatus.RUNNING,
                        ),
                    }
                }
            ),
            State(
                assets={
                    AssetType.NULL: {
                        "test": null_asset(
                            name="test",
                        ),
                        "test2": null_asset(
                            name="test2",
                            addr_block="123",
                        ),
                    }
                }
            ),
        ),
        (
            # different elements
            State(
                assets={
                    AssetType.NULL: {
                        "test": null_asset(
                            name="test",
                        ),
                    }
                }
            ),
            State(
                assets={
                    AssetType.NULL: {
                        "test2": null_asset(
                            name="test2",
                            id="123",
                            href="/123",
                        ),
                    }
                }
            ),
        ),
    ],
    ids=[
        "single element with different attribute",
        "different elements",
    ],
)
def test_state_ne(a: State, b: State):
    assert a != b


def test_state_iter():
    assets = [
        null_asset(
            name="test",
        ),
        null_asset(
            name="test2",
        ),
    ]
    state = State(assets={AssetType.NULL: {asset.name: asset for asset in assets}})
    iterated_assets = [asset for asset in state]

    assert sorted(assets, key=lambda x: x.name) == sorted(
        iterated_assets, key=lambda x: x.name
    )
