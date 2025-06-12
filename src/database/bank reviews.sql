drop table tbl_reviews cascade constraints;
create table tbl_banks (
   id   number
      generated always as identity
   primary key,
   name varchar2(100) unique not null
);

-- Then create the reviews table
create table tbl_reviews (
   id              number
      generated always as identity
   primary key,
   bank_id         number
      references tbl_banks ( id ),
   rating          number(2,1),
   review_date     date,
   review_text     clob,
   sentiment_label varchar2(20),
   sentiment_score float,
   themes          clob,
   source          varchar2(50)
);
alter table tbl_banks add app_id varchar2(100);