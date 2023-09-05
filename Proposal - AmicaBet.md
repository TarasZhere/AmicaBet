<center>

|Student|Class|Project Type|
|:---:|:-:|:---:|
|Taras Zherebetskyy|CISC 6080 - Capstone Project in Data Science [SWE Project]|Full-stack Web Application|

</center>

# AmicaBet Description
**AmicaBet** is a betting social network built with Flask. It allows users to bet on anything they want. Therefore, they can create custom bets and invite friends to accept their challenges. AmicaBet lets you create a custom bet with the following info:
- Event Title: (e.g. ["Arm wrestling," "100-yard sprint"] )
- Description: optional (e.g. ["How about you accept the challenge so we can see who's better at arm wrestling"])
- Bettors: (list of one or more friends to challenge)
- Ticket's price: (The number of tokens all bettors have to pay to accept the bet)

Once the bet is created, the app will automatically send a request to all friends involved, allowing them to accept or reject the challenge. If no one gets it, the bet is closed with no winner. The challenge begins if a chance is taken and there are at least two bettors. The app will automatically detract the ticket price from the user's balance.
## Tokens
The balance is expressed in tokens, a digital currency that all users can buy from the website's store. Users can withdraw the amount in USD when they have accumulated enough tokens (e.g., 100 tokens). The user can use the promotions only occasionally (otherwise, we have infinite glitch money).
**Why tokens and not just USD?** Tokens are free of charge to move around. Any time a bet is placed, tokens are exchanged from all bettors to the pool. Once a winner is chosen, the pool will be founded to the winner's balance. It's just easier.
**How is a winner chosen?** AmicaBet lets the bettors choose the winner, but it will listen to the majority of the votes to determine the winner. If there is no majority, the bet is **voided**. In a **voided** bet, the bettors are refunded only a percentage of the original ticket's price. This is to incentive users, to be honest, or they'll slowly lose balance.
Additionally, **AmicaBet** creates posts and updates the graph of friends about the challenges a user is creating. If a challenge is still available, a friend can request to join. All users can challenge all friends, and anyone can decide to participate after asking the creator of the bet.

## Core functionality: voided vs non-voided games

As the introductory paragraph explains, a <u>voided game is when a mutual agreement between users is not reached.</u> Therefore, someone has lied about the votes. The goal is to incentive people to be honest with their bets and for people who are open to betting only with other honest people. To do so, **AmicaBet** will collect user data, calculate a percentage of non-voided games' overall games, and display it under the user's profile.
<center>

### Sample diagram of a non-voided game

```mermaid
sequenceDiagram
Bob ->> AmicaBet: Challenge Alice & John in 100 yard run
AmicaBet ->> Bob: 100 yard run challenge, -30$
AmicaBet ->> Alice: 100 yard run challenge, -30$
AmicaBet ->> John: 100 yard run challenge, -30$
Bob -->> AmicaBet: I won
Alice --x AmicaBet: I won
John -->> AmicaBet: Bob won
AmicaBet ->> AmicaBet: Majority? Yes
AmicaBet ->> Bob: Here your +90$
AmicaBet ->> Alice: you lost
AmicaBet ->> John: you lost
```
### Sample diagram of a voided game
```mermaid
sequenceDiagram
Bob ->> AmicaBet: Challenge Alice & John in 100 yard run
AmicaBet ->> Bob: 100 yard run challenge, -30$
AmicaBet ->> Alice: 100 yard run challenge, -30$
AmicaBet ->> John: 100 yard run challenge, -30$
Bob --X AmicaBet: I won
Alice --x AmicaBet: I won
John --x AmicaBet: I won
AmicaBet ->> AmicaBet: Majority? No
AmicaBet ->> Bob: voided challenge, refound +29$
AmicaBet ->> Alice: voided challenge, refound +29$
AmicaBet ->> John: voided challenge, refound +29$
AmicaBet ->> AmicaBet: just erned 3$ 
```
</center>

# Technical Documentation
What building techs **AmicaBet** uses? This paragraph discusses what techs are used to build the webapp and what reason they have been chosen. 
## Tech Stack
The full development stack is:

 1. **Flask**, a web framework that uses python as core to manage HTTP requests and Database to create dynamic web pages
 2. **Bootstrap 5** to style web pages in a simple and quick manner
 3. **SQLite3** is a Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL
 4.  more ...

## Software Architecture
<center>

![ABArchitecture (1).png](../_resources/ABArchitecture%20%281%29.png)

</center>

# Capabilities
AmicaBet is currently under development. Some features have already been implemented, while others are still in progress. Below is a comprehensive list of completed ✅ and pending features:
## Registration / Login
- [x] Responsive UI
- [x] Register Users
- [x] Login Users
- [x] Security: Server checks if inputs *[email, password, ...]* are valid
- [ ] Code refactoring for improvement

## Database
- [x] SQLite Integration
- [x] Database Normalization
- [x] Switching to MySql Database 
- [ ] Code refactoring for improvement

## User Interaction
- [ ] Responsive UI
- [x] Friend request to other users
- [x] Accept/Reject incoming requests
- [x] Search Users by name
- [x] Challenge a friend in bets
- [x] Accept/Reject bets
- [x] Vote winner during bet
- [ ] Push notification when receiving a friend request
- [ ] Friends can see your bets
- [ ] Friends can request to join bets
- [ ] Data analytics 
- [ ] Code refactoring for improvement
- [ ] Purches Tokens
- [ ] Withdraw USD

## Bets
- [x] Sort bets by current state *[accepted, rejiected, voided, won, lost]*
- [x] Voting in bet
- [x] Mutual Agreement algorithm [decides the winer]
- [ ] Schedule a deadline for the bet
- [ ] push notifications when receiving a bet request
- [ ] Code refactoring for improvement

## Deployment
- [x] Docker file 
- [ ] kubernetes file
- [ ] Google Cloud Deployment
- [ ] Different Deployment [Eventually for cheaper solution]

## Others
- [ ] Software Engineering Documentation

Certainly, here are five sample rows of data for the "Bet" table:

| Bid  | Title          | Description                | Ticket | Pool    | Status    |
|------|----------------|----------------------------|--------|---------|-----------|
| 1    | Football Match | Predict the winner         | 3 | 6  | Running      |
| 2    | Horse Race     | Bet on the fastest horse   | 4 | 8   | Closed    |
| 3    | Basketball     | Total points over/under     | 4 | 4  | Pending   |
| 4    | Poker Night    | Place your poker hand bet  | 5 | 10  | Running      |
| 5    | Tennis Match   | Predict the set outcomes   | 2 | 4   | Closed    |
| 6    | Cricket Match   | Guess the winning margin     | 3 | 6   | Running      |
| 7    | Slot Machine    | Spin for a chance to win     | 10 | 20   | Closed    |
| 8    | Soccer Penalty  | Predict the shooter's side   | 10 | 10    | Pending   |

Remember that these examples are fabricated for demonstration purposes and may not reflect real-world data accurately.