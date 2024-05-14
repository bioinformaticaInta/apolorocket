--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alignment; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.alignment (
    id integer NOT NULL,
    query_region_block_id integer,
    reference_region_block_id integer,
    strand character(1),
    missmatches integer,
    alignment_block_number integer
);


ALTER TABLE public.alignment OWNER TO sgonzalez;

--
-- Name: alignment_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.alignment ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.alignment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: efficiency; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.efficiency (
    id integer NOT NULL,
    query_id integer,
    method character varying(50) NOT NULL,
    efficiency_data integer[] NOT NULL
);


ALTER TABLE public.efficiency OWNER TO sgonzalez;

--
-- Name: efficiency_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.efficiency ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.efficiency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: maintarget_comparison; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.maintarget_comparison (
    id integer NOT NULL,
    project_id integer,
    query_region_id integer
);


ALTER TABLE public.maintarget_comparison OWNER TO sgonzalez;

--
-- Name: maintarget_comparison_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.maintarget_comparison ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.maintarget_comparison_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: maintarget_comparison_reference; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.maintarget_comparison_reference (
    id integer NOT NULL,
    maintarget_comparison_id integer,
    reference_id integer
);


ALTER TABLE public.maintarget_comparison_reference OWNER TO sgonzalez;

--
-- Name: maintarget_comparison_reference_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.maintarget_comparison_reference ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.maintarget_comparison_reference_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: maintarget_comparison_reference_region; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.maintarget_comparison_reference_region (
    id integer NOT NULL,
    maintarget_comparison_reference_id integer,
    target_number integer NOT NULL,
    reference_region_id integer,
    maintarget boolean
);


ALTER TABLE public.maintarget_comparison_reference_region OWNER TO sgonzalez;

--
-- Name: maintarget_comparison_reference_region_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.maintarget_comparison_reference_region ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.maintarget_comparison_reference_region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: offtarget_comparison; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.offtarget_comparison (
    id integer NOT NULL,
    project_id integer,
    query_region_id integer,
    selected_region boolean DEFAULT false NOT NULL
);


ALTER TABLE public.offtarget_comparison OWNER TO sgonzalez;

--
-- Name: offtarget_comparison_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.offtarget_comparison ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.offtarget_comparison_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: offtarget_comparison_reference; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.offtarget_comparison_reference (
    id integer NOT NULL,
    offtarget_comparison_id integer,
    reference_id integer
);


ALTER TABLE public.offtarget_comparison_reference OWNER TO sgonzalez;

--
-- Name: offtarget_comparison_reference_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.offtarget_comparison_reference ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.offtarget_comparison_reference_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: offtarget_comparison_reference_region; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.offtarget_comparison_reference_region (
    id integer NOT NULL,
    offtarget_comparison_reference_id integer,
    target_number integer NOT NULL,
    reference_region_id integer
);


ALTER TABLE public.offtarget_comparison_reference_region OWNER TO sgonzalez;

--
-- Name: offtarget_comparison_reference_region_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.offtarget_comparison_reference_region ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.offtarget_comparison_reference_region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: project; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.project (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    genus character varying(50) NOT NULL,
    specie character varying(50) NOT NULL,
    user_name character varying(50) NOT NULL,
    initial_date date NOT NULL,
    last_modification_date date
);


ALTER TABLE public.project OWNER TO sgonzalez;

--
-- Name: project_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.project ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: query; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.query (
    id integer NOT NULL,
    name text NOT NULL,
    sequence text NOT NULL
);


ALTER TABLE public.query OWNER TO sgonzalez;

--
-- Name: query_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.query ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.query_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: query_region; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.query_region (
    id integer NOT NULL,
    query_id integer,
    start_position integer NOT NULL,
    end_position integer NOT NULL
);


ALTER TABLE public.query_region OWNER TO sgonzalez;

--
-- Name: query_region_block; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.query_region_block (
    id integer NOT NULL,
    query_region_id integer,
    start_position integer NOT NULL,
    end_position integer NOT NULL
);


ALTER TABLE public.query_region_block OWNER TO sgonzalez;

--
-- Name: query_region_block_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.query_region_block ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.query_region_block_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: query_region_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.query_region ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.query_region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reference; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.reference (
    id integer NOT NULL,
    genus character varying(50) NOT NULL,
    specie character varying(50) NOT NULL,
    version character varying(50) NOT NULL,
    annotation boolean DEFAULT false NOT NULL,
    genomic boolean NOT NULL
);


ALTER TABLE public.reference OWNER TO sgonzalez;

--
-- Name: reference_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.reference ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.reference_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reference_region; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.reference_region (
    id integer NOT NULL,
    reference_id integer,
    sequence_name text NOT NULL,
    start_position integer NOT NULL,
    end_position integer NOT NULL,
    annotation text
);


ALTER TABLE public.reference_region OWNER TO sgonzalez;

--
-- Name: reference_region_block; Type: TABLE; Schema: public; Owner: sgonzalez
--

CREATE TABLE public.reference_region_block (
    id integer NOT NULL,
    reference_region_id integer,
    start_position integer NOT NULL,
    end_position integer NOT NULL
);


ALTER TABLE public.reference_region_block OWNER TO sgonzalez;

--
-- Name: reference_region_block_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.reference_region_block ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.reference_region_block_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reference_region_id_seq; Type: SEQUENCE; Schema: public; Owner: sgonzalez
--

ALTER TABLE public.reference_region ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.reference_region_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: alignment; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.alignment (id, query_region_block_id, reference_region_block_id, strand, missmatches, alignment_block_number) FROM stdin;
\.


--
-- Data for Name: efficiency; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.efficiency (id, query_id, method, efficiency_data) FROM stdin;
\.


--
-- Data for Name: maintarget_comparison; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.maintarget_comparison (id, project_id, query_region_id) FROM stdin;
\.


--
-- Data for Name: maintarget_comparison_reference; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.maintarget_comparison_reference (id, maintarget_comparison_id, reference_id) FROM stdin;
\.


--
-- Data for Name: maintarget_comparison_reference_region; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.maintarget_comparison_reference_region (id, maintarget_comparison_reference_id, target_number, reference_region_id, maintarget) FROM stdin;
\.


--
-- Data for Name: offtarget_comparison; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.offtarget_comparison (id, project_id, query_region_id, selected_region) FROM stdin;
\.


--
-- Data for Name: offtarget_comparison_reference; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.offtarget_comparison_reference (id, offtarget_comparison_id, reference_id) FROM stdin;
\.


--
-- Data for Name: offtarget_comparison_reference_region; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.offtarget_comparison_reference_region (id, offtarget_comparison_reference_id, target_number, reference_region_id) FROM stdin;
\.


--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.project (id, name, description, genus, specie, user_name, initial_date, last_modification_date) FROM stdin;
1	project1	Project test one	A	A	sergio	2024-05-13	2024-05-13
2	project2	Project test two	A	A	sergio	2024-05-13	2024-05-13
3	project3	Project test three	A	A	sergio	2024-05-13	2024-05-13
4	project4	Project testi four	A	A	sergio	2024-05-13	2024-05-13
5	project5	Project test five	A	A	sergio	2024-05-13	2024-05-13
\.


--
-- Data for Name: query; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.query (id, name, sequence) FROM stdin;
\.


--
-- Data for Name: query_region; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.query_region (id, query_id, start_position, end_position) FROM stdin;
\.


--
-- Data for Name: query_region_block; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.query_region_block (id, query_region_id, start_position, end_position) FROM stdin;
\.


--
-- Data for Name: reference; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.reference (id, genus, specie, version, annotation, genomic) FROM stdin;
1	Arabidopsis	thaliana	1.0	t	t
2	Homo	sapiens	38	t	t
3	Arabidopsis	thaliana	1.0	t	f
4	Botrytis	cinerea	5.10	t	t
5	Homo	sapiens	38	t	f
6	Botrytis	cinerea	5.10	t	f
7	Oryza	sativa	20	t	t
8	Oryza	sativa	20	t	f
9	Drosophila	melanogaster	3.2	t	t
10	Drosophila	melanogaster	3.2	t	f
\.


--
-- Data for Name: reference_region; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.reference_region (id, reference_id, sequence_name, start_position, end_position, annotation) FROM stdin;
\.


--
-- Data for Name: reference_region_block; Type: TABLE DATA; Schema: public; Owner: sgonzalez
--

COPY public.reference_region_block (id, reference_region_id, start_position, end_position) FROM stdin;
\.


--
-- Name: alignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.alignment_id_seq', 1, false);


--
-- Name: efficiency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.efficiency_id_seq', 1, false);


--
-- Name: maintarget_comparison_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.maintarget_comparison_id_seq', 1, false);


--
-- Name: maintarget_comparison_reference_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.maintarget_comparison_reference_id_seq', 1, false);


--
-- Name: maintarget_comparison_reference_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.maintarget_comparison_reference_region_id_seq', 1, false);


--
-- Name: offtarget_comparison_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.offtarget_comparison_id_seq', 1, false);


--
-- Name: offtarget_comparison_reference_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.offtarget_comparison_reference_id_seq', 1, false);


--
-- Name: offtarget_comparison_reference_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.offtarget_comparison_reference_region_id_seq', 1, false);


--
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.project_id_seq', 11, true);


--
-- Name: query_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.query_id_seq', 1, false);


--
-- Name: query_region_block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.query_region_block_id_seq', 1, false);


--
-- Name: query_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.query_region_id_seq', 1, false);


--
-- Name: reference_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.reference_id_seq', 10, true);


--
-- Name: reference_region_block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.reference_region_block_id_seq', 1, false);


--
-- Name: reference_region_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sgonzalez
--

SELECT pg_catalog.setval('public.reference_region_id_seq', 1, false);


--
-- Name: alignment alignment_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.alignment
    ADD CONSTRAINT alignment_pkey PRIMARY KEY (id);


--
-- Name: alignment alignment_query_region_block_id_reference_region_block_id_s_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.alignment
    ADD CONSTRAINT alignment_query_region_block_id_reference_region_block_id_s_key UNIQUE (query_region_block_id, reference_region_block_id, strand, missmatches, alignment_block_number);


--
-- Name: efficiency efficiency_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.efficiency
    ADD CONSTRAINT efficiency_pkey PRIMARY KEY (id);


--
-- Name: efficiency efficiency_query_id_method_efficiency_data_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.efficiency
    ADD CONSTRAINT efficiency_query_id_method_efficiency_data_key UNIQUE (query_id, method, efficiency_data);


--
-- Name: maintarget_comparison maintarget_comparison_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison
    ADD CONSTRAINT maintarget_comparison_pkey PRIMARY KEY (id);


--
-- Name: maintarget_comparison_reference maintarget_comparison_referen_maintarget_comparison_id_refe_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference
    ADD CONSTRAINT maintarget_comparison_referen_maintarget_comparison_id_refe_key UNIQUE (maintarget_comparison_id, reference_id);


--
-- Name: maintarget_comparison_reference_region maintarget_comparison_referen_maintarget_comparison_referen_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference_region
    ADD CONSTRAINT maintarget_comparison_referen_maintarget_comparison_referen_key UNIQUE (maintarget_comparison_reference_id, target_number, reference_region_id);


--
-- Name: maintarget_comparison_reference maintarget_comparison_reference_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference
    ADD CONSTRAINT maintarget_comparison_reference_pkey PRIMARY KEY (id);


--
-- Name: maintarget_comparison_reference_region maintarget_comparison_reference_region_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference_region
    ADD CONSTRAINT maintarget_comparison_reference_region_pkey PRIMARY KEY (id);


--
-- Name: offtarget_comparison offtarget_comparison_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison
    ADD CONSTRAINT offtarget_comparison_pkey PRIMARY KEY (id);


--
-- Name: offtarget_comparison_reference offtarget_comparison_referenc_offtarget_comparison_id_refer_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference
    ADD CONSTRAINT offtarget_comparison_referenc_offtarget_comparison_id_refer_key UNIQUE (offtarget_comparison_id, reference_id);


--
-- Name: offtarget_comparison_reference_region offtarget_comparison_referenc_offtarget_comparison_referenc_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference_region
    ADD CONSTRAINT offtarget_comparison_referenc_offtarget_comparison_referenc_key UNIQUE (offtarget_comparison_reference_id, target_number, reference_region_id);


--
-- Name: offtarget_comparison_reference offtarget_comparison_reference_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference
    ADD CONSTRAINT offtarget_comparison_reference_pkey PRIMARY KEY (id);


--
-- Name: offtarget_comparison_reference_region offtarget_comparison_reference_region_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference_region
    ADD CONSTRAINT offtarget_comparison_reference_region_pkey PRIMARY KEY (id);


--
-- Name: project project_name_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_name_key UNIQUE (name);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);


--
-- Name: query query_name_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query
    ADD CONSTRAINT query_name_key UNIQUE (name);


--
-- Name: query query_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query
    ADD CONSTRAINT query_pkey PRIMARY KEY (id);


--
-- Name: query_region_block query_region_block_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query_region_block
    ADD CONSTRAINT query_region_block_pkey PRIMARY KEY (id);


--
-- Name: query_region_block query_region_block_query_region_id_start_position_end_posit_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query_region_block
    ADD CONSTRAINT query_region_block_query_region_id_start_position_end_posit_key UNIQUE (query_region_id, start_position, end_position);


--
-- Name: query_region query_region_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query_region
    ADD CONSTRAINT query_region_pkey PRIMARY KEY (id);


--
-- Name: query_region query_region_query_id_start_position_end_position_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query_region
    ADD CONSTRAINT query_region_query_id_start_position_end_position_key UNIQUE (query_id, start_position, end_position);


--
-- Name: query query_sequence_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query
    ADD CONSTRAINT query_sequence_key UNIQUE (sequence);


--
-- Name: reference reference_genus_specie_genomic_version_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference
    ADD CONSTRAINT reference_genus_specie_genomic_version_key UNIQUE (genus, specie, genomic, version);


--
-- Name: reference reference_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference
    ADD CONSTRAINT reference_pkey PRIMARY KEY (id);


--
-- Name: reference_region_block reference_region_block_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference_region_block
    ADD CONSTRAINT reference_region_block_pkey PRIMARY KEY (id);


--
-- Name: reference_region_block reference_region_block_reference_region_id_start_position_e_key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference_region_block
    ADD CONSTRAINT reference_region_block_reference_region_id_start_position_e_key UNIQUE (reference_region_id, start_position, end_position);


--
-- Name: reference_region reference_region_pkey; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference_region
    ADD CONSTRAINT reference_region_pkey PRIMARY KEY (id);


--
-- Name: reference_region reference_region_reference_id_sequence_name_start_position__key; Type: CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference_region
    ADD CONSTRAINT reference_region_reference_id_sequence_name_start_position__key UNIQUE (reference_id, sequence_name, start_position, end_position);


--
-- Name: alignment fk_a_query_region_block; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.alignment
    ADD CONSTRAINT fk_a_query_region_block FOREIGN KEY (query_region_block_id) REFERENCES public.query_region_block(id);


--
-- Name: alignment fk_a_reference_region_block; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.alignment
    ADD CONSTRAINT fk_a_reference_region_block FOREIGN KEY (reference_region_block_id) REFERENCES public.reference_region_block(id);


--
-- Name: efficiency fk_e_query; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.efficiency
    ADD CONSTRAINT fk_e_query FOREIGN KEY (query_id) REFERENCES public.query(id);


--
-- Name: maintarget_comparison fk_mtc_project; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison
    ADD CONSTRAINT fk_mtc_project FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: maintarget_comparison fk_mtc_query_region; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison
    ADD CONSTRAINT fk_mtc_query_region FOREIGN KEY (query_region_id) REFERENCES public.query_region(id);


--
-- Name: maintarget_comparison_reference fk_mtcr_maintarget_comparison; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference
    ADD CONSTRAINT fk_mtcr_maintarget_comparison FOREIGN KEY (maintarget_comparison_id) REFERENCES public.maintarget_comparison(id);


--
-- Name: maintarget_comparison_reference fk_mtcr_reference; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference
    ADD CONSTRAINT fk_mtcr_reference FOREIGN KEY (reference_id) REFERENCES public.reference(id);


--
-- Name: maintarget_comparison_reference_region fk_mtcrr_maintarget_comparison_reference; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference_region
    ADD CONSTRAINT fk_mtcrr_maintarget_comparison_reference FOREIGN KEY (maintarget_comparison_reference_id) REFERENCES public.maintarget_comparison_reference(id);


--
-- Name: maintarget_comparison_reference_region fk_mtcrr_reference_region; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.maintarget_comparison_reference_region
    ADD CONSTRAINT fk_mtcrr_reference_region FOREIGN KEY (reference_region_id) REFERENCES public.reference_region(id);


--
-- Name: offtarget_comparison fk_otc_project; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison
    ADD CONSTRAINT fk_otc_project FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- Name: offtarget_comparison fk_otc_query; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison
    ADD CONSTRAINT fk_otc_query FOREIGN KEY (query_region_id) REFERENCES public.query_region(id);


--
-- Name: offtarget_comparison_reference fk_otcr_maintarget_comparison; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference
    ADD CONSTRAINT fk_otcr_maintarget_comparison FOREIGN KEY (offtarget_comparison_id) REFERENCES public.offtarget_comparison(id);


--
-- Name: offtarget_comparison_reference fk_otcr_reference; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference
    ADD CONSTRAINT fk_otcr_reference FOREIGN KEY (reference_id) REFERENCES public.reference(id);


--
-- Name: offtarget_comparison_reference_region fk_otcrr_offtarget_comparison_reference; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference_region
    ADD CONSTRAINT fk_otcrr_offtarget_comparison_reference FOREIGN KEY (offtarget_comparison_reference_id) REFERENCES public.offtarget_comparison_reference(id);


--
-- Name: offtarget_comparison_reference_region fk_otcrr_reference_region; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.offtarget_comparison_reference_region
    ADD CONSTRAINT fk_otcrr_reference_region FOREIGN KEY (reference_region_id) REFERENCES public.reference_region(id);


--
-- Name: query_region_block fk_qb_query_region; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query_region_block
    ADD CONSTRAINT fk_qb_query_region FOREIGN KEY (query_region_id) REFERENCES public.query_region(id);


--
-- Name: query_region fk_qr_query; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.query_region
    ADD CONSTRAINT fk_qr_query FOREIGN KEY (query_id) REFERENCES public.query(id);


--
-- Name: reference_region fk_tr_reference; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference_region
    ADD CONSTRAINT fk_tr_reference FOREIGN KEY (reference_id) REFERENCES public.reference(id);


--
-- Name: reference_region_block fk_trb_reference_region; Type: FK CONSTRAINT; Schema: public; Owner: sgonzalez
--

ALTER TABLE ONLY public.reference_region_block
    ADD CONSTRAINT fk_trb_reference_region FOREIGN KEY (reference_region_id) REFERENCES public.reference_region(id);


--
-- PostgreSQL database dump complete
--

