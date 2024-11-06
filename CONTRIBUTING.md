# CDP Agentkit Contributing Guide
Thank you for your interest in contributing to CDP Agentkit! We welcome all contributions, no matter how big or small. Some of the ways you can contribute include:
- Adding new actions to the core package
- Updating existing Langchain Toolkits or adding new Langchain Toolkits to support new tools
- Creating new AI frameworks extensions
- Adding tests and improving documentation

## Development

### Prerequisites
- Python 3.10 or higher
- Rust/Cargo installed ([Rust Installation Instructions](https://doc.rust-lang.org/cargo/getting-started/installation.html))
- Poetry for package management and tooling
  - [Poetry Installation Instructions](https://python-poetry.org/docs/#installation)

`cdp-langchain` also requires a [CDP API Key](https://portal.cdp.coinbase.com/access/api).

### Set-up

Clone the repo by running:

```bash
git clone git@github.com:coinbase/cdp-agentkit.git
```

## Adding an Action to Agentkit Core
- Actions are defined in `./cdp_agentkit_core/actions` module. See `./cdp_agentkit_core/actions/mint_nft.py` for an example.

### Components of an Agentic Action
Each action will define and export 3 components:
- Prompt - A string that will provide the AI Agent with context on what the function does and a natural language description of the input.
  - E.g. 
```python
MINT_NFT_PROMPT = """
This tool will mint an NFT (ERC-721) to a specified destination address onchain via a contract invocation. It takes the contract address of the NFT onchain and the destination address onchain that will receive the NFT as inputs."""
```
- ArgSchema - A Pydantic Model that defines the input argument schema for the action.
  - E.g.
```python
class MintNftInput(BaseModel):
    """Input argument schema for mint NFT action."""

    contract_address: str = Field(
        ...,
        description="The contract address of the NFT (ERC-721) to mint, e.g. `0x036CbD53842c5426634e7929541eC2318f3dCF7e`",
    )
    destination: str = Field(
        ...,
        description="The destination address that will receieve the NFT onchain, e.g. `0x036CbD53842c5426634e7929541eC2318f3dCF7e`",
    )
```
- Action Callable - A function (or Callable class) that executes the action.
  - E.g.
```python
def mint_nft(wallet: Wallet, contract_address: str, destination: str) -> str:
    """Mint an NFT (ERC-721) to a specified destination address onchain via a contract invocation.

    Args:
        wallet (Wallet): The wallet to trade the asset from.
        contract_address (str): The contract address of the NFT (ERC-721) to mint, e.g. `0x036CbD53842c5426634e7929541eC2318f3dCF7e`.
        destination (str): The destination address that will receieve the NFT onchain, e.g. `0x036CbD53842c5426634e7929541eC2318f3dCF7e`.

    Returns:
        str: A message containing the NFT mint details.

    """
    mint_args = {"to": destination, "quantity": "1"}

    mint_invocation = wallet.invoke_contract(
        contract_address=contract_address, method="mint", args=mint_args
    ).wait()

    return f"Minted NFT from contract {contract_address} to address {destination} on network {wallet.network_id}.\nTransaction hash for the mint: {mint_invocation.transaction.transaction_hash}\nTransaction link for the mint: {mint_invocation.transaction.transaction_link}"
```

## Adding an Agentic Action to Langchain Toolkit
1. Ensure the action is implemented in `cdp-agentkit-core`.
2. Add a wrapper method to `CdpAgentkitWrapper` in `./cdp_langchain/utils/cdp_agentkit_wrapper.py`
   - E.g.
```python
    def mint_nft_wrapper(self, contract_address: str, destination: str) -> str:
        """Mint an NFT (ERC-721) to a specified destination address onchain via a contract invocation.

        Args:
            contract_address (str): "The contract address of the NFT (ERC-721) to mint, e.g. `0x036CbD53842c5426634e7929541eC2318f3dCF7e`".
            destination (str): "The destination address that will receieve the NFT onchain, e.g. `0x036CbD53842c5426634e7929541eC2318f3dCF7e`".

        Returns:
            str: A message containing the NFT mint details.

        """
        return mint_nft(
            wallet=self.wallet,
            contract_address=contract_address,
            destination=destination,
        )
```
3. Add call to the wrapper in `CdpAgentkitWrapper.run` in `./cdp_langchain/utils/cdp_agentkit_wrapper.py`
   - E.g.
```python
        if mode == "mint_nft":
            return self.mint_nft_wrapper(**kwargs)

```
4. Add the action to the list of available tools in the `CdpToolkit` in `./cdp_langchain/agent_toolkits/cdp_toolkit.py`
   - E.g.
```python
        actions: List[Dict] = [
            {
                "mode": "mint_nft",
                "name": "mint_nft",
                "description": MINT_NFT_PROMPT,
                "args_schema": MintNftInput,
            },
        ]
```
5. Add the action to the list of tools in the `CdpToolkit` class documentation.

## Development Tools
### Formatting
`make format`

### Linting
- Check linter
`make lint`

- Fix linter errors
`make lint-fix`

### Unit Testing
- Run unit tests
`make test`

## Changelog
- For new features and bug fixes, please add a new changelog entry to the `CHANGELOG.md` file in the appropriate packages and include that in your Pull Request.