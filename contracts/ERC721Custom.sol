// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract ERC721Custom is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    using SafeMath for uint256;
    using Strings for uint256;

    uint256 private NFTPrice = 88800000000000000;
    uint256 private mintLimit = 10;
    uint256 public presaleMintLimit = 3;
    uint256 public constant tokenSupply = 5000;

    bool public saleOpen;
    bool public revealed;
    bool public presaleOpen;

    mapping(address => bool) private whiteList;
    mapping(address => uint256) private presaleMints;

    Counters.Counter private _tokenIdCount;

    string private baseURI;
    string private notRevealedUri;
    string private contractURI;
    string public baseExtension = ".json";
    string public provenance_hash;

    address private community = 0x0000000000000000000000000000000000000000;
    address private dev = 0x0000000000000000000000000000000000000000;

    constructor(
        string memory _initNotRevealedUri,
        string memory _initContractURI
    ) ERC721("My NFT Project", "MNP") {
        setNotRevealedURI(_initNotRevealedUri);
        setContractURI(_initContractURI);
    }

    function setNotRevealedURI(string memory _notRevealedURI) public onlyOwner {
        notRevealedUri = _notRevealedURI;
    }

    function setContractURI(string memory _cURI) public onlyOwner {
        contractURI = _cURI;
    }

    function _contractURI() public view returns (string memory) {
        return contractURI;
    }

    function setBaseURI(string memory URI) public onlyOwner {
        baseURI = URI;
    }

    function reveal() public onlyOwner {
        revealed = true;
    }

    function setPresaleMintLimit(uint256 _presaleMintLimit) external onlyOwner {
        presaleMintLimit = _presaleMintLimit;
    }

    function presaleStateChange() public onlyOwner {
        presaleOpen = !presaleOpen;
    }

    function saleStateChange() public onlyOwner {
        saleOpen = !saleOpen;
    }

    function addToWhiteList(address[] calldata addresses) external onlyOwner {
        for (uint256 i = 0; i < addresses.length; i++) {
            if (!whiteList[addresses[i]]) {
                whiteList[addresses[i]] = true;
                presaleMints[addresses[i]] = 0;
            }
        }
    }

    function isOnWhiteList(address wallet) external view returns (bool) {
        return whiteList[wallet];
    }

    function createTokenPresale(uint256 _tokenAmount) public payable {
        require(presaleOpen, "Presale is not open");
        require(
            NFTPrice * _tokenAmount <= msg.value,
            "Insufficient amount of funds."
        );
        require(
            tokenSupply >= _tokenIdCount.current().add(_tokenAmount),
            "Cannot exceed the max supply!"
        );
        require(whiteList[msg.sender] == true, "Not on whitelist");
        require(
            presaleMints[msg.sender] + _tokenAmount <= presaleMintLimit,
            "Over the presale minting limit"
        );

        presaleMints[msg.sender] += _tokenAmount;
        for (uint256 i = 0; i < _tokenAmount; i++) {
            mintNFT();
        }
    }

    function createToken(uint256 _nftAmount) public payable {
        require(
            saleOpen,
            "The sale has not started yet or it has been closed!"
        );
        require(
            _nftAmount <= mintLimit,
            "You cannot mint this many NFTs at once!"
        );
        require(
            NFTPrice * _nftAmount <= msg.value,
            "Insufficient amount of funds."
        );
        require(
            tokenSupply >= _tokenIdCount.current().add(_nftAmount),
            "Cannot exceed the max supply!"
        );
        for (uint256 i = 0; i < _nftAmount; i++) {
            mintNFT();
        }
    }

    function mintNFT() private {
        _safeMint(msg.sender, _tokenIdCount.current() + 1);
        _tokenIdCount.increment();
    }

    function reserveTokens(address to, uint256 _amount) public onlyOwner {
        require(
            tokenSupply >= _tokenIdCount.current().add(_amount),
            "Cannot exceed the max supply!"
        );
        for (uint256 i = 0; i < _amount; i++) {
            _safeMint(to, _tokenIdCount.current() + 1);
            _tokenIdCount.increment();
        }
    }

    function setMintLimit(uint256 _amount) external onlyOwner {
        mintLimit = _amount;
    }

    function getMintLimit() public view returns (uint256) {
        return mintLimit;
    }

    function setTokenPrice(uint256 _price) external onlyOwner {
        NFTPrice = _price;
    }

    function getTokenPrice() public view returns (uint256) {
        return NFTPrice;
    }

    function totalSupply() public view virtual returns (uint256) {
        return _tokenIdCount.current();
    }

    function _baseURI() internal view override returns (string memory) {
        return baseURI;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI query for nonexistent token"
        );
        if (revealed == false) {
            return notRevealedUri;
        }
        string memory currentBaseURI = _baseURI();
        return
            bytes(currentBaseURI).length > 0
                ? string(
                    abi.encodePacked(
                        currentBaseURI,
                        tokenId.toString(),
                        baseExtension
                    )
                )
                : "";
    }

    function setProvenanceHash(string memory provenanceHash) public onlyOwner {
        provenance_hash = provenanceHash;
    }

    function withdraw() public onlyOwner {
        uint256 _balance = address(this).balance;
        uint256 _split = _balance.mul(90).div(100);
        (bool sentCom, bytes memory data_com) = community.call{value: _split}(
            ""
        );
        require(sentCom, "Failed to send Ether");
        (bool sentDev, bytes memory data_dev) = dev.call{
            value: _balance.sub(_split)
        }("");
        require(sentDev, "Failed to send Ether");
    }
}
