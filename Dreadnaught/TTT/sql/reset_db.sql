use Dreadnaught;

delete from TTT_game;
delete from TTT_scripts;
delete from TTT_users;


alter table TTT_game AUTO_INCREMENT = 1;
alter table TTT_scripts AUTO_INCREMENT = 1;
alter table TTT_users AUTO_INCREMENT = 1;
