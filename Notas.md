# Para usar python de forma mas comoda se recomienda crear entornos virtuales

```shell
python -m venv venv curso-fastapi
```
Para activar el entorno virtual
```shell
.\Scripts\Activate.ps1
```

Para desactivar el entorno virtual
```shell
deactivate
```

Instalar fastapi, para instalar mas dependecias junto a fastapi se colocan [standard], que instala otras dependecias que son necesarias para que puedamos correr fastapi en nuestro entorno, las dos comillas es para que no se interpreten los []

```shell
pip install "fastapi[standard]"
```
Para ejecutar el proyecto te situas al nivel de main.py y se ejecuta:
```shell
fastapi dev
```
Para usar sqlModel se instala una combinacion de SQLAlchemy y Pydantic

```shell
pip install sqlmodel
```

Para saber las versiones de las dependencias instaladas de fastapi
```shell
pip freeze | Select-String fastapi 
```

Para saber las versiones de las dependencias instaladas de sqlmodel
```shell
pip freeze | Select-String sqlmodel
```
