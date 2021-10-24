pragma solidity >=0.7.0 <0.9.0;

contract RetroMall  {
   
    struct Coupon {
        uint discount; // weight is accumulated by delegation
        string brand;  // if true, that person already voted
        address addr; // person delegated to
    }


    address public owner;
    
    mapping (address => uint) public ownerTicketCount;
    mapping (uint => Coupon) public idToCoupons;
    
    
    uint public currentIndex = 0;


    modifier onlyOwnerOf(address _addr) {
        require(_addr == owner);
        _;
    }
    
    constructor() public {
        owner = msg.sender;
    }
    
    
    function transferOwnership(address newOwner) external onlyOwnerOf(msg.sender) {
        owner = newOwner;
        
    }
    
    function giveCouponTo(string memory brand, uint discount, address newOwner) external onlyOwnerOf(msg.sender) {
        Coupon memory newCoupon = Coupon(discount, brand, newOwner);
        idToCoupons[currentIndex] = newCoupon;
        currentIndex++;
        ownerTicketCount[newOwner]++;
    }

    function balanceOf(address _owner) public view returns (uint256 _balance){
        _balance = ownerTicketCount[_owner];
    }
    
    function ownerOf(uint256 _tokenId) public view returns (address _owner) {
        _owner = idToCoupons[_tokenId].addr;
    }

    function brandOf(uint256 _tokenId) public view returns (string memory data) {
        data = idToCoupons[_tokenId].brand;
    }
    
    function discountOf(uint256 _tokenId) public view returns (uint data) {
        data = idToCoupons[_tokenId].discount;
    }
    
    function transfer(address _to, uint256 _tokenId) public {
        require( idToCoupons[_tokenId].addr == msg.sender);
        idToCoupons[_tokenId].addr = _to;
        ownerTicketCount[_to]++;
        ownerTicketCount[msg.sender]--;
    }
    
}
