\# Taller Semana 3: Modernización,

\# Contenedores y Automatización (CI/CD)

\*\*Tema:\*\* Docker, Docker Compose, APIs REST, Clean Architecture, CI/CD, Principios INVEST y  
Gestión de Riesgos.  
\*\*Contexto del Reto:\*\* "La Salida a Producción" (Deployment & Modernization)  
En la industria real, no basta con que el código funcione en la máquina del desarrollador. Tras  
haber asumido y estabilizado el sistema heredado ("Brownfield") en la iteración anterior, el  
cliente ahora exige que la aplicación se exponga al mundo, sea escalable, portátil y que sus  
pruebas se ejecuten de manera automatizada.  
\*\*La Dinámica:\*\*  
Los equipos continuarán trabajando sobre el repositorio que estabilizaron en el Taller 2\.  
\*\*Misión:\*\* Ustedes deben refactorizar la solución para exponerla a través de una API REST, debatir  
su estado arquitectónico, contenerizar la aplicación para garantizar su portabilidad y construir  
un pipeline de Integración Continua (CI) que valide automáticamente la calidad de cada nuevo  
cambio. Todo esto acompañado de una rigurosa gestión de riesgos integrada en su  
planificación de QA.

\#\# Stack y Herramientas

1\. \*\*IDE \+ AI:\*\* VS Code con GitHub Copilot.  
2\. \*\*Infraestructura y CI:\*\* Docker, Docker Compose, GitHub Actions.  
3\. \*\*Pruebas de API:\*\* Postman.  
4\. \*\*Gestión:\*\* GitHub (Issues, Projects, Actions), GitFlow.

\#\# Flujo de Trabajo

\#\#\# 0\. Fase de Planificación (QA)

Antes de tocar el código o la infraestructura, el equipo debe planificar la transición y evaluar los  
requerimientos.  
● \*\*Actividad 0.1: Historias de Usuario e INVEST.\*\* Definir las historias de usuario necesarias  
para la creación de la API y la contenerización asegurando que cumplan con los Principios  
INVEST (Independientes, Negociables, Valiosas, Estimables, Pequeñas y Testeables).

\#\#\# 1\. Fase de Re-Arquitectura y API REST (DEV)

El sistema actual es probablemente un monolito cerrado. Es hora de abrirlo al ecosistema.  
● \*\*Actividad 1.1: Debate Arquitectónico.\*\* Analizar la estructura actual. Documentar los

\`\`\`  
"dolores" del Monolito heredado y contrastarlos teóricamente con los beneficios que  
aportaría migrar hacia una Clean Architecture.  
● Actividad 1.2: Construcción de la API. Exponer la funcionalidad trabajada en el Taller 2 a  
través de una API REST.  
○ Regla: Deben hacer un uso semánticamente correcto de los Verbos HTTP (GET, POST,  
PUT, DELETE) y manejar adecuadamente los Códigos de Estado (Ej: 200 OK, 201  
Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error).  
○ Entregable: Un archivo ARCHITECTURE.md que contenga el debate arquitectónico y la  
documentación de los endpoints (contrato de la API).  
\`\`\`  
\#\#\# 2\. Fase de Contenerización (DEV)

Garantizar que "si funciona en mi máquina, funciona en cualquier parte".  
● \*\*Actividad 2.1: Creación de la Imagen.\*\* Escribir un Dockerfile optimizado para la  
aplicación.  
● \*\*Actividad 2.2: Orquestación Multicontenedor.\*\* Crear un archivo docker-compose.yml  
que levante la aplicación (API) y al menos un servicio complementario (ej. Base de datos o  
un mock server).  
● \*\*Actividad 2.3: Persistencia de Datos.\*\* Configurar Volúmenes en Docker para asegurar  
que la información generada a través de la API no se pierda al apagar o destruir los  
contenedores.

\#\#\# 3\. Fase de Estrategia de Calidad Continua (QA & DEV)

El código empaquetado debe ser probado, y esto ya no puede ser un proceso manual.  
● \*\*Actividad 3.1: Actualización del Plan de Pruebas y Riesgos.\*\* Evolucionar el documento  
del taller anterior. El nuevo plan debe contemplar pruebas de integración para los nuevos  
endpoints de la API REST. Además, \*\*dentro de este mismo plan\*\* , se debe incluir una  
sección dedicada a la \*\*Gestión de Riesgos\*\*. El equipo deberá investigar y definir la  
estrategia de calidad para el proyecto, consolidando un documento de \*\*Plan de Pruebas\*\*  
que establezca el alcance, los niveles de prueba , las herramientas, calendario de pruebas,  
riesgos.  
● \*\*Actividad 3.2: Diseño de casos de pruebas:\*\* Cada equipo deberá diseñar casos de  
prueba redactados en lenguaje \*\*Gherkin\*\* (Given/When/Then), aplicando técnicas de  
diseño para maximizar la cobertura. Estos escenarios deberán organizarse en una \*\*hoja de  
cálculo\*\* que funcione como matriz de pruebas, donde posteriormente se registrará la  
\*\*ejecución manual\*\* indicando el resultado obtenido (Pasó/Falló).  
● \*\*Actividad 3.3: Integración Continua (CI básico).\*\* Crear un workflow en GitHub Actions  
(.github/workflows/ci.yml).  
○ \_Regla:\_ El pipeline debe dispararse automáticamente con cada Push o Pull Request  
hacia todas las ramas (main, develop, feature/\*\*\*). Debe construir el entorno y ejecutar  
las pruebas creadas (TDD) en el Taller 2, fallando e impidiendo la integración si alguna  
prueba no pasa. Cobertura mínima: 70%.

\#\# Entregables Finales del Taller

\`\`\`  
● Repositorio Actualizado:  
○ Historial de Git reflejando el uso de GitFlow para la creación de la API y la  
infraestructura.  
○ Archivos Dockerfile y docker-compose.yml funcionales en la raíz del proyecto.  
○ Directorio .github/workflows/ con el pipeline de CI integrado.  
● Documentación de Ingeniería y QA:  
○ ARCHITECTURE.md: Análisis Monolito vs Clean Architecture y especificación/contrato  
de la API REST (Verbos y Códigos).  
○ TEST\_PLAN\_V3.md: Plan de pruebas actualizado (enfocado en la API). Debe incluir la  
actualización del Plan de Pruebas y Riesgos (diferenciando Riesgos de Proyecto vs  
Producto), el diseño de las pruebas y la aplicación de los principios INVEST en las  
historias.  
● Evidencia de Calidad y Ejecución (Sesión Evaluar):  
○ Enlace a la pestaña "Actions" del repositorio mostrando ejecuciones exitosas (en  
verde) del pipeline de CI.  
○ Capturas de peticiones exitosas y fallidas a la API usando Postman demostrando  
el manejo de los códigos de estado.  
\`\`\`  
\#\# Criterios de Evaluación

\`\`\`  
● Diseño de API (DEV): ¿La API respeta los principios RESTful, usando correctamente los  
verbos HTTP y devolviendo los códigos de estado adecuados según la situación?  
● Portabilidad (DEV): ¿El docker-compose up levanta todo el ecosistema de la aplicación  
sin errores y los volúmenes persisten los datos tras reiniciar?  
● Automatización CI (DEV/QA): ¿El pipeline de GitHub Actions captura y detiene la subida  
de código si los tests del Taller 2 se rompen?  
● Rigor Analítico (QA): ¿El plan de pruebas incluye una matriz de riesgos que demuestra  
comprensión real de la diferencia entre riesgos del producto técnico y riesgos de la  
gestión del proyecto? ¿Se aplicaron bien los principios INVEST en las historias?  
\`\`\`  
\#\# Pautas para sesión Evaluar

\`\`\`  
● Tiempo estimado: 20-25 minutos por grupo  
● El orden se sortea el día de la sesión  
● Presentación: Funcionalidad, Entregables (Documentación) y Evidencia de Calidad y  
Ejecución.  
\`\`\`

