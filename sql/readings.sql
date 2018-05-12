CREATE TABLE IF NOT EXISTS public.readings (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	inserted timestamp NULL,
	"month" text NULL,
	reading int4 NULL,
	consumption int4 NULL
)
WITH (
	OIDS=FALSE
) ;
