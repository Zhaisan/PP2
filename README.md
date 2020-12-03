19B030552.py DAR tanks


![3c0c935d-c623-47d7-9204-9be11bf6b9fe_photo-resizer ru](https://user-images.githubusercontent.com/57716933/101046635-654a9b00-35ab-11eb-98f1-7b70d9e7aab3.png)

Welcome to DAR tanks! 
This project is dedicated to server of tanks game that is hosted by DAR Tech and available to anyone interested. The server employs client-server model. Using current documentation a client can make calls and interact with the server. Enjoy the game!

Game concepts
rooms – there are 30 game rooms available to players. One client can play only in one room. Room IDs are as follows: room-1, room-2, …, room-30 Maximum 12 tanks may join a room at any given time

game field – each room has one game field. Game field is 2D field with width and height. Tanks and bullets are located on the game field

timed rounds – in order to avoid endless games and to make the game rapid, games are run in rounds

a round starts when game field is empty and a new player joins the game via registration

each round lasts 120 seconds (2 minutes)

when round ends, if there are players left on the game field, losers are winners are decided

authentication – before starting the game, a client must register on the server and receive a token. Client should use that token when sending commands to server

tank – tank is a moving object in the game. One player can control only 1 tank. Player’s goal is to score points by firing bullets and hitting opponents

bullet – bullet is a moving object in the game that is fired by a tank. A player can send a request to DAR tanks to fire a bullet. In order to limit unfair play, each tank is limited to fire one bullet per second

hit – a hit happens when a bullet collides with a tank that is not the owner of the bullet. Tank cannot hit itself with a bullet, it can hit opponents. When hit, tank loses health and bullet that hit the tank disappears

loser – loser is tank whose health decreased and changed to zero. When losing the game, tank’s corresponding session is closed and player can no longer control the tank

winner – a tank can win in the following conditions:

when it is the last tank left on the game field and score is bigger than or equal to 3

when game timed round ends, and the tank has the highest score. If there are multiple tanks left with same maximum score, then the winners are tanks that have more health points

kicked – a tank is kicked from the game if does not send any commands for 30 seconds. This done in order to avoid unfair score farming and freeing player slots if the player is AFK (away from keyboard). When tank is kicked, tank’s token is deleted and player can no longer control the tank

RabbitMQ client-server architecture
RabbitMQ in DAR tanks consists of one topic exchange called X:routing.topic. DAR tanks server has a server queue that binds to X:routing.topic via binding-keys of AMQP endpoints. In order to send a request to DAR tanks server, a client must produce a message to X:routing.topic with proper body and routing-key. It is strongly advised to review RPC tutorial to recall how client-server model is implemented in RabbitMQ. General design of client-server interaction in DAR tanks looks as follows:

