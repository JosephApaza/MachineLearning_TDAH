CREATE OR REPLACE PROCEDURE insertar_estudiante(
    IN p_nombre VARCHAR(100),
    IN p_edad INTEGER,
    IN p_genero VARCHAR(10),
    IN p_tiene_tdah BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO estudiantes (nombre, edad, genero, tiene_tdah)
    VALUES (p_nombre, p_edad, p_genero, p_tiene_tdah);
END;
$$;

CREATE OR REPLACE PROCEDURE actualizar_estudiante(
    IN p_id_estudiante INTEGER,
    IN p_nombre VARCHAR(100),
    IN p_edad INTEGER,
    IN p_genero VARCHAR(10),
    IN p_tiene_tdah BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE estudiantes
    SET nombre = p_nombre,
        edad = p_edad,
        genero = p_genero,
        tiene_tdah = p_tiene_tdah
    WHERE id_estudiante = p_id_estudiante;
END;
$$;

CREATE OR REPLACE PROCEDURE eliminar_estudiante(
    IN p_id_estudiante INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM estudiantes WHERE id_estudiante = p_id_estudiante;
END;
$$;

CREATE OR REPLACE FUNCTION listar_estudiantes()
RETURNS TABLE (
    id_estudiante INTEGER,
    nombre VARCHAR(100),
    edad INTEGER,
    genero VARCHAR(10),
    tiene_tdah BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT * FROM estudiantes;
END;
$$;

CREATE OR REPLACE FUNCTION obtener_datos_estudiantes()
RETURNS TABLE (
    nombre_estudiante VARCHAR(100),
    edad_estudiante INTEGER,
    genero_estudiante VARCHAR(10),
    nombre_expresion VARCHAR(50)
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        e.nombre AS nombre_estudiante,
        e.edad AS edad_estudiante,
        e.genero AS genero_estudiante,
        ex.nombre AS nombre_expresion
    FROM 
        estudiantes e
    JOIN 
        resultados_facial rf ON e.id_estudiante = rf.id_estudiante
    JOIN 
        expresiones ex ON rf.id_expresion = ex.id_expresion;
END;
$$;

CREATE OR REPLACE FUNCTION obtener_datos_para_svm()
RETURNS TABLE (
    nombre_estudiante VARCHAR(100),
    edad_estudiante INTEGER,
    genero_estudiante VARCHAR(10),
    tiene_tdah BOOLEAN,
    nombre_imagen VARCHAR(50),
    fecha TIMESTAMP,
    confidence DOUBLE PRECISION,
    expresion VARCHAR(50),
    au01_r DOUBLE PRECISION,
    au02_r DOUBLE PRECISION,
    au04_r DOUBLE PRECISION,
    au05_r DOUBLE PRECISION,
    au06_r DOUBLE PRECISION,
    au07_r DOUBLE PRECISION,
    au09_r DOUBLE PRECISION,
    au10_r DOUBLE PRECISION,
    au12_r DOUBLE PRECISION,
    au14_r DOUBLE PRECISION,
    au15_r DOUBLE PRECISION,
    au17_r DOUBLE PRECISION,
    au20_r DOUBLE PRECISION,
    au23_r DOUBLE PRECISION,
    au25_r DOUBLE PRECISION,
    au26_r DOUBLE PRECISION,
    au45_r DOUBLE PRECISION,
    au01_c DOUBLE PRECISION,
    au02_c DOUBLE PRECISION,
    au04_c DOUBLE PRECISION,
    au05_c DOUBLE PRECISION,
    au06_c DOUBLE PRECISION,
    au07_c DOUBLE PRECISION,
    au09_c DOUBLE PRECISION,
    au10_c DOUBLE PRECISION,
    au12_c DOUBLE PRECISION,
    au14_c DOUBLE PRECISION,
    au15_c DOUBLE PRECISION,
    au17_c DOUBLE PRECISION,
    au20_c DOUBLE PRECISION,
    au23_c DOUBLE PRECISION,
    au25_c DOUBLE PRECISION,
    au26_c DOUBLE PRECISION,
    au28_c DOUBLE PRECISION,
    au45_c DOUBLE PRECISION
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.nombre AS nombre_estudiante,
        e.edad AS edad_estudiante,
        e.genero AS genero_estudiante,
        e.tiene_tdah,
        rf.nombre_imagen,
        rf.fecha,
        rf.confidence,
        ex.nombre AS expresion,
        rf.au01_r, rf.au02_r, rf.au04_r, rf.au05_r, rf.au06_r, rf.au07_r,
        rf.au09_r, rf.au10_r, rf.au12_r, rf.au14_r, rf.au15_r, rf.au17_r,
        rf.au20_r, rf.au23_r, rf.au25_r, rf.au26_r, rf.au45_r,
        rf.au01_c, rf.au02_c, rf.au04_c, rf.au05_c, rf.au06_c, rf.au07_c,
        rf.au09_c, rf.au10_c, rf.au12_c, rf.au14_c, rf.au15_c, rf.au17_c,
        rf.au20_c, rf.au23_c, rf.au25_c, rf.au26_c, rf.au28_c, rf.au45_c
    FROM 
        estudiantes e
    JOIN 
        resultados_facial rf ON e.id_estudiante = rf.id_estudiante
    JOIN 
        expresiones ex ON rf.id_expresion = ex.id_expresion
    ORDER BY 
        e.nombre, rf.fecha;
END;
$$;
