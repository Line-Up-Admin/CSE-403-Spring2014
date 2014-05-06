CREATE TABLE Users (
	id int PRIMARY KEY,
	temp int,
	uname varchar(32),
	fname varchar(20),
	lname varchar(20),
	email varchar(32),
	pw varchar(32)
);

CREATE TABLE QSettings (
	id int PRIMARY KEY,
	qname varchar(32),
	max_size int,
	keywords varchar(256),
	location varchar(64),
	active int
);

CREATE TABLE QIndex (
	uid int,
	qid int,
	optionalData varchar (256),
	PRIMARY KEY (uid, qid),
	FOREIGN KEY (uid) REFERENCES Users(id),
	FOREIGN KEY (qid) REFERENCES QSettings(id)
);

/* This table stores administrator, employee, and blocked users. */
CREATE TABLE Permissions (
	pid int,
	qid int,
	permissionLevel int,
	PRIMARY KEY (pid, qid),
	FOREIGN KEY (pid) REFERENCES Users(id),
	FOREIGN KEY (qid) REFERENCES QSettings(id)
);
