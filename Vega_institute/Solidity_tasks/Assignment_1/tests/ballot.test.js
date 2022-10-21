// Right click on the script name and hit "Run" to execute
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("BallotV", function () {
    let add1 //owner
    let add2 //address in list
    let add3 //address in list
    let add4 //address out of list
    let payments
    let list
    beforeEach(async function () {
        [add1, add2, add3, add4] = await ethers.getSigners()
        const Payments = await ethers.getContractFactory("BallotV", add1)
        list = [add2.getAddress(), add3.getAddress()]
        payments = await Payments.deploy()
        await payments.deployed()
        console.log(payments.address)
    })
    it("should be deployed", async function () {
        console.log("success!!")
        expect(payments.address).to.be.properAddress
    });
    it("should have 0 ether by default", async function () {
        const balance = await payments.currentBalance()
        console.log(payments.currentBalance())
        expect(balance).to.eq(0)
    });
    it("should be possible to call CreateVoting only for owner, otherwise you will get 'You are not an owner!'.", async function () {
        await expect(payments.connect(add4).CreateVoting(1,2,3, list))
             .to.be.revertedWith("You are not an owner!");
    });
    it("should be possible to vote for the candidate only from list, otherwise you will get 'Wrong candidate'.", async function () {
        await expect(payments.connect(add4).VoteFor(add1.getAddress()))
             .to.be.revertedWith("Wrong candidate");
    });
    it("should be possible to vote only with X wei, otherwise you will get 'Wrong fee value'.", async function () {
        await payments.connect(add1).CreateVoting(1, 2, 3, list)
        await expect(payments.connect(add4).VoteFor(add2.getAddress(), { value: 4 }))
             .to.be.revertedWith("Wrong fee value");
    });
    it("should be possible to vote only with X wei.", async function () {
        await payments.connect(add1).CreateVoting(1, 2, 3, list)
        await payments.connect(add4).VoteFor(add2.getAddress(), { value: 3}) 
        const balance = await payments.currentBalance()
        console.log(payments.currentBalance())
        expect(balance).to.eq(3)
        console.log(balance)
    });
    it("should be possible to withdraw fees only for owner, otherwise you will get 'You can not withdraw fees, you are not an owner!'.", async function () {
        await expect(payments.connect(add4).withdrawFees())
             .to.be.revertedWith("You can not withdraw fees, you are not an owner!");
    });
})
