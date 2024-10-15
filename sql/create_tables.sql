BEGIN;

ALTER TABLE IF EXISTS public.resultados_facial DROP CONSTRAINT IF EXISTS resultados_facial_estudiante_id_fkey;
ALTER TABLE IF EXISTS public.resultados_facial DROP CONSTRAINT IF EXISTS resultados_facial_expresion_id_fkey;

DROP TABLE IF EXISTS public.estudiantes;
CREATE TABLE IF NOT EXISTS public.estudiantes
(
    id_estudiante serial NOT NULL,
    nombre character varying(100) COLLATE pg_catalog."default",
    edad integer,
    genero character varying(10) COLLATE pg_catalog."default",
    tiene_tdah boolean,
    CONSTRAINT estudiantes_pkey PRIMARY KEY (id_estudiante)
);

DROP TABLE IF EXISTS public.expresiones;
CREATE TABLE IF NOT EXISTS public.expresiones
(
    id_expresion serial NOT NULL,
    nombre character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT expresiones_pkey PRIMARY KEY (id_expresion)
);

DROP TABLE IF EXISTS public.resultados_facial;
CREATE TABLE IF NOT EXISTS public.resultados_facial
(
    id_resultados serial NOT NULL,
    id_estudiante integer,
    id_expresion integer,
    cant_imagen character varying(255) COLLATE pg_catalog."default",
    frame integer,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    "timestamp" double precision,
    confidence double precision,
    success boolean,
    au01_r double precision,
    au02_r double precision,
    au04_r double precision,
    au05_r double precision,
    au06_r double precision,
    au07_r double precision,
    au09_r double precision,
    au10_r double precision,
    au12_r double precision,
    au14_r double precision,
    au15_r double precision,
    au17_r double precision,
    au20_r double precision,
    au23_r double precision,
    au25_r double precision,
    au26_r double precision,
    au45_r double precision,
    au01_c boolean,
    au02_c boolean,
    au04_c boolean,
    au05_c boolean,
    au06_c boolean,
    au07_c boolean,
    au09_c boolean,
    au10_c boolean,
    au12_c boolean,
    au14_c boolean,
    au15_c boolean,
    au17_c boolean,
    au20_c boolean,
    au23_c boolean,
    au25_c boolean,
    au26_c boolean,
    au28_c boolean,
    au45_c boolean,
    CONSTRAINT resultados_facial_pkey PRIMARY KEY (id_resultados)
);

ALTER TABLE IF EXISTS public.resultados_facial
    ADD CONSTRAINT resultados_facial_estudiante_id_fkey FOREIGN KEY (id_estudiante)
    REFERENCES public.estudiantes (id_estudiante) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.resultados_facial
    ADD CONSTRAINT resultados_facial_expresion_id_fkey FOREIGN KEY (id_expresion)
    REFERENCES public.expresiones (id_expresion) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;