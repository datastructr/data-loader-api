SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 185 (class 1259 OID 61443)
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE accounts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE accounts_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 186 (class 1259 OID 61445)
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE accounts (
    id integer DEFAULT nextval('accounts_id_seq'::regclass) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    role character varying(255),
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    verification_token character varying(255),
    is_verified boolean
);


ALTER TABLE accounts OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 61456)
-- Name: answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE answers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE answers_id_seq OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 61467)
-- Name: answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answers (
    id integer DEFAULT nextval('answers_id_seq'::regclass) NOT NULL,
    answer_text text,
    question_id integer,
    feedback_result_id integer,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    account_id integer
);


ALTER TABLE answers OWNER TO postgres;

--
-- TOC entry 191 (class 1259 OID 61490)
-- Name: countries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE countries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE countries_id_seq OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 61492)
-- Name: countries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE countries (
    id integer DEFAULT nextval('countries_id_seq'::regclass) NOT NULL,
    country_name character varying(255) NOT NULL
);


ALTER TABLE countries OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 61479)
-- Name: leads_fid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE leads_fid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE leads_fid_seq OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 61481)
-- Name: leads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE leads (
    fid integer DEFAULT nextval('leads_fid_seq'::regclass) NOT NULL,
    project_title text,
    project_number character varying(255),
    project_size text,
    project_description text
);


ALTER TABLE leads OWNER TO postgres;

--
-- TOC entry 193 (class 1259 OID 61498)
-- Name: leads_countries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE leads_countries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE leads_countries_id_seq OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 61500)
-- Name: leads_countries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE leads_countries (
    id integer DEFAULT nextval('leads_countries_id_seq'::regclass) NOT NULL,
    lead_fid integer NOT NULL,
    country_id integer NOT NULL
);


ALTER TABLE leads_countries OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 69659)
-- Name: leads_sectors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE leads_sectors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE leads_sectors_id_seq OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 69661)
-- Name: leads_sectors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE leads_sectors (
    id integer DEFAULT nextval('leads_sectors_id_seq'::regclass) NOT NULL,
    lead_fid integer NOT NULL,
    sector_id integer NOT NULL
);


ALTER TABLE leads_sectors OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 69677)
-- Name: leads_tests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE leads_tests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE leads_tests_id_seq OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 69679)
-- Name: leads_tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE leads_tests (
    id integer DEFAULT nextval('leads_tests_id_seq'::regclass) NOT NULL,
    lead_fid integer NOT NULL,
    test_id integer NOT NULL
);


ALTER TABLE leads_tests OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 69649)
-- Name: sectors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sectors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sectors_id_seq OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 69651)
-- Name: sectors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sectors (
    id integer DEFAULT nextval('sectors_id_seq'::regclass) NOT NULL,
    sector character varying(255)
);


ALTER TABLE sectors OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 69667)
-- Name: tests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tests_id_seq OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 69669)
-- Name: tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE tests (
    id integer DEFAULT nextval('tests_id_seq'::regclass) NOT NULL,
    test_name character varying(255)
);


ALTER TABLE tests OWNER TO postgres;

--
-- TOC entry 2468 (class 0 OID 61445)
-- Dependencies: 186
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY accounts (id, password, email, role, created_at, updated_at, verification_token, is_verified) FROM stdin;
1	password	admin@state.gov	admin	2016-11-15 11:12:32.571456-05	2016-11-15 11:12:32.571456-05	\N	t
\.


--
-- TOC entry 2492 (class 0 OID 0)
-- Dependencies: 185
-- Name: accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('accounts_id_seq', 1, true);


--
-- TOC entry 2470 (class 0 OID 61467)
-- Dependencies: 188
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answers (id, answer_text, question_id, feedback_result_id, created_at, updated_at, account_id) FROM stdin;
1	Answer one	1	1	\N	\N	\N
2	Answer two	2	2	\N	\N	\N
3	Answer three	3	3	\N	\N	\N
4	Answer four	4	4	\N	\N	\N
5	Answer five	5	5	\N	\N	\N
6	Answer six	6	6	\N	\N	\N
7	Answer one	1	1	\N	\N	\N
8	Answer one	1	1	\N	\N	\N
9	Answer one	1	1	\N	\N	\N
10	Answer one	1	1	\N	\N	\N
11	Answer two	2	2	\N	\N	\N
12	Answer three	3	3	\N	\N	\N
13	Answer four	4	4	\N	\N	\N
14	Answer five	5	5	\N	\N	\N
15	Answer six	6	6	\N	\N	\N
16	Answer one	1	1	\N	\N	\N
17	Answer two	2	2	\N	\N	\N
18	Answer one	1	1	\N	\N	\N
19	Answer two	2	2	\N	\N	\N
20	Answer three	3	3	\N	\N	\N
21	Answer four	4	4	\N	\N	\N
22	Answer five	5	5	\N	\N	\N
23	Answer six	6	6	\N	\N	\N
24	Answer one	1	1	\N	\N	\N
25	Answer two	2	2	\N	\N	\N
26	Answer one	1	1	\N	\N	\N
27	Answer two	2	2	\N	\N	\N
28	Answer one	1	1	\N	\N	\N
29	Answer two	2	2	\N	\N	\N
30	Answer one	1	1	\N	\N	\N
31	Answer two	2	2	\N	\N	\N
32	Answer three	3	\N	\N	\N	\N
33	Answer four	4	4	\N	\N	\N
34	Answer five	5	5	\N	\N	\N
35	Answer six	6	6	\N	\N	\N
36	Answer one	1	1	\N	\N	\N
37	Answer two	2	2	\N	\N	\N
38	Answer three	3	\N	\N	\N	\N
39	Answer four	4	4	\N	\N	\N
40	Answer five	5	5	\N	\N	\N
41	Answer six	6	6	\N	\N	\N
42	Answer one	1	1	\N	\N	\N
43	Answer two	2	2	\N	\N	\N
44	Answer three	3	\N	\N	\N	\N
45	Answer one	1	1	\N	\N	\N
46	Answer two	2	2	\N	\N	\N
47	Answer three	3	\N	\N	\N	\N
48	Answer four	4	4	\N	\N	\N
49	Answer five	5	5	\N	\N	\N
50	Answer six	6	6	\N	\N	\N
55	Answer one	1	1	\N	\N	\N
56	Answer two	2	2	\N	\N	\N
57	Answer three	3	3	\N	\N	\N
58	Answer four	4	4	\N	\N	\N
59	Answer five	5	5	\N	\N	\N
60	Answer six	6	6	\N	\N	\N
61	Answer one	1	1	\N	\N	\N
62	Answer two	2	2	\N	\N	\N
63	Answer three	3	3	\N	\N	\N
64	Answer four	4	4	\N	\N	\N
65	Answer five	5	5	\N	\N	\N
66	Answer six	6	6	\N	\N	\N
67	Answer one	1	1	\N	\N	\N
68	Answer two	2	2	\N	\N	\N
69	Answer three	3	3	\N	\N	\N
70	Answer one	1	1	\N	\N	\N
71	Answer two	2	2	\N	\N	\N
72	Answer three	3	3	\N	\N	\N
73	Answer four	4	4	\N	\N	\N
74	Answer five	5	5	\N	\N	\N
75	Answer six	6	6	\N	\N	\N
76	Answer one	1	1	\N	\N	\N
77	Answer two	2	2	\N	\N	\N
78	Answer three	3	3	\N	\N	\N
79	Answer four	4	4	\N	\N	\N
80	Answer five	5	5	\N	\N	\N
81	Answer six	6	6	\N	\N	\N
82	Answer four	4	4	\N	\N	\N
83	Answer five	5	5	\N	\N	\N
84	Answer six	6	6	\N	\N	\N
85	Answer four	4	4	\N	\N	\N
86	Answer five	5	5	\N	\N	\N
87	Answer six	6	6	\N	\N	\N
88	Answer four	4	4	\N	\N	\N
89	Answer five	5	5	\N	\N	\N
90	Answer six	6	6	\N	\N	\N
100	Answer one	1	1	\N	\N	\N
101	Answer two	2	2	\N	\N	\N
102	Answer three	3	3	\N	\N	\N
91	Answer four	4	4	\N	\N	\N
92	Answer five	5	5	\N	\N	\N
93	Answer six	6	6	\N	\N	\N
100	Answer one	1	1	\N	\N	\N
101	Answer two	2	2	\N	\N	\N
102	Answer three	3	3	\N	\N	\N
94	Answer four	4	4	\N	\N	\N
95	Answer five	5	5	\N	\N	\N
96	Answer six	6	6	\N	\N	\N
100	Answer one	1	1	\N	\N	\N
101	Answer two	2	2	\N	\N	\N
102	Answer three	3	3	\N	\N	\N
97	Answer four	4	4	\N	\N	\N
98	Answer five	5	5	\N	\N	\N
99	Answer six	6	6	\N	\N	\N
100	Answer one	1	1	\N	\N	\N
101	Answer two	2	2	\N	\N	\N
102	Answer three	3	3	\N	\N	\N
100	Answer four	4	4	\N	\N	\N
101	Answer five	5	5	\N	\N	\N
102	Answer six	6	6	\N	\N	\N
100	Answer one	1	1	\N	\N	\N
101	Answer two	2	2	\N	\N	\N
102	Answer three	3	3	\N	\N	\N
103	Answer four	4	4	\N	\N	\N
104	Answer five	5	5	\N	\N	\N
105	Answer six	6	6	\N	\N	\N
106	Answer four	4	4	\N	\N	\N
107	Answer five	5	5	\N	\N	\N
108	Answer six	6	6	\N	\N	\N
109	Answer four	4	4	\N	\N	\N
110	Answer five	5	5	\N	\N	\N
111	Answer six	6	6	\N	\N	\N
100	Answer one	1	1	\N	\N	\N
101	Answer two	2	2	\N	\N	\N
102	Answer three	3	3	\N	\N	\N
100	Answer one	111111	1	\N	\N	\N
101	Answer two	444	2	\N	\N	\N
102	Answer three	5555	3	\N	\N	\N
100	Answer one	111111	1	\N	\N	\N
101	Answer two	444	2	\N	\N	\N
102	Answer three	5555	3	\N	\N	\N
100	Answer one	111111	1	\N	\N	\N
101	Answer two	444	2	\N	\N	\N
102	Answer three	5555	3	\N	\N	\N
100	Answer one	111111	1	\N	\N	\N
101	Answer two	444	2	\N	\N	\N
102	Answer three	5555	3	\N	\N	\N
100	Answer one	111111	1	\N	\N	\N
101	Answer two	444	2	\N	\N	\N
102	Answer three	5555	3	\N	\N	\N
120	Answer one	111111	1	\N	\N	\N
121	Answer two	444	2	\N	\N	\N
122	Answer three	5555	3	\N	\N	\N
123	Answer one	111111	1	\N	\N	\N
124	Answer two	444	2	\N	\N	\N
125	Answer three	5555	3	\N	\N	\N
126	Answer one	111111	1	\N	\N	\N
127	Answer two	444	2	\N	\N	\N
128	Answer three	5555	3	\N	\N	\N
129	Answer one	111111	1	\N	\N	\N
130	Answer two	444	2	\N	\N	\N
131	Answer three	5555	3	\N	\N	\N
132	Answer one	111111	1	\N	\N	\N
133	Answer two	444	2	\N	\N	\N
134	Answer three	5555	3	\N	\N	\N
135	Answer one	111111	1	\N	\N	\N
136	Answer two	444	2	\N	\N	\N
137	Answer three	5555	3	\N	\N	\N
138	Answer one	111111	1	\N	\N	\N
139	Answer two	444	2	\N	\N	\N
140	Answer three	5555	3	\N	\N	\N
141	Answer one	111111	1	\N	\N	\N
142	Answer two	444	2	\N	\N	\N
143	Answer three	5555	3	\N	\N	\N
144	Answer one	111111	1	\N	\N	\N
145	Answer two	444	2	\N	\N	\N
146	Answer three	5555	3	\N	\N	\N
147	Answer one	111111	1	\N	\N	\N
148	Answer two	444	2	\N	\N	\N
149	Answer three	5555	3	\N	\N	\N
150	Answer one	111111	1	\N	\N	\N
151	Answer two	444	2	\N	\N	\N
152	Answer three	5555	3	\N	\N	\N
153	Answer one	111111	1	\N	\N	\N
154	Answer two	444	2	\N	\N	\N
155	Answer three	5555	3	\N	\N	\N
156	Answer one	111111	1	\N	\N	\N
157	Answer two	444	2	\N	\N	\N
158	Answer three	5555	3	\N	\N	\N
\.


--
-- TOC entry 2493 (class 0 OID 0)
-- Dependencies: 187
-- Name: answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('answers_id_seq', 158, true);


--
-- TOC entry 2474 (class 0 OID 61492)
-- Dependencies: 192
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY countries (id, country_name) FROM stdin;
3	Afghanistan
7	Albania
64	Algeria
9	Andorra
6	Angola
244	Antarctica
13	Antigua and Barbuda
5	Argentina
11	Armenia
10	Australia
15	Austria
17	Azerbaijan
26	Bahrain
24	Bangladesh
36	Barbados
31	Belarus
19	Belgium
32	Belize
21	Benin
39	Bhutan
34	Bolivia
30	Bosnia and Herzegovina
40	Botswana
35	Brazil
37	Brunei
25	Bulgaria
22	Burkina Faso
134	Burma
18	Burundi
45	C̫te d'Ivoire
53	Cabo Verde
108	Cambodia
47	Cameroon
246	Canada
41	Central African Republic
186	Chad
43	Chile
44	China
51	Colombia
52	Comoros
54	Costa Rica
89	Croatia
55	Cuba
101	Cyprus
58	Czech Republic
50	Democratic Republic of the Congo
29	Denmark
62	Djibouti
63	Dominica
60	Dominican Republic
67	Ecuador
218	Egypt
176	El Salvador
20	Equatorial Guinea
68	Eritrea
65	Estonia
72	Ethiopia
76	Federated States of Micronesia
73	Fiji
8	Finland
107	France
79	Gabon
83	Gambia
80	Georgia
61	Germany
81	Ghana
27	Greece
28	Grenada
46	Guatemala
82	Guinea
84	Guinea-Bissau
85	Guyana
90	Haiti
204	Holy See
88	Honduras
91	Hungary
97	Iceland
242	India
57	Indonesia
95	Iran
93	Iraq
92	Ireland
102	Israel
103	Italy
104	Jamaica
98	Japan
96	Jordan
100	Kashmir
99	Kazakhstan
105	Kenya
109	Kiribati
113	Kosovo
114	Kuwait
106	Kyrgyzstan
117	Laos
71	Latvia
118	Lebanon
125	Lesotho
119	Liberia
121	Libya
123	Liechtenstein
111	Lithuania
115	Luxembourg
130	Macedonia
126	Madagascar
142	Malawi
143	Malaysia
127	Maldives
132	Mali
133	Malta
129	Marshall Islands
140	Mauritania
141	Mauritius
128	Mexico
94	Moldova
78	Monaco
136	Mongolia
135	Montenegro
214	Morocco
138	Mozambique
144	Namibia
152	Nauru
149	Nepal
2	Netherlands
49	New Zealand
146	Nicaragua
139	Niger
145	Nigeria
163	North Korea
147	Norway
150	Oman
154	Pakistan
161	Palau
156	Panama
162	Papua New Guinea
166	Paraguay
159	Peru
160	Philippines
157	Poland
164	Portugal
168	Qatar
48	Republic of Congo
169	Romania
170	Russia
165	Rwanda
110	Saint Kitts and Nevis
122	Saint Lucia
69	Saint Vincent and the Grenadines
210	Samoa
177	San Marino
179	Sao Tome and Principe
171	Saudi Arabia
172	Senegal
178	Serbia
185	Seychelles
175	Sierra Leone
173	Singapore
181	Slovakia
151	Slovenia
174	Solomon Islands
222	Somalia
213	South Africa
112	South Korea
217	South Sudan
70	Spain
124	Sri Lanka
221	Sudan
180	Suriname
183	Swaziland
182	Sweden
42	Switzerland
212	Syria
198	Taiwan
192	Tajikistan
199	Tanzania
190	Thailand
23	The Bahamas
195	Timor-Leste
187	Togo
196	Tonga
155	Trinidad and Tobago
188	Tunisia
197	Turkey
194	Turkmenistan
248	Tuvalu
193	Uganda
201	Ukraine
4	United Arab Emirates
33	United Kingdom
16	United States of America
200	Uruguay
203	Uzbekistan
209	Vanuatu
205	Venezuela
207	Vietnam
247	Western Sahara
211	Yemen
215	Zambia
216	Zimbabwe
\.


--
-- TOC entry 2494 (class 0 OID 0)
-- Dependencies: 191
-- Name: countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('countries_id_seq', 1, false);


--
-- TOC entry 2472 (class 0 OID 61481)
-- Dependencies: 190
-- Data for Name: leads; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY leads (fid, project_title, project_number, project_size, project_description) FROM stdin;
1	title_1	1	1000000	description_1
2	title_1	2	10000	description_1
3	title_1	3	1	description_1
4	title_1	1	1000000	description_1
5	title_1	1	1000000	description_1
6	title_1	2	10000	description_1
7	title_1	3	1	description_1
8	title_1	1	1000000	description_1
9	title_1	2	10000	description_1
10	title_1	3	1	description_1
11	title_1	1	1000000	description_1
12	title_1	2	10000	description_1
13	title_1	3	1	description_1
32	title_1	1	1000000	description_1
33	title_1	2	10000	description_1
34	title_1	3	1	description_1
35	title_1	1	1000000	description_1
36	title_1	2	10000	description_1
37	title_1	3	1	description_1
38	title_1	1	1000000	description_1
39	title_1	2	10000	description_1
40	title_1	3	1	description_1
41	title_1	1	1000000	description_1
42	title_1	2	10000	description_1
43	title_1	3	1	description_1
44	title_1	1	1000000	description_1
45	title_1	2	10000	description_1
46	title_1	3	1	description_1
47	title_1	1	1000000	description_1
48	title_1	2	10000	description_1
49	title_1	3	1	description_1
50	title_1	1	1000000	description_1
51	title_1	2	10000	description_1
52	title_1	3	1	description_1
53	title_1	1	1000000	description_1
54	title_1	2	10000	description_1
55	title_1	3	1	description_1
56	title_1	1	1000000	description_1
57	title_1	2	10000	description_1
58	title_1	3	1	description_1
59	title_1	1	1000000	description_1
60	title_1	2	10000	description_1
61	title_1	3	1	description_1
64	title_1	1	1000000	description_1
65	title_1	2	10000	description_1
66	title_1	3	1	description_1
67	title_1	1	1000000	description_1
68	title_1	2	10000	description_1
69	title_1	3	1	description_1
70	title_1	1	1000000	description_1
71	title_1	2	10000	description_1
72	title_1	3	1	description_1
73	title_1	1	1000000	description_1
74	title_1	2	10000	description_1
75	title_1	3	1	description_1
76	title_1	1	1000000	description_1
77	title_1	2	10000	description_1
78	title_1	3	1	description_1
79	title_1	1	1000000	description_1
80	title_1	2	10000	description_1
81	title_1	3	1	description_1
82	title_1	1	1000000	description_1
83	title_1	2	10000	description_1
84	title_1	3	1	description_1
85	title_1	1	1000000	description_1
86	title_3	2	10000	description_2
87	title_3	3	1	description_3
88	title_1	1	1000000	description_1
89	title_3	2	10000	description_2
90	title_3	3	1	description_3
91	tátle_1	1	1000000	description_1
92	title_3	2	10000	description_2
93	title_3	3	1	description_3
94	tátle_1	1	1000000	description_1
95	select * from leads;	2	10000	description_2
96	title_3	3	1	description_3
97	tátle_1	1	1000000	description_1
98	select * from leads;	2	10000	description_2
99	title_3	3	1	description_3
100	tátle_1	1	1000000	description_1
101	select * from leads;	2	10000	description_2
102	title_3	3	1	description_3
\.


--
-- TOC entry 2476 (class 0 OID 61500)
-- Dependencies: 194
-- Data for Name: leads_countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY leads_countries (id, lead_fid, country_id) FROM stdin;
1	33	32
2	33	33
3	33	34
4	33	35
5	33	36
6	33	37
7	33	38
8	33	39
9	33	40
10	33	41
11	33	42
12	33	43
13	33	44
14	33	45
15	33	46
16	33	47
17	33	48
18	33	49
19	33	50
20	33	51
21	33	52
22	33	53
23	33	54
24	33	55
25	33	56
26	33	57
27	33	58
28	33	59
29	33	60
30	33	61
31	33	64
32	33	65
33	33	66
34	33	67
35	33	68
36	33	69
37	33	70
38	33	71
39	33	72
40	73	33
41	74	33
42	75	33
43	76	33
44	77	33
45	78	33
46	79	33
47	80	33
48	81	33
49	82	33
50	83	33
51	84	33
52	85	33
53	86	15
54	87	218
55	88	33
56	89	15
57	90	218
58	91	33
59	92	15
60	93	218
61	94	33
62	95	15
63	96	218
64	97	33
65	98	15
66	99	218
67	100	33
68	101	15
69	102	218
\.


--
-- TOC entry 2495 (class 0 OID 0)
-- Dependencies: 193
-- Name: leads_countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('leads_countries_id_seq', 69, true);


--
-- TOC entry 2496 (class 0 OID 0)
-- Dependencies: 189
-- Name: leads_fid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('leads_fid_seq', 102, true);


--
-- TOC entry 2480 (class 0 OID 69661)
-- Dependencies: 198
-- Data for Name: leads_sectors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY leads_sectors (id, lead_fid, sector_id) FROM stdin;
2	5	32
3	5	33
4	5	34
5	5	35
6	5	36
7	5	37
8	5	38
9	5	39
10	5	40
11	5	41
12	5	42
13	5	43
14	5	44
15	5	45
16	5	46
17	5	47
18	5	48
19	5	49
20	5	50
21	5	51
22	5	52
23	5	53
24	5	54
25	5	55
26	5	56
27	5	57
28	5	58
29	5	59
30	5	60
31	5	61
32	5	64
33	5	65
34	5	66
35	5	67
36	5	68
37	5	69
38	5	70
39	5	71
40	5	72
41	73	5
42	74	5
43	75	5
44	76	5
45	77	5
46	78	5
47	79	5
48	80	5
49	81	5
50	82	5
51	83	5
52	84	5
53	85	5
54	86	14
55	87	13
56	88	5
57	89	14
58	90	13
59	91	5
60	92	14
61	93	13
62	94	5
63	95	14
64	96	13
65	97	5
66	98	14
67	99	13
68	100	5
69	101	14
70	102	13
\.


--
-- TOC entry 2497 (class 0 OID 0)
-- Dependencies: 197
-- Name: leads_sectors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('leads_sectors_id_seq', 70, true);


--
-- TOC entry 2484 (class 0 OID 69679)
-- Dependencies: 202
-- Data for Name: leads_tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY leads_tests (id, lead_fid, test_id) FROM stdin;
1	1	34
2	1	37
3	1	40
4	1	43
5	1	46
6	1	49
7	1	52
8	1	55
9	1	58
10	1	61
11	1	66
12	1	69
13	1	72
14	75	1
15	78	1
16	81	1
17	84	1
18	87	1
19	90	1
20	93	1
21	96	1
22	99	1
23	102	1
\.


--
-- TOC entry 2498 (class 0 OID 0)
-- Dependencies: 201
-- Name: leads_tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('leads_tests_id_seq', 23, true);


--
-- TOC entry 2478 (class 0 OID 69651)
-- Dependencies: 196
-- Data for Name: sectors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sectors (id, sector) FROM stdin;
1	Administrative and Support and Waste Management and Remediation Services
2	Agriculture, Forestry, Fishing and Hunting
3	Construction
4	Educational Services
5	Finance and Insurance
6	Health Care and Social Assistance
7	Information
8	Manufacturing
9	Mining, Quarrying, and Oil and Gas Extraction
10	Professional, Scientific, and Technical Services
11	Public Administration
12	Transportation and Warehousing
13	Utilities
14	Other
\.


--
-- TOC entry 2499 (class 0 OID 0)
-- Dependencies: 195
-- Name: sectors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sectors_id_seq', 1, false);


--
-- TOC entry 2482 (class 0 OID 69669)
-- Dependencies: 200
-- Data for Name: tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tests (id, test_name) FROM stdin;
1	Test One
\.


--
-- TOC entry 2500 (class 0 OID 0)
-- Dependencies: 199
-- Name: tests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tests_id_seq', 1, true);


--
-- TOC entry 2328 (class 2606 OID 61455)
-- Name: accounts accounts_email_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_email_unique UNIQUE (email);


--
-- TOC entry 2330 (class 2606 OID 61453)
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- TOC entry 2334 (class 2606 OID 61497)
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- TOC entry 2336 (class 2606 OID 61505)
-- Name: leads_countries leads_countries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY leads_countries
    ADD CONSTRAINT leads_countries_pkey PRIMARY KEY (id);


--
-- TOC entry 2332 (class 2606 OID 61489)
-- Name: leads leads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY leads
    ADD CONSTRAINT leads_pkey PRIMARY KEY (fid);


--
-- TOC entry 2342 (class 2606 OID 69666)
-- Name: leads_sectors leads_sectors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY leads_sectors
    ADD CONSTRAINT leads_sectors_pkey PRIMARY KEY (id);


--
-- TOC entry 2348 (class 2606 OID 69684)
-- Name: leads_tests leads_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY leads_tests
    ADD CONSTRAINT leads_tests_pkey PRIMARY KEY (id);


--
-- TOC entry 2338 (class 2606 OID 69656)
-- Name: sectors sectors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sectors
    ADD CONSTRAINT sectors_pkey PRIMARY KEY (id);


--
-- TOC entry 2340 (class 2606 OID 69658)
-- Name: sectors sectors_sector_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sectors
    ADD CONSTRAINT sectors_sector_unique UNIQUE (sector);


--
-- TOC entry 2344 (class 2606 OID 69674)
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- TOC entry 2346 (class 2606 OID 69676)
-- Name: tests tests_test_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tests
    ADD CONSTRAINT tests_test_name_unique UNIQUE (test_name);


--
-- TOC entry 2349 (class 2606 OID 61474)
-- Name: answers account_id_fk_constraint; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answers
    ADD CONSTRAINT account_id_fk_constraint FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE;


-- Completed on 2016-11-30 17:00:19 EST

--
-- PostgreSQL database dump complete
--

