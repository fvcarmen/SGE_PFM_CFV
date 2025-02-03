# Planificación módulo Odoo

### Nombre del módulo

_cine\_gestion\_sesiones_

### Descripción corta

Este módulo gestiona todos los eventos y películas del cine, incluyendo la programación de sesiones, asignación de descuentos, control de material adicional para eventos y la gestión de KDMs para películas que permiten su proyección.

### Descripción detallada de todas las funcionalidades a cubrir

1.  _Gestión de películas y eventos:_
    
    *   Registro de películas / eventos con sus respectivos datos:
        
        *   Título
            
        *   Género
            
        *   Duración
            
        *   PEGI (clasificación por edad)
            
        *   Descripción
            
        *   Distribuidora
            
        *   KDM
            
        *   DCP
            
        *   Estado
            
        *   Imagen
            
    *   Programación de horarios para películas y eventos.
        
    *   Asociación de publicidad a las películas según su género y otros requisitos de distribuidoras y anunciantes.
        
2.  _Gestión de Sesiones:_
    
    *   Configuración automática de los horarios de las sesiones según:
        
        *   Capacidad de la sala
            
        *   Duración de las películas (que no se superpongan)
            
        *   Género de la película
            
    *   Panel de estado de programación semanal que permita acceder al estado de la sesión al seleccionarla.
        
    *   Panel de estado en tiempo real que muestre las sesiones en curso y alerte los errores en rojo.
        
    *   Editor manual de sesiones.
        
3.  _Gestión de KDMS:_
    
    *   Crear las KDMS
        
    *   Asociarlas a cada película
        
    *   Validar automáticamente si es válida o ha expirado.
        
    *   Alertar sobre las KDM expiradas o que expirarán pronto.
        
4.  _Gestión de Tarifas y Descuentos:_
    
    *   Editor de tarifas:
        
        *   Vista formulario de tarifas que permita crearlas, editarlas y asociarlas a una sesión.
            
        *   Vista lista de las tarifas disponibles.
            
    *   Editor de descuentos:
        
        *   Vista formulario de descuentos que permita crearlos, editarlos, y asociarlos a una tarifa / ticket.
            
        *   Vista lista de los descuentos disponibles.
            
5.  _Gestión de Salas:_
    
    *   Vista formulario de salas que permita crear y editar las salas de cada cine, con su respectiva capacidad generada calculada por las filas y columnas que tiene...
        
    *   Vista lista para visualizarlas
        
6.  _Gestión de Anuncios:_
    
    *   Vista formulario de anuncios que permita crear y editar los anuncios de cada cine, con su respectivo género, duración, pegi...
        
    *   Vista lista para visualizarlas
        
7.  _Generación de Informes y Estadísticas de ventas:_
    
    Generar según la cantidad de ocupación de una sesión / una película concreta / uso de descuentos / géneros ... informes para mejorar la programación automática y tener datos de las películas.
    

### Mapa del módulo
![MapaModulo](img/mapa_modulo.png)

### Dependencias de otros módulos

*   Para la venta de entradas y productos: ventas
    
*   Para gestionar las ventas por usuario: empleados
    
*   Para sincronizar la venta de entradas con el tpv: punto de venta
    
*   Para enviar recordatorios de caducidad de kdm: mail
    
*   Para la gestión de generación de sesiones con tarifas acordes, acceso al: calendario
    

### Wireframes
![Wireframe1](img/wireframe_vista.png)
![Wireframe2](img/wireframe_lista.png)
![Wireframe3](img/vista_semanal.png)
![Wireframe4](img/vista_diaria.png)
### Control de accesos

*   Encargados:
    
    *   Acceso al panel de estado actual y programación semanal.
        
    *   Acceso para visualizar y editar programación de sesiones.
        
    *   Acceso para crear, editar y eliminar películas y eventos.
        
    *   Acceso a estadísticas e informes.
        
    *   Gestión de KDMs.
        
*   Oficinas:
    
    *   Acceso completo al módulo.
        
    *   Acceso a estadísticas e informes.
        
    *   Acceso a crear, editar y eliminar películas, eventos, tarifas y sesiones.
        
*   Empleados de cabina:
    
    *   Acceso al panel de estado y programación.
        
    *   Gestión de KDMs.
        
*   Empleados:
    
    *   Acceso para crear, editar y eliminar las sesiones programadas.
        
    *   Acceso al panel de programación semanal.
        

### Diagramas de flujo
![Diagrama1](img/logico_sesiones.png)
![Diagrama2](img/logico_sesiones_manual.png)

### Esquema relacional
![EsquemaER](img/diagrama_relacional.png)