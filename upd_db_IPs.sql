-- 
-- Actualiza los registros de equipos cuya fecha de expiracion ha llegado
-- 
update Equipos set valido=0 where ( (fexp < now() ) AND (fexp != '0000-00-00') AND (valido=1) );

