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
    nombre_imagen character varying(50),
    cant_imagen integer,  -- Cambiamos de character varying a integer
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
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
    au01_c double precision,
    au02_c double precision,
    au04_c double precision,
    au05_c double precision,
    au06_c double precision,
    au07_c double precision,
    au09_c double precision,
    au10_c double precision,
    au12_c double precision,
    au14_c double precision,
    au15_c double precision,
    au17_c double precision,
    au20_c double precision,
    au23_c double precision,
    au25_c double precision,
    au26_c double precision,
    au28_c double precision,
    au45_c double precision,
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