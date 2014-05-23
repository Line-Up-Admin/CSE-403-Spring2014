PRAGMA foreign_keys = ON;
CREATE TABLE Users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	temp int,
	uname varchar(32),
	fname varchar(20),
	lname varchar(20),
	email varchar(32),
	pw varchar(32)
);

CREATE TABLE Queues (
	id int PRIMARY KEY,
	starting_index int,
	ending_index int
);

CREATE TABLE QSettings (
	qid INTEGER PRIMARY KEY AUTOINCREMENT,
	qname varchar(32),
	max_size int,
	keywords varchar(256),
	location varchar(64),
	active int,
	FOREIGN KEY (qid) REFERENCES Queues(id)
);

CREATE TABLE QIndex (
	uid int,
	qid int,
	relative_position int,
	optional_data varchar (256),
	PRIMARY KEY (uid, qid),
	FOREIGN KEY (uid) REFERENCES Users(id),
	FOREIGN KEY (qid) REFERENCES Queues(id)
);

/* This table stores administrator, employee, and blocked users. */
CREATE TABLE Permissions (
	pid int,
	qid int,
	permission_level int,
	PRIMARY KEY (pid, qid),
	FOREIGN KEY (pid) REFERENCES Users(id),
	FOREIGN KEY (qid) REFERENCES Queues(id)
);
