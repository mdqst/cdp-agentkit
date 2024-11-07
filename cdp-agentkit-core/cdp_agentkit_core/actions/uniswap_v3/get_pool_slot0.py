from cdp import SmartContract
from pydantic import BaseModel, Field

from cdp_agentkit_core.actions.uniswap_v3.constants import (
    UNISWAP_V3_POOL_ABI,
)

UNISWAP_V3_GET_POOL_SLOT0_PROMPT = """
This tool will get the slot0 details for Uniswap V3 pools that have been previously created. The slot0 contains the sqrtPriceX96, tick, observationIndex, observationCardinality, observationCardinalityNext, feeProtocol, and unlocked.
The sqrtPriceX96 is the current price of the pool as a sqrt(token1/token0) Q64.96 value.
The tick is the current tick of the pool, i.e. according to the last tick transition that was run. This value may not always be equal to SqrtTickMath getTickAtSqrtRatio(sqrtPriceX96) if the price is on a tick boundary.
The observationIndex is the index of the last oracle observation that was written.
The observationCardinality is the current maximum number of observations stored in the pool.
The observationCardinalityNext is the next maximum number of observations.
The feeProtocol is the current protocol fee as a percentage of the swap fee taken on withdrawal.
The unlocked is whether the pool is currently locked to reentrancy.
It takes in the networkId and the pool contract address. Supported networks are Base Sepolia, Base Mainnet, Ethereum Mainnet, Polygon Mainnet, and Arbitrum Mainnet.
"""


class UniswapV3GetPoolSlot0Input(BaseModel):
    """Input argument schema for get pool slot0 action."""

    network_id: str = Field(
        ...,
        description="The network ID of the network to get the pool on.",
    )
    pool_contract_address: str = Field(
        ...,
        description="The contract address of the pool to get the slot0 for.",
    )


def uniswap_v3_get_pool_slot0(network_id: str, pool_contract_address: str) -> str:
    """Get the slot0 for Uniswap V3 pools that have been created.

    Args:
        network_id (str): The network ID of the network to get the pool on.
        pool_contract_address (str): The contract address of the pool to get the liquidity for.

    Returns:
        str: A message containing the slot0 details for the pool.

    """
    slot0 = SmartContract.read(
        network_id=network_id,
        contract_address=pool_contract_address,
        method="slot0",
        abi=UNISWAP_V3_POOL_ABI,
        args={},
    )

    return f"Slot0 for pool {pool_contract_address} is {slot0}."
