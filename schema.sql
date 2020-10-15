drop table if exists "raw"."boxofficemojo_revenues";

create table "raw"."boxofficemojo_revenues" (
    DATA JSONB NOT NULL
);