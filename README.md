# evidencia-final-multiagentes

### Integrantes

* Sergio Chávez A01284297
* Miguel Pedraza A01284469
* Eugenio Castro A00830392
* Eduardo Ramon A01384225
* Emiliano Sánchez A00831284

## Agentes

### Intersección

Se coloca al inicio de nuestra simulación y sirve como el punto de referencia para el camino y la secuencia de pasos a tomar por los diferentes agentes Carro, Es el camino trazado para que estos Agentes puedan saber que hacer en su siguiente paso.

### Carro

Este agente tiene el protocolo de avanzar según la posición inicial que se le da, comportándose de manera única cada vez. Tiene una funcionalidad exactamente iguala a la que tendría un carro en una intersección, haciendo giros hacia la derecha o siguiendo su camino recto. Tiene también propiedad y comportamientos para evitar colisiones y comportarse acorde al estatus de su semáforo asignado. 

### Semáforo

Este actúa como una bandera sobre la cual tiene jerarquía y control de los carros. Funciona en turnos y en cualquier momento de la intersección siempre actuarán esquinas contrarias, es decir mientras unas esquinas están activas, las opuestas no lo estarán, así respetando el flujo de una calle. Estos semáforos indican si un carro puede avanzar después de cierto punto. 

## Proceso de Simulación

### Instalación

Para esta sección debe de quedar claro que se pretende tener un proyecto de Python actuando sobre la librería de mesa y un proyecto de Unity con pro builder para las graficas computaciones. Se tuvo que instalar la librería de mesa, y el paquete de pro builder para poder tener un ambiente funcional para nuestra solución. Aunado a esto también un servidor se tuvo que levantar para hacer una conexión entre la respuesta del Python y algo que Unity pueda entender para así poner a manejar a los agentes en un ambiente de simulacro. 

### Configuración

Dentro del Unity se tuvo que configurar los Scripts necesarios para poder entender los elementos enviados desde Python en estilo de Json. El servidor también tiene que ser configurado para poder actuar como el puente entre ambas aplicaciones y poder enviar y recibir datos de manera correcta. 

### Ejecución 

Dentro de Unity se debe de compilar correctamente el proyecto para posteriormente ver la simulación presionando el botón de Play y viendo como funciona la intersección desde la cámara principal de Unity. 
