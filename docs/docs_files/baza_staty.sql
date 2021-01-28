

# skrypt do tworzenia potrzebnych rzeczy do statystyk 

# uwaga: tabela `auth_user` ktora wykorzustuje 1sza procedura jest tworzona przez 
# django i jej tu nie ma (lecz jest testowa do odkomentowania)

create database if not exists `ZMIEN_MNIE`;

use ZMIEN_MNIE;

#

drop table if exists stat_player_game;

CREATE TABLE IF NOT EXISTS `stat_player_game`(
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `game_id` int NOT NULL,
  `player_points` int NOT NULL,
  `team` enum('red', 'blue') NOT NULL,
  `vehicle` enum('walk', 'bike', 'car') not null,
  `distance` int DEFAULT NULL,
  `team_points` int DEFAULT NULL,
  `map` varchar(30) DEFAULT NULL,
  `won` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);

#

drop table if exists top_players;

CREATE TABLE IF NOT EXISTS `top_players`(
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `nick` varchar(100) not null,
  `games_won` int DEFAULT NULL,
  `percent_won` int DEFAULT NULL,
  `avg_points` float(7,2) DEFAULT NULL,
  `contribution` float(7,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

#

# to co procedura recount_players_top ale dla wszystkich, recznie
/*
insert into top_players(player_id, nick, games_won, percent_won, avg_points, contribution) 
	select 
		player_id,
		players.nick as Nick, 
		SUM(stat_player_game.won) as 'Liczba wygranych', 
        avg(won)*100 as 'Procent wygranych',
        avg(player_points) as 'Średnia punktów',
        avg(player_points)/avg(team_points) as 'Wkład w druzynę'
	
    from stat_player_game 
    join players on players.id=stat_player_game.player_id
    group by player_id;
*/


# testowa tabelka, taka jak będzie utworzona przez django dla graczy
/*
create table if not exists `auth_user` (
	`id` int not null auto_increment,
    `username` varchar(100) not null,
    primary key (`id`)
);
*/

drop procedure if exists recount_player_top;

DELIMITER //
CREATE PROCEDURE recount_player_top(in in_id int)
BEGIN
	declare g_won, p_won int;
    declare a_points, contr float;
    declare temp_nick varchar(30);
    
    select nick into temp_nick from top_players where player_id=in_id;
    
    if temp_nick is NULL then
		insert into top_players (player_id, nick) select 
			player_id,
			auth_user.username
		from stat_player_game 
        join auth_user on auth_user.id = stat_player_game.player_id
        where stat_player_game.player_id = in_id
        limit 1;

	end if;
            
    select 
		SUM(stat_player_game.won), 
        avg(won)*100,
        avg(player_points),
        avg(player_points)/avg(team_points)
        
	into g_won, p_won, a_points, contr 
    from stat_player_game 
    where player_id = in_id
    group by player_id;
    
    update top_players set 
		games_won = g_won,
        percent_won = p_won,
        avg_points = a_points,
        contribution = contr 
	where top_players.player_id = in_id;
    
END//
DELIMITER ;

#

drop trigger if exists recount_player_top_trigger;

DELIMITER //
create trigger recount_player_top_trigger after insert on stat_player_game for each row
BEGIN
	
    call recount_player_top(NEW.player_id);
    
END//
DELIMITER ;

#

drop table if exists stat_map_game;

CREATE TABLE IF NOT EXISTS `stat_map_game`(
  `id` int NOT NULL AUTO_INCREMENT,
  `game_id` int NOT NULL,
  `map` varchar(30) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `team_red_points` int NOT NULL,
  `team_blue_points` int NOT NULL,
  `team_won` enum('red', 'blue') DEFAULT NULL,
  PRIMARY KEY (`id`)
);

#

drop table if exists top_map;

CREATE TABLE IF NOT EXISTS `top_map`(
  `id` int NOT NULL AUTO_INCREMENT,
  `map` varchar(30) NOT NULL,
  `no_of_games` int,
  `avg_time` time,
  `max_points_team` int,
  `avg_points` float,
  PRIMARY KEY (`id`)
);

#

drop procedure if exists populate_top_map;

DELIMITER //
CREATE PROCEDURE populate_top_map()
BEGIN

	declare t_map varchar(30);
	declare t_no_of_games, t_max_points_team, t_red_points, t_blue_points int;
	declare t_avg_time time;
	declare t_start_time, t_end_time datetime;
	declare t_avg_points float;

	DECLARE mapax varchar(30);
    
    declare done Bool default false;
    declare my_cursor cursor for 
    select distinct map from stat_map_game;
    
    declare continue HANDLER for not found set done = true;
    
    open my_cursor;
    fetch next from my_cursor into mapax;
    
    delete from top_map where id >= 0;
    
    while done = false
    do
		select mapax;
        set @sel_map = mapax;
        
        # ilosc gier
        set t_no_of_games = (select count(*) from stat_map_game where map like @sel_map group by map);
        select t_no_of_games;
        # max punktow
        set t_red_points = (select max(team_red_points) from stat_map_game where map like @sel_map group by map);
        set t_blue_points = (select max(team_blue_points) from stat_map_game where map like @sel_map group by map);
        
        if t_red_points > t_blue_points then
			set t_max_points_team = t_red_points;
		else
			set t_max_points_team = t_blue_points;
		end if;
        
        select t_max_points_team;
        
        # srednio pkt na gre
        set t_red_points = (select sum(team_red_points) from stat_map_game where map like @sel_map group by map);
        set t_blue_points = (select sum(team_blue_points) from stat_map_game where map like @sel_map group by map);
        
        set t_avg_points = (t_red_points + t_blue_points) / (t_no_of_games * 2);
        select t_avg_points;
        
        # sredni czas
        set t_avg_time = (select avg(timediff(end_time, start_time)) from stat_map_game where map like @sel_map group by map);
        select t_avg_time;
        
        # do tabeli
        
        insert into top_map(map, no_of_games, avg_time, max_points_team, avg_points) values
        (
			mapax,
            t_no_of_games,
            t_avg_time,
            t_max_points_team,
            t_avg_points
		);
        
        fetch next from my_cursor into mapax;
	end while;
    
END//
DELIMITER ;

#

set global event_scheduler = ON;

drop event if exists top_map_event;

create event top_map_event on SCHEDULE EVERY 1 HOUR DO 
	call populate_top_map();



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    