insert into Queues values(0, 0, 0);
insert into Queues values(1, 0, 0);
insert into Queues values(2, 0, 0);
insert into Queues values(3, 0, 0);
insert into QSettings values (0, 'tgr4', 10, 'thomas,seattle', 'seattle,uw', 1, null, null, null, null, 'What is your name?');
insert into QSettings values (1, 'portland', 10, 'portland,oregon', 'portland,oregon', 1, null, null, null, null, 'What is the something velocity of a swallow?');
insert into QSettings values (2, 'bestqueueever', 10, 'best,favorite', 'moon', 1, null, null, null, null, 'Party size:');
insert into QSettings values (3, 'RedRobin', 10, 'RedRobin,restaurant,food,covington', 'covington', 1, null, null, null, null, 'Party size:');
insert into QSettings values (4, 'NoQuestion', 20, 'NoQuestion', 'NoQuestion', 1, null, null, null, null, null);
insert into Users values (0, 0, 'Creator', 'Thomas', 'Rothschilds', 'tgr4@uw.edu', 'e6bef8e574ecd067037366b5ea67e6b72a6d765534068e004ce3c83b', 78540859);
insert into Users values (1, 0, 'Jim', 'Jim', 'Jim', 'jim@jim.jim', '1803f10da5d1a3bbe2f33af03f1d1d5c135b397977d0c2e772d0de50', 4168124163);
insert into Users values (2, 0, 'Boi', 'Boi', 'Boi', 'boi@boi.boi', 'eb4a4e0737763444a7143fd076c25ec6fa2831bd7cd08b33daf4180a', 681102815);
insert into Users values (3, 0, 'best', 'best', 'best', 'best@best.best', 'c8d164ef299540b40539367d3ec76e01e8b0fa16629274c3ca28a048', 1448604608);
insert into Users values(4, 0, 'Joe', 'Joe', 'Joe', 'Joe@Joe.Joe', 'de7b8577f5d8a483bc5a2bfefcd88fc8c002c0568f5803e167d606c6', 1746490568);
insert into Permissions values (0, 0, 3);
insert into Permissions values (0, 1, 3);
insert into Permissions values (0, 2, 3);
insert into Permissions values (0, 3, 1);
insert into Permissions values (1, 0, 1);
insert into Permissions values (1, 1, 3);
insert into Permissions values (1, 2, 1);
insert into Permissions values (3, 4, 3);
insert into Permissions values (4, 3, 3);
insert into QIndex values(0, 0, (select ending_index from Queues where id=0), 'Thomas');
update Queues set ending_index=ending_index+1 where id=0;
insert into QHistory values (0, 0, 1400884418, null);
insert into QIndex values(1, 0, (select ending_index from Queues where id=0), 'Which kind of swallow?');
update Queues set ending_index=ending_index+1 where id=0;
insert into QHistory values (1, 0, 1400884419, null);
insert into QIndex values(2, 1, (select ending_index from Queues where id=1), '10');
update Queues set ending_index=ending_index+1 where id=1;
insert into QHistory values (2, 1, 1400884429, null);
insert into QIndex values(1, 1, (select ending_index from Queues where id=1), '1125');
update Queues set ending_index=ending_index+1 where id=1;
insert into QHistory values (1, 1, 1400884450, null);
insert into QIndex values(4, 2, (select ending_index from Queues where id=2), '3');
update Queues set ending_index=ending_index+1 where id=2;
insert into QHistory values (4, 2, 1400885550, null);

