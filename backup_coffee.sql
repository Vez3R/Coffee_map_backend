--
-- PostgreSQL database cluster dump
--

-- Started on 2024-12-12 23:33:08

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:5U+6Qk/0QlejKh4WcW8P2A==$VdfoULUirEzv0yKNaZ0iNzo301cf086ZKOUojkUrcog=:ih33A3AsDImItyMYbnCN3mYfpLTQ2AcYLgm0kg+DywQ=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6
-- Dumped by pg_dump version 16.3

-- Started on 2024-12-12 23:33:09

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2024-12-12 23:33:09

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6
-- Dumped by pg_dump version 16.3

-- Started on 2024-12-12 23:33:09

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 4859 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- TOC entry 230 (class 1255 OID 16452)
-- Name: rate_function(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.rate_function() RETURNS trigger
    LANGUAGE plpgsql
    AS $$DECLARE
  average_rate REAL;
BEGIN
  -- Получаем среднюю оценку для кафе из user_rate
  SELECT AVG(rate) INTO average_rate
  FROM user_review
  WHERE cafe_id = NEW.cafe_id;

  -- Обновляем оценку кафе в таблице cafe
  UPDATE cafe
  SET rate = average_rate -- Используем 0, если оценок нет
  WHERE id = NEW.cafe_id;

  RETURN NEW;
END;
$$;


ALTER FUNCTION public.rate_function() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16411)
-- Name: cafe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cafe (
    id uuid NOT NULL,
    description text NOT NULL,
    metro text NOT NULL,
    rate real,
    image_link text NOT NULL,
    cafe_name text NOT NULL
);


ALTER TABLE public.cafe OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16404)
-- Name: user_review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_review (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    cafe_id uuid NOT NULL,
    comment text NOT NULL,
    rate smallint NOT NULL,
    CONSTRAINT rate_check CHECK (((rate >= 1) AND (rate <= 5)))
);


ALTER TABLE public.user_review OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16397)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    login text NOT NULL,
    password text NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 4853 (class 0 OID 16411)
-- Dependencies: 218
-- Data for Name: cafe; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cafe (id, description, metro, rate, image_link, cafe_name) FROM stdin;
61f0c404-5cb3-11e7-907b-a6052ad3dba0	Что-то	Сокольники	4	ссылка	кек
61f0c404-5cb3-11e7-907b-a6006ad3dba0	лол кек	Лубянка	4	ссылка	лол
\.


--
-- TOC entry 4852 (class 0 OID 16404)
-- Dependencies: 217
-- Data for Name: user_review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_review (id, user_id, cafe_id, comment, rate) FROM stdin;
61f0c404-5cb3-11e7-907b-a6006ad3dba7	61f0c404-5cb3-11e7-907b-a6006ad3dba2	61f0c404-5cb3-11e7-907b-a6006ad3dba0	dfkgdlfg	5
61f0c404-5cb3-11e7-907b-a6006ad3dba3	61f0c404-5cb3-11e7-907b-a6006ad3dba2	61f0c404-5cb3-11e7-907b-a6006ad3dba0	kjk	3
\.


--
-- TOC entry 4851 (class 0 OID 16397)
-- Dependencies: 216
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, login, password, name) FROM stdin;
61f0c404-5cb3-11e7-907b-a6006ad3dba2	Vlad	12345	Владислав
61f0c404-5cb3-11e7-907b-a6006ad3dba9	Liza	12345	Елизавета
0e6bbbff-728f-458f-998c-d022d56fbd81	Roma	scrypt:32768:8:1$zpMmmMI7EPuIQheI$c298095960c0e3d4432bd6cd2d51d9e031d3349f74ea43e10d4c3c3734ca01e493bb088838994dd3a7a511b6c2fdc29c1a21d334b42ecdc1f2ab6227dde61e9e	Роман
\.


--
-- TOC entry 4704 (class 2606 OID 16417)
-- Name: cafe cafe_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cafe
    ADD CONSTRAINT cafe_pkey PRIMARY KEY (id);


--
-- TOC entry 4698 (class 2606 OID 16429)
-- Name: cafe rate_check; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public.cafe
    ADD CONSTRAINT rate_check CHECK (((rate >= (1)::double precision) AND (rate <= (5)::double precision))) NOT VALID;


--
-- TOC entry 4702 (class 2606 OID 16410)
-- Name: user_review user_review_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_review
    ADD CONSTRAINT user_review_pkey PRIMARY KEY (id);


--
-- TOC entry 4700 (class 2606 OID 16403)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4707 (class 2620 OID 16453)
-- Name: user_review rate_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER rate_trigger AFTER INSERT OR DELETE OR UPDATE OF rate ON public.user_review FOR EACH ROW EXECUTE FUNCTION public.rate_function();


--
-- TOC entry 4705 (class 2606 OID 16423)
-- Name: user_review cafe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_review
    ADD CONSTRAINT cafe_id_fkey FOREIGN KEY (cafe_id) REFERENCES public.cafe(id) NOT VALID;


--
-- TOC entry 4706 (class 2606 OID 16418)
-- Name: user_review user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_review
    ADD CONSTRAINT user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) NOT VALID;


-- Completed on 2024-12-12 23:33:10

--
-- PostgreSQL database dump complete
--

-- Completed on 2024-12-12 23:33:10

--
-- PostgreSQL database cluster dump complete
--

