# Solución NAC (Network Access Control) para equipos de usuario en un IES
### Desarrollado como parte del TFE, en el Grado en Ingeniería Informática de UNIR

En líneas generales los institutos de enseñanza secundaria (IES) no disponen de ningún mecanismo que permita controlar los equipos que se conectan a su red cableada, lo que puede suponer una enorme brecha en lo que a seguridad se refiere. 

Por las características propias de un centro de este tipo, el flujo de personal itinerante es constante (profesores, sustitutos, alumnos, etc.) y la movilidad entre estancias una necesidad absoluta, por ejemplo, un profesor cambia cada hora de clase. Al llegar a ella conecta su portátil a la toma de red cableada donde tiene acceso inmediato a los recursos tanto internos (unidades de almacenamiento compartido, por ejemplo) como externos (reglas de acceso a Internet). Es habitual que el acceso a los recursos internos esté protegido mediante credenciales, lo cual ya sabemos que no es una medida demasiado segura y se dan muchos casos donde se comparten nombres de usuario y contraseña para el acceso a unidades de red, por ejemplo.

Lo anterior describiría el funcionamiento lógico en el día a día, pero ¿qué sucede si un alumno no autorizado obtiene ese mismo acceso cuando conecta su portátil a la red? Tendría acceso a expedientes, documentación, etc. a los que nunca debe poder llegar.

###	Planteamiento del trabajo

El sistema propuesto añadiría una capa extra de seguridad, gestionando una base de datos con los equipos de usuario (profesores, PAS, otros) identificando el portátil del alumno e impidiendo el acceso del alumno a la red donde el profesorado almacena información, por ejemplo.

Adicionalmente al control de acceso, el sistema será capaz de “catalogar” el PC o portátil y asignarlo al segmento de red que le correspondiera, es decir, separaría los equipos según su categoría en “red_profesores”, “red_pas” y “red_invitados”, por ejemplo, y los asignaría a una determinada VLAN según cada categoría.

Otra ventaja que se obtiene del sistema es que permitiría al personal del centro (profesores, PAS, invitados, etc.) una movilidad completa por las clases y estancias del IES concediéndoles acceso únicamente a los recursos que correspondan a su categoría.
