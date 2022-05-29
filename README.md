# Introducción a Docker

> Autor: Enmanuel Verdesia Suárez

Docker brinda la capacidad de empaquetar y ejecutar una aplicación en un entorno aislado llamado contenedor. Los contenedores son livianos y contienen todo lo necesario para ejecutar la aplicación, por lo que no dependen de lo que está instalado en el host. Además, se pueden compartir fácilmente y asegurarse de que todas las personas con las que se comparte obtengan una versión que funciona de la misma manera. Adicionalmente permite manejar la infraestructura de la misma forma que se manejan las aplicaciones, lo que disminuye el tiempo entre escribir el código y llevarlo a producción.

## Instalación

El proceso de instalación es específico para la plataforma en que se vaya a usar. Para realizarlo es recomendable ir a la documentación oficial pues puede sufrir actualizaciones o modificaciones.

Siga los pasos de acuerdo a su sistema operativo e instale Docker desde [aquí](https://docs.docker.com/get-docker/).

## Objetos de Docker

### Imágenes

Una imagen es una plantilla de solo lectura con las instrucciones necesarias para crear un contenedor de Docker. Frecuentemente una imagen se construye sobre otra imagen con información adicional.

Por ejemplo para una aplicación desarrollada en Python se puede tomar como imagen base una versión de Python apropiada y sobre esta crear una nueva imagen con el código y todas las dependencias instaladas para ponerla en producción

De esta forma se pueden usar imágenes propias o usar desarrolladas por terceros. Para construir una imagen es necesario crear un `Dockerfile` con los pasos necesarios para crear la imagen y ejecutarla. Cada instrucción en este archivo crea una capa en la imagen, de esta forma si se cambia una instrucción solo es necesario modificar las capas afectadas. Este proceso hace que las imágenes sean mucho más livianas que otros métodos de virtualización

A continuación se muestra un Dockerfile básico para crear la imagen de un programa en Python.

```Dockerfile
# define la imagen base
FROM python:3.9.5
# crea el directorio /app y se ubica en el
WORKDIR /app
# copia el contenido del programa
COPY . .
# instala las dependencias
RUN pip3 install -r requirements.txt    
# comando ejecutado por defecto cuando se crea un contenedor
# a partir de la imagen
CMD ["python3", "main.py"]
```

Cada una de estas instrucciones crea una capa en la imagen. Por ejemplo si otra imagen también tiene como imagen base `FROM python:3.10` compartirá junto con la anterior el mismo espacio en disco para esa capa.

> 💡 Puede descargar las imágenes de Docker sin consumo de internet a través del proxy de la UCLV `docker.uclv.cu`. Por ejemplo en el Dockerfile anterior puede usar la imagen base: `FROM docker.uclv.cu/python:3.10`.

> 💡 Puede instalar las dependencias en Python sin consumo de internet a través del proxy de la UCI `http://nexus.prod.uci.cu/repository/pypi-proxy/simple/`. Por ejemplo en el Dockerfile anterior puede instalar las dependencias con el comando: `pip install -r requirements.txt --index-url http://nexus.prod.uci.cu/repository/pypi-proxy/simple/ --trusted-host nexus.prod.uci.cu`.

Puede obtener más información sobre como crear Dockerfiles en la [documentación oficial](https://docs.docker.com/engine/reference/builder/).

Una vez creado el Dockerfile anterior basta correr el siguiente comando para crear su imagen:

```
docker image build -t my-first-image .
```

El parámetro `-t <name>` permite asignarle un nombre específico a la imagen. Este comando toma como receta el Dockerfile en el directorio en que se ejecuta, para especificar uno se usa el parámetro `-f <file>`.

Como probablemente usted no tenga la imagen base de Python 3.10 en su repositorio local este comando lo primero que va a hacer es descargarla. Esto puede demorar unos minutos de acuerdo con su conexión. Este proceso se realiza solo una vez, en un futuro siempre que use esa imagen como base será la misma que descargó.

> 💡 Para descargar una imagen puede usar `docker pull <image:tag>`. Por ejemplo: `docker pull docker.uclv.cu/python:3.9.5`.

El comando anterior ejecuta una a una las instrucciones del Dockerfile y una vez completado usted debe tener la nueva imagen creada y además de ella la imagen base que tuvo q descargar. Para mostrar sus imágenes pude usar el siguiente comando:

```
docker image ls
```

Obtendrá la lista de sus imágenes

```
REPOSITORY                     TAG       IMAGE ID       CREATED              SIZE
my-first-image                 latest    ae1d2c9f75d3   About a minute ago   892MB
docker.uclv.cu/python          3.9.5     9b0d330dfd02   About a minute ago   886MB
```

### Contenedores

Los contenedores pueden ser vistos com instancias de las imágenes. A partir de una imagen se puede crear múltiples contenedores que pueden funcionar de forma independiente. Estos se pueden crear, iniciar, detener, mover o borrar usando la API de Docker o la consola de comandos. Además se puede conectar un contenedor a una o más redes, vincularle un almacenamiento o incluso crear una nueva imagen basada en su estado actual.

Un contenedor esta definido por su imagen así como cualquier opción de configuración proveída a la hora de crearlo o iniciarlo. Cuando un contenedor es eliminado, cualquier cambio a su estado no almacenado en un medio persistente desaparece.

Para iniciar un contenedor puede usar el comando `docker run`, por ejemplo:

```
docker container run my-first-image
```

Esto creará un contenedor basado en la imagen y ejecutar su punto de entrada, en este caso `main.py`. El ejemplo encontrado en `basic-python/` da como resultado:

```
❯ docker run my-first-image             
Hello world. Do you like Go?
```

Al comando run se le pueden pasar diferentes parámetros que se pueden consultar con `docker container run --help` como son:

- `-d`: desvincula el contenedor de la consola actual.
- `-e`: añade variables de entorno al contenedor.
- `--expose`: expone un puerto del contenedor al host, útil para acceder al contenedor desde una aplicación externa.
- `-v`: vincula un volumen al contenedor, útil para persistir información.
- `--name`: asigna un nombre al contenedor creado, se usa para referenciarlo de una forma más fácil, por defecto se le asigna al azar un adjetivo junto al nombre de un científico famoso.

De igual forma a con las imágenes se pueden mostrar los contenedores que están en ejecución o detenidos con el siguiente comando:

```
❯ docker container ls -a
CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS                      PORTS   NAMES
2b8af4003e6d   my-first-image   "python3 main.py"   13 minutes ago   Exited (0) 13 minutes ago           quizzical_proskuriakova
```

Se puede crear otro contenedor a partir de la misma imagen y este funciona independiente al anterior:

```
❯ docker container run my-first-image        
Hello world. Do you like Typescript?

❯ docker container ls -a             
CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS                      PORTS   NAMES
3479cfd234fd   my-first-image   "python3 main.py"   12 seconds ago   Exited (0) 12 seconds ago           dreamy_robinson
2b8af4003e6d   my-first-image   "python3 main.py"   33 minutes ago   Exited (0) 33 minutes ago           quizzical_proskuriakova
```

Estos contenedores anteriores esta detenidos y se pueden reiniciar, lo que causa que se invoque nuevamente el punto de entrada:

```
❯ docker container restart dreamy_robinson quizzical_proskuriakova 
dreamy_robinson
quizzical_proskuriakova

❯ docker container logs dreamy_robinson                           
Hello world. Do you like Typescript?
Hello world. Do you like C#?

❯ docker container logs quizzical_proskuriakova 
Hello world. Do you like Go?
Hello world. Do you like Haskell?
```

> 💡 Para consultar los logs de un contenedor puede usar el comando `docker container logs <container-name-or-id>`.

Como se puede observar los contenedores volvieron a ejecutar su punto de entrada a partir del estado que tenían anteriormente.

Para destruir los contenedores puede usar el comando `docker container rm <container-name-or-id>`:

```
❯ docker container rm dreamy_robinson quizzical_proskuriakova     
dreamy_robinson
quizzical_proskuriakova

❯ docker container ls -a                                     
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
```

Adicionalmente se puede usar el parámetro `-f` para forzar y destruir un contenedor que esté en ejecución.

### Volúmenes

Los volúmenes son la mejor forma de persistir datos en Docker. Otras opciones son [bind mounts](https://docs.docker.com/storage/bind-mounts/) y [tmpfs mounts](https://docs.docker.com/storage/tmpfs/).

![](images/types-of-mounts-volume.png)

Los volúmenes permiten compartir espacio del almacenamiento entre el host y contenedores. Ofrecen una serie de ventajas, entre ellas: 

- Fáciles de copiar y migrar.
- Se pueden administrar usando la API de Docker o la consola de comandos.
- Funcionan tanto en contenedores de Windows como de Linux.
- Pueden ser compartidos de forma sencilla entre múltiples contenedores.
- Pueden obtenerse diferentes funcionalidades a través de drivers.

Para crear un volumen se puede usar el comando `docker volume create <vol-name>`.

```
❯ docker volume create my-vol  
my-vol
```

Puedes listar todos los volúmenes con `docker volume ls` e inspeccionar un volumen con `docker volume inspect <vol-name>`.

```
❯ docker volume ls           
DRIVER    VOLUME NAME
local     my-vol

❯ docker volume inspect my-vol                                                          
[
    {
        "CreatedAt": "2022-05-29T15:17:36-04:00",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
        "Name": "my-vol",
        "Options": {},
        "Scope": "local"
    }
]
```

Al inspeccionar un volumen podemos ver la información relacionada a este. En el campo `Mountpoint` se puede ver la dirección del host donde se va a persistir la información. Cuando un volumen se mapea a una dirección interna del contenedor los cambios son reflejados de forma bidireccional entre un y otro.

Para usar este volumen en un contenedor se puede usar el parámetro `-v` al crear el contenedor:

```
docker container run -v my-vol:/app --name my-app my-first-image
```

Ahora podemos inspeccionar el contenedor y verificar que está usando efectivamente el volumen designado, para ello se usa el comando `docker container inspect <container-name-or-id>`.

```
❯ docker container inspect my-app
# Omitted output...
        "Mounts": [
            {
                "Type": "volume",
                "Name": "my-vol",
                "Source": "/var/lib/docker/volumes/my-vol/_data",
                "Destination": "/app",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ],
# Omitted output...
```

Se puede apreciar que en la seccion de `Mounts` el volumen usado es el definido previamente y que `Source` coincide con el `Mountpoint` del volumen. El directorio interno del contenedor que apunta al volumen está indicado por `Destination`, en este caso `/app`.

De hecho podemos comprobar que cuando se creó el contenedor los ficheros del contenedor ubicados en `/app` fuero copiados al volumen:

```
❯ sudo bash
root@verdesia-laptop:/home/verdesia# cd /var/lib/docker/volumes/my-vol/_data
root@verdesia-laptop:/var/lib/docker/volumes/my-vol/_data# ls
Dockerfile  main.py  requirements.txt
```

Sí se añade una archivo a este directorio, por ejemplo ejecutando `touch file.txt` este estará disponible dentro del contenedor.

Puede obtener más información sobre como manejar volúmenes en la [documentación oficial](https://docs.docker.com/storage/volumes/).

### Otros objetos

Además existen otro objetos como redes, plugins, etc. los cuales ofrecen más funcionalidades pero que están fuera del alcance de esta introducción.

## Tarea Propuesta

En el directorio `fastapi-homework/` se encuentra una aplicación simple escrita con FastAPI. El Dockerfile se encuentra vació.

Usted debe:
- Escribir el Dockerfile.
  - Use la versión 3.9.5 de Python.
  - El comando de inicio de la imagen sea `uvicorn main:app`.
- Crear la imagen a partir del Dockerfile.
- Crear dos contenedores a partir de la imagen anterior.
  - Cada contenedor debe exponer un puerto distinto al host para recibir conexiones.
  - Cada contenedor debe recibir una variable de entorno `MSG` la cual es un mensaje que va a devolver la API cuando se haga una petición `GET` a `/`.
- Añadir persistencia a los logs de la API.
  - Crear un volumen llamado `api-logs`
  - Modificar el código de tal forma que cada vez que se haga una petición al endpoint dentro de uno de los contenedores, este lo registre de forma persistente en un fichero que almacene sus logs en el volumen creado.
- Conectarse con su navegador a `http://localhost:<puerto>/` de cada contenedor.
  - Comprobar que el mensaje recibido es el esperado.
  - Comprobar que ambos contenedores persisten sus logs en el volumen.

## Referencias

- [Documentación Oficial de Docker](https://docs.docker.com)
