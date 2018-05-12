CREATE TABLE IF NOT EXISTS public.bill_history (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	inserted timestamp NULL,
	bill_date date NULL,
	amount money NULL
)
WITH (
	OIDS=FALSE
) ;
