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
    nombre_expresion VARCHAR(50),
    numero_imagenes INTEGER
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.nombre AS nombre_estudiante,
        e.edad AS edad_estudiante,
        e.genero AS genero_estudiante,
        ex.nombre AS nombre_expresion,
        rf.cant_imagen AS numero_imagenes  -- Obtener directamente el valor de cant_imagen
    FROM 
        estudiantes e
    JOIN 
        resultados_facial rf ON e.id_estudiante = rf.id_estudiante
    JOIN 
        expresiones ex ON rf.id_expresion = ex.id_expresion;
END;
$$;
