CREATE TABLE public.organisations (
	id int GENERATED ALWAYS AS IDENTITY NOT NULL,
	name varchar NOT NULL,
	CONSTRAINT organisation_pk PRIMARY KEY (id)
);

INSERT INTO public.organisations ("name") VALUES('Default');
INSERT INTO public.organisations ("name") VALUES('Organisation Blue');
INSERT INTO public.organisations ("name") VALUES('Organisation Green');
INSERT INTO public.organisations ("name") VALUES('Organisation No Theme');


CREATE TABLE public.users (
	id int GENERATED ALWAYS AS IDENTITY NOT NULL,
	"name" varchar NOT NULL,
	organisation_id int NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id),
	CONSTRAINT users_organisations_fk FOREIGN KEY (organisation_id) REFERENCES public.organisations(id)
);

INSERT INTO public.users ("name", organisation_id) VALUES('user 1', 1);
INSERT INTO public.users ("name", organisation_id) VALUES('user 2', 1);
INSERT INTO public.users ("name", organisation_id) VALUES('user blue 1', 2);
INSERT INTO public.users ("name", organisation_id) VALUES('user blue 2', 2);
INSERT INTO public.users ("name", organisation_id) VALUES('user green 1', 3);
INSERT INTO public.users ("name", organisation_id) VALUES('user no theme 1', 4);


CREATE TABLE public.themes (
	id int GENERATED ALWAYS AS IDENTITY NOT NULL,
	organisation_id int NOT NULL,
	title varchar NULL,
	"header" varchar NULL,
	"content" varchar NULL,
	styles varchar NULL,
	CONSTRAINT themes_pk PRIMARY KEY (id),
	CONSTRAINT themes_organisations_fk FOREIGN KEY (organisation_id) REFERENCES public.organisations(id)
);

INSERT INTO public.themes (organisation_id, title, "header", "content", styles) VALUES(1, 'Default Title', 'Default Header', 'Default Content', '{"h1_color": "#f50505", "h2_color": "#f54e4e", "p_color": "#fa9393"}');
INSERT INTO public.themes (organisation_id, title, "header", "content", styles) VALUES(2, 'Blue Title', 'Blue Header', 'Blue Content', '{"h1_color": "#0260f7", "h2_color": "#468bfa", "p_color": "#77aafc"}');
INSERT INTO public.themes (organisation_id, title, "header", "content", styles) VALUES(3, 'Green Title', 'Green Header', 'Green Content', '{"h1_color": "#008000", "h2_color": "#00e600", "p_color": "#66ff66"}');
