CREATE TABLE IF NOT EXISTS "otzyvua" (
	"id" varchar(50) NOT NULL,
	"title" text,
    "date" varchar(50),
    "text" text,
    "phone" varchar(50),
    "advantages" text[],
    "disadvantages" text[],
    "images" text[],
	CONSTRAINT "otzyvua_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

-- CREATE TABLE IF NOT EXISTS "devices" (
-- 	"id" serial NOT NULL,
-- 	"name" varchar(50) NOT NULL,
-- 	"ip" varchar(50) NOT NULL,
--     "status" varchar(50),
-- 	"do_not_disturb" BOOLEAN NOT NULL,
-- 	"notify" BOOLEAN NOT NULL DEFAULT TRUE,
-- 	"change_date" timestamp NOT NULL,
-- 	"user_id" bigint NOT NULL,
--     "last_check" timestamp NOT NULL,
-- 	CONSTRAINT "devices_pk" PRIMARY KEY ("id"),
--     CONSTRAINT "devices_fk0"
--     FOREIGN KEY ("user_id")
--     REFERENCES "users" ("user_id")
--     ON DELETE CASCADE
-- ) WITH (
--   OIDS=FALSE
-- );
