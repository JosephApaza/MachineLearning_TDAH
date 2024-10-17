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

