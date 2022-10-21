// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.12;

//Owner set the X ETH fee and list of candidates

contract BallotV {

    address immutable owner;
    uint immutable deployDate;
    mapping (address => uint256) public CountVote;
    address[] public candidateListNames;
    uint Payment; //X wei
    uint VoitingCommision; //F
    uint Duration; //D

    constructor() { 
        owner = msg.sender;
        deployDate = block.timestamp;
    }
    function getDuration() view public returns (uint){
        return Duration;
    }


//create a ballot
    modifier onlyOwner() {
        require(msg.sender == owner, "You are not an owner!");
        _;
    }
    function CreateVoting (uint duration_, uint voiting_commission, uint payment_, address[] memory candidateNames) external onlyOwner{
        Payment = payment_ ;
        VoitingCommision = voiting_commission;
        Duration = duration_;
        for(uint i = 0; i < candidateNames.length; i++) {
            candidateListNames.push(candidateNames[i]);
        }
    }


//vote_functions 
    function VoteFor(address candidate) external payable {
        require(validCandidate(candidate), "Wrong candidate");
        require(validFee(msg.value), "Wrong fee value");
        require(timeIsOvercheck(), "Time is over!");
        CountVote[candidate] += 1;
    }

    function validCandidate(address candidate) view public returns (bool) {
        for(uint i = 0; i < candidateListNames.length; i++) {
            if (candidateListNames[i] == candidate) {
                return true;
            }
        }
        return false;
    } 
    function validFee(uint fee) view public returns (bool) {
        return fee == Payment ? true : false;
    }
    function timeIsOvercheck() view public returns (bool) {
        return block.timestamp < (deployDate + Duration * 1 days);
    }


//check time and get results
    modifier timeIsOver(){ 
            require(block.timestamp >= (deployDate + Duration * 1 days), "Time is not up");
            _;
    }
    function ResultsWhenTimeIsUp() external timeIsOver {
        address Winner = address(0); 
        uint CountWin = 0;
        uint IterWin;
            for(uint i = 0; i < candidateListNames.length; i++) {
                if (CountVote[candidateListNames[i]] > CountWin) {
                    Winner = candidateListNames[i];
                    CountWin = CountVote[candidateListNames[i]];
                    IterWin = i;
                }
        }
        if(Winner != address(0)){
            address payable _to = payable(candidateListNames[IterWin]);
            address _thisConstract = address(this);
            _to.transfer( _thisConstract.balance * (1 ether - VoitingCommision));
        }
        
    }


//withdraw fees
    modifier timeIsOverandonlyOwner(){ 
            require(block.timestamp < (deployDate + Duration * 1 days), "Wait, the voting has not finished.");
            require(msg.sender == owner, "You can not withdraw fees, you are not an owner!");
            _;
    }
    function withdrawFees() external payable timeIsOverandonlyOwner{
        address payable _to = payable(owner);
        address _thisConstract = address(this);
        _to.transfer( _thisConstract.balance * (VoitingCommision));
    }

    
// get information
    function getVoteInfo() pure public returns (string memory) {
        string memory str =  "You can vote for candidates by sending X ETH. ";
        return str;
    }
//test functions
    function currentBalance() view public returns (uint256) {
        return address(this).balance;
    }
}
