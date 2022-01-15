// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DappToken is ERC20 {
    constructor() ERC20("Dapp", "DAPP") {
        uint256 initialSupply = 1000000 * 10**18; // 1,000,00
        _mint(msg.sender, initialSupply);
    }
}
