--
-- PostgreSQL database populate file
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (email, token, token_expire_time, cookie, is_admin, cookie_expire_time) FROM stdin;
example@gmail.com	\N	\N	\N	t	\N
\.


--
-- Data for Name: zones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.zones (id, name, start_x, start_y, end_x, end_y, hourly_rate) FROM stdin;
1	A	2	2	98	64	15
2	B	2	68	98	130	15
3	C	114	2	210	64	15
4	D	114	68	210	130	15
\.

--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars (id, email, model, license_number) FROM stdin;
2	example@gmail.com	Volkswagen Touareg	A000AA
\.


--
-- Data for Name: roads; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roads (id, start_x, start_y, end_x, end_y, zone_id) FROM stdin;
1	1	25	98	37	1
\.


--
-- Data for Name: spaces; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spaces (id, zone_id, number, start_x, start_y, end_x, end_y, car_id, booked_from, booked_until) FROM stdin;
2	1	2	15	1	27	23	\N	\N	\N
3	1	3	29	1	41	23	\N	\N	\N
4	1	4	43	1	55	23	\N	\N	\N
5	1	5	57	1	69	23	\N	\N	\N
6	1	6	71	1	83	23	\N	\N	\N
7	1	7	85	1	97	23	\N	\N	\N
8	1	8	1	39	13	61	\N	\N	\N
9	1	9	15	39	27	61	\N	\N	\N
10	1	10	29	39	41	61	\N	\N	\N
11	1	11	43	39	55	61	\N	\N	\N
12	1	12	57	39	69	61	\N	\N	\N
13	1	13	71	39	83	61	\N	\N	\N
14	1	14	85	39	97	61	\N	\N	\N
1	1	1	1	1	13	23	\N	\N	\N
\.

