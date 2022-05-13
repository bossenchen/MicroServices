# 使用 Python 创建微服务

作为一名 Python 开发人员，您可能听说过微服务这个术语，并希望自己构建一个 Python 微服务。 微服务是构建高度可扩展应用程序的绝佳架构。 在开始使用微服务构建应用程序之前，您必须熟悉使用微服务的优点和缺点。
在本文中，您将了解使用微服务的优点和缺点。 您还将了解如何构建自己的微服务并使用 Docker Compose 进行部署。

在本教程中，您将学习以下内容：

- 微服务的优点和缺点
- 为什么应该使用 Python 构建微服务
- 如何使用 FastAPI 和 PostgreSQL 构建 REST API
- 如何使用 FastAPI 构建微服务
- 如何使用 docker-compose 运行微服务
- 如何使用 Nginx 管理微服务

您将首先使用 FastAPI 构建一个简单的 REST API，然后使用 PostgreSQL 作为我们的数据库。 然后，将相同的应用程序扩展到微服务。

# 微服务简介

微服务是将大型单体应用程序分解为专门用于特定服务/功能的单个应用程序的方法。 这种方法通常被称为面向服务的架构（**Service-Oriented Architecture**）或 SOA。

在单体架构中，每个业务逻辑都驻留在同一个应用程序中。 用户管理、身份验证和其他功能等应用程序服务使用相同的数据库。

在**微服务架构**中，应用程序被分解为几个独立的服务，这些服务在不同的进程中运行。 对于应用程序的不同功能，有一个不同的数据库，并且服务使用 HTTP、AMQP 或 TCP 等二进制协议相互通信，具体取决于每个服务的性质。
也可以使用 [RabbitMQ](https://www.rabbitmq.com/)、[Kafka](https://kafka.apache.org/) 或 [Redis](https://redis.io/)
等消息队列来执行服务间通信。

## 微服务的优点

微服务架构有很多好处。 其中一些好处是：

- 松散耦合的应用程序意味着可以使用最适合的技术来构建不同的服务。 因此，开发团队不受启动项目时所做选择的限制。
- 由于不同的服务负责不同的功能，这使得更容易理解和控制应用程序。
- 应用程序扩展也变得更容易，因为如果其中一项服务需要高 GPU 使用率，那么只有包含该服务的服务器需要具有高 GPU，而其他服务可以在普通服务器上运行。

## 微服务的缺点

微服务架构不是解决所有问题的灵丹妙药，也有一些缺点。包括：

- 由于不同的服务使用不同的数据库，涉及多个服务的事务需要使用最终一致性。
- 在第一次尝试时很难实现服务的完美拆分，这需要在实现最好的服务分离之前进行迭代。
- 由于服务之间通过网络交互进行通信，这使得应用程序由于网络延迟和服务慢而变慢。

## Python 为什么需要微服务

Python 是构建微服务的完美工具，因为其具有出色的社区、简单的学习曲线和大量的库。 由于在 Python 中引入了异步编程，出现了性能与 GO 和 Node.js 相当的 Web 框架。

# FastAPI 简介

FastAPI 是一个现代、高性能的 Web 框架，且具有大量很酷的功能，例如基于 OpenAPI 的自动文档以及内置的序列化和验证库。 有关 FastAPI
中所有很酷的功能的列表，请参见[此处](https://fastapi.tiangolo.com/features/)。

## 为什么使用 FastAPI

之所以 FastAPI 是 Python 中用于构建为服务的很好的选择，是因为：

- 自动文档
- `async`/`await` 支持
- 内置的验证和序列化
- 100 % 的类型注解，因为可以很好的进行自动补全

## 安装 FastAPI

在安装 FastAPI 之前，创建一个新目录 `movie_service` 并使用 `virtualenv` 在新创建的目录中创建一个新的虚拟环境。

如果还没有安装 `virtualenv`，则可以通过下面的命令安装：

```shell
pip install virtualenv
```

现在创建一个新的虚拟环境：

```shell
virtualenv env
```

如果是在 Linux 或 Mac 上，则可以使用下面的命令激活虚拟环境：

```shell
source ./env/bin/activate
```

Windows 用户可以运行下面的命令激活虚拟环境：

```shell
.\env\Scripts\activate
```

现在就可以运行下面的命令安装 FastAPI 了：

```shell
pip install fastapi
```

由于 FastAPI 没有内置服务，因此需要安装 `uvicorn` 才能运行。 `uvicorn` 是一个允许使用 async/await 功能的 ASGI 服务器。

使用命令安装 `uvicorn`：

```shell
pip install uvicorn
```

## 使用 FastAPI 创建示例 REST API

在学习使用 FastAPI 构建微服务之前，让我们先来学习一些关于 FastAPI 的基础知识。创建一个新的名为 `app` 的目录，并在其中创建一个名为 `main.py` 的文件。

将下面的代码添加到 `main.py` 文件中：

```python
# movie-service/app/main.py
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index():
    return {"Real": "Python"}
```

上面的代码首先导入并实例化 `FastAPI`，然后注册返回 JSON 的根端点 `/` 。

可以使用 `uvicorn app.main:app --reload` 运行应用程序服务器。 这里 `app.main` 表示使用 `app` 目录中的 `main.py` 文件， `:app` 表示 `FastAPI` 实例名称。

可以从 `http://127.0.0.1:8000` 访问该应用程序。 要访问自动文档，请访问 `http://127.0.0.1:8000/docs`。 可以从浏览器本身玩转 API 并与之交互。

下面来为应用程序添加一些 CRUD 功能。

将 `main.py` 更新为如下所示：

```python
# movie-service/app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    }
]


class Movie(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]


@app.get('/', response_model=List[Movie])
async def index():
    return fake_movie_db
```

如上所示，创建了一个继承自 `BaseModel` 的新类 `Movie`，其中的 `BaseModel` 是 Pydantic 中由于创建模型类的基类。

`Movie` 模型包含名称、照片、流派和演员表。 Pydantic 内置了 FastAPI，这使得模型和请求验证变得轻而易举。

如果前往文档站点，会看到示例响应部分中已经提到了电影模型的字段。 这是可能的，因为已经在路由定义中定义了 `response_model`。

现在，添加端点以将电影添加到我们的电影列表中。

添加一个新的端点定义来处理 POST 请求。

```python
@app.post('/', status_code=201)
async def add_movie(payload: Movie):
    movie = payload.dict()
    fake_movie_db.append(movie)
    return {'id': len(fake_movie_db) - 1}
```

现在，转到浏览器并测试新的 API。 尝试添加包含无效字段或不包含必填字段的电影，并查看验证是否由 FastAPI 自动处理。

让我们添加一个新端点来更新电影。

```python
from fastapi import HTTPException


@app.put('/{id}')
async def update_movie(id: int, payload: Movie):
    movie = payload.dict()
    movies_length = len(fake_movie_db)
    if 0 <= id <= movies_length:
        fake_movie_db[id] = movie
        return None
    raise HTTPException(status_code=404, detail="Movie with given id not found")
```

这里 `id` 是 `fake_movie_db` 列表的索引。

**注意：**记得从 `fastapi` 中的导入 `HTTPException`。

现在还可以添加端点来删除电影。

```python
@app.delete('/{id}')
async def delete_movie(id: int):
    movies_length = len(fake_movie_db)
    if 0 <= id <= movies_length:
        del fake_movie_db[id]
        return None
    raise HTTPException(status_code=404, detail="Movie with given id not found")
```

在继续之前，让我们以更好的方式构建我们的应用程序。 在 `app` 目录中创建一个新文件夹 `api`，并在其中创建一个新文件 `movies.py`。 将所有与路由相关的代码从 `main.py` 移动到 `movies.py`。
所以，`movies.py` 应该如下所示：

```python
# movie-service/app/api/movies.py
from typing import List
from fastapi import APIRouter, HTTPException

from .models import Movie

fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    }
]

movies = APIRouter()


@movies.get('/', response_model=List[Movie])
async def index():
    return fake_movie_db


@movies.post('/', status_code=201)
async def add_movie(payload: Movie):
    movie = payload.dict()
    fake_movie_db.append(movie)
    return {'id': len(fake_movie_db) - 1}


@movies.put('/{id}')
async def update_movie(id: int, payload: Movie):
    movie = payload.dict()
    movies_length = len(fake_movie_db)
    if 0 <= id <= movies_length:
        fake_movie_db[id] = movie
        return None
    raise HTTPException(status_code=404, detail="Movie with given id not found")


@movies.delete('/{id}')
async def delete_movie(id: int):
    movies_length = len(fake_movie_db)
    if 0 <= id <= movies_length:
        del fake_movie_db[id]
        return None
    raise HTTPException(status_code=404, detail="Movie with given id not found")
```

在这里，使用 FastAPI 中的 `APIRouter` 注册了一个新的 API 路由。

此外，在 `api` 中创建一个新文件 `models.py`，并将 Pydantic 模型相关的代码移入其中。

```python
# movie-service/app/api/models.py
from typing import List
from pydantic import BaseModel


class Movie(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]
```

然后，在 `app/main.py` 文件中注册新的路由：

```python
# movie-service/app/main.py
from fastapi import FastAPI

from .api.movies import movies

app = FastAPI()

app.include_router(movies)
```

最终，应用程序的目录结果应该是下面这样的：

```
movie-service
├── app
│   ├── api
│   │   ├── models.py
│   │   ├── movies.py
│   |── main.py
└── env
```

在继续之前，请确保应用程序正常运行。

## 在 FastAPI 中使用 PostgreSQL 数据库

前面的代码中使用了 Python 列表来存储电影，现在可以我们将使用数据库来存储电影。 为此，将使用 [PostgreSQL](https://www.postgresql.org/)。在数据库中创建一个名为 `movie` 的数据库。

使用 [encode/databases](https://github.com/encode/databases) 通过 `async` 和 `await` 支持连接到数据库。
在[此处](https://florimond.dev/blog/articles/2019/08/introduction-to-asgi-async-python-web/)了解有关 Python 中的 `async`/`await`
的更多信息

使用以下命令安装所需的库：

```shell
pip install 'databases[postgresql]'
```

上面的命令将会安装 `sqlalchemy` 和 `asyncpg`，后者是提供异步支持的 PostgreSQL 驱动程序。

在 `app/api` 目录中创建一个名为 `db.py` 的文件，此文件中将包含用于 REST API 的数据库模型。

```python
# movie-service/app/api/db.py

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URL = 'postgresql://neo:admin@192.168.3.40/movie'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts', ARRAY(String))
)

database = Database(DATABASE_URL)
```

`DATABASE_URI` 是用于连接到 PostgreSQL 数据库的 URL。 `movie_user` 是数据库用户名，`movie_password` 是数据库用户密码，`movie` 是数据库名。

就像在 [SQLAlchemy](https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/) 中一样，必须已经在 `movie`
数据库中创建了表。

更新 `main.py` 以连接到数据库。 `main.py` 应如下所示：

```python
# movie-service/app/main.py

from fastapi import FastAPI
from .api.movies import movies
from .api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(movies)
```

FastAPI 提供了一些事件处理程序，可以使用它们在应用程序启动时连接到数据库，并在应用程序关闭时断开连接。

更新 `movies.py`，使其使用数据库而不是 Python 列表。

```python
# movie-service/app/api/movies.py
from typing import List
from fastapi import APIRouter, HTTPException

from .models import MovieIn, MovieOut
from . import crud

movies = APIRouter()


@movies.get('/', response_model=List[MovieOut])
async def index():
    return await crud.get_all_movies()


@movies.post('/', status_code=201)
async def add_movie(payload: MovieIn):
    movie_id = await crud.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }

    return response


@movies.put('/{movie_id}')
async def update_movie(movie_id: int, payload: MovieIn):
    movie = await crud.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)
    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)

    return await crud.update_movie(movie_id, updated_movie)


@movies.delete('/{movie_id}')
async def delete_movie(movie_id: int):
    movie = await crud.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await crud.delete_movie(movie_id)
```

添加 `crud.py` 来维护数据库。

```python
# movie-service/app/api/crud.py

from app.api.models import MovieIn, MovieOut, MovieUpdate
from app.api.db import movies, database


async def add_movie(payload: MovieIn):
    query = movies.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_movies():
    query = movies.select()
    return await database.fetch_all(query=query)


async def get_movie(id):
    query = movies.select(movies.c.id == id)
    return await database.fetch_one(query=query)


async def delete_movie(id: int):
    query = movies.delete().where(movies.c.id == id)
    return await database.execute(query=query)


async def update_movie(id: int, payload: MovieIn):
    query = (
        movies
            .update()
            .where(movies.c.id == id)
            .values(**payload.dict())
    )
    return await database.execute(query=query)
```

更新 `models.py` 以便可以将 Pydantic 模型与 SQLAlchemy 表一起使用。

```python
# movie-service/app/api/models.py

from pydantic import BaseModel
from typing import List, Optional


class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]


class MovieOut(MovieIn):
    id: int


class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts: Optional[List[str]] = None
```

这里的 `MovieIn` 是用于将电影添加到数据库的基本模型。 在从数据库中获取 `MovieIn` 模型时，必须将 `id` 添加到此模型中，因此使用 `MovieOut` 模型。 `MovieUpdate`
模型允许将模型中的值设置为可选的，以便在更新电影时只发送需要更新的字段。

现在，前往浏览器文档站点并开始使用 API。

# 微服务数据管理模式

在微服务中管理数据是构建微服务最具挑战性的方面之一。 由于应用程序的不同功能由不同的服务处理，因此数据库的使用可能会很棘手。

以下是一些可用于管理应用程序中的数据流的模式。

## 每个服务一个数据库

如果希望微服务尽可能松散耦合，那么为每个服务使用一个数据库是比较好的选择。 每个服务拥有不同的数据库使我们能够独立扩展不同的服务。 涉及多个数据库的事务是通过定义良好的 API 完成的。
这带来了其缺点，因为实现涉及多个服务的业务事务并不简单。 此外，网络开销的增加也降低了其使用效率。

## 共享数据库

如果有很多事务涉及多个服务，最好使用共享数据库。 这带来一项好处，即应用程序的高度一致性，但带走了微服务架构带来的大部分好处。 开发一项服务的开发人员需要与其他服务中的模式更改进行协调。

## API 组合

在涉及多个数据库的事务中，API Composer 充当 API 网关并按所需顺序执行对其他微服务的 API 调用。 最后，每个微服务的结果在执行内存连接后返回给客户端服务。 这种方法的缺点是大型数据集的内存连接效率低下。

# 使用 Docker 创建 Python 微服务

使用 Docker 可以大大减少部署微服务的痛苦。 Docker 有助于封装每个服务并独立对其进行扩展。

## 安装 Docker 和 Docker Compose

Docker 用于管理容器，Docker Compose 用于定义和运行多个 Docker 容器。 Docker Compose 还有助于容器之间的轻松交互。

## 创建电影服务

由于在开始使用 FastAPI 时已经完成了大量构建电影服务的工作，因此我们将重用已经编写的代码。 创建一个全新的文件夹 `python-microservices`，并将之前的 `movie-service` 文件夹和其中的文件移入其中。

现在，目录结构应该是下面这样的：

```
python-microservices/
└── movie-service/
    ├── app/
    └── env/
```

首先创建一个 `requirements.txt` 文件，并在其中保留将在电影服务中使用的所有依赖项。 在 `movie-service` 中创建一个新文件 `requirements.txt` 并添加以下内容：

```
fastapi[all] == 0.75.2
httpx == 0.22.0
databases[postgresql] == 0.5.5
```

上面的代码已经用到了 `requirements.txt` 中列出的所有库，除了在进行服务到服务 API 调用时要使用的 `httpx`。

使用以下内容在 `movie-service` 中创建一个 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/
```

首先，定义要使用的 Python 版本。 然后将 `WORKDIR` 设置为 Docker 容器内的 `app` 文件夹中。 然后安装在应用程序中所必需的   `gcc`。最后，安装 `requirements.txt`
中的所有依赖项，并将所有文件复制到 `movie-service/app` 中。

更新 `db.py`，将：

```python
DATABASE_URL = 'postgresql://movie_user:movie_password@localhost/movie_db'
```

替换为：

```python
DATABASE_URL = os.getenv('DATABASE_URL')
```

**注意：**不要忘记在文件的最上面导入 `os`。

需要这样做，以便以后可以提供 `DATABASE_URL` 作为环境变量。

另外，更新 `main.py`，并将：

```python
app.include_router(movies)
```

替换为：

```python
app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
```

在这里，添加了前缀 `/api/v1/movies`，这样管理不同版本的 API 变得更加容易。 此外，标签使在 FastAPI 文档中查找与 `movies` 相关的 API 变得更加容易。

另外，还需要更新模型，以便 `casts` 存储演员表的 ID 而不是实际名称。 因此，将 `models.py` 更新为如下所示：

```python
# python-microservices/movie-service/app/api/db.py
from pydantic import BaseModel
from typing import List, Optional


class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts_id: List[int]


class MovieOut(MovieIn):
    id: int


class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts_id: Optional[List[int]] = None
```

同样，需要更新数据库表，让我们更新 `db.py`：

```python
# python-microservices/movie-service/app/api/db.py

import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts_id', ARRAY(Integer))
)

database = Database(DATABASE_URL)
```

现在，在添加新电影或更新电影之前，更新 `movies.py` 以检查具有给定 ID 的演员表是否存在于演员表服务中。

```python
from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import MovieOut, MovieIn, MovieUpdate
from app.api import db_manager
from app.api.service import is_cast_present

movies = APIRouter()


@movies.post('/', response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }

    return response


@movies.get('/', response_model=List[MovieOut])
async def get_movies():
    return await db_manager.get_all_movies()


@movies.get('/{id}/', response_model=MovieOut)
async def get_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movies.put('/{id}/', response_model=MovieOut)
async def update_movie(id: int, payload: MovieUpdate):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)

    return await db_manager.update_movie(id, updated_movie)


@movies.delete('/{id}', response_model=None)
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await db_manager.delete_movie(id)
```

让我们添加一个服务来对演员表服务进行 API 调用：

```python
# python-microservices/movie-service/app/api/service.py

import os
import httpx

CAST_SERVICE_HOST_URL = 'http://localhost:8002/api/v1/casts/'
url = os.environ.get('CAST_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL


def is_cast_present(cast_id: int):
    r = httpx.get(f'{url}{cast_id}/')
    return True if r.status_code == 200 else False
```

进行 API 调用以获取具有给定 `cast_id` 的演员表，如果演员表存在则返回 `True`，否则返回 `False`。

## 创建演员表服务

与 `movie-service` 类似，使用 FastAPI 和 PostgreSQL 数据库创建 `casts-service`。

创建如下文件夹结构：

```
python-microservices/
.
├── cast_service/
│   ├── app/
│   │   ├── api/
│   │   │   ├── casts.py
│   │   │   ├── db_manager.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── movie_service/
...
```

`requirements.txt` 内容如下：

```
fastapi[all] == 0.75.2
httpx == 0.22.0
databases[postgresql] == 0.5.5
```

`Dockerfile` 内容如下：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/
```

`main.py` 内容如下：

```python
from fastapi import FastAPI
from .api.casts import casts
from .api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])
```

添加了 `/api/v1/casts` 前缀，以便更轻松地管理 API。 此外，添加标签可以使得在 FastAPI 文档中查找与演员表相关的文档更加容易。

`casts.py` 内容如下：

```python
from fastapi import APIRouter, HTTPException

from .models import CastOut, CastIn
from . import crud

casts = APIRouter()


@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await crud.add_cast(payload)

    response = {
        'id': cast_id,
        **payload.dict()
    }

    return response


@casts.get('/{cast_id}/', response_model=CastOut)
async def get_cast(cast_id: int):
    cast = await crud.get_cast(cast_id)
    if not cast:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast
```

## 使用 Docker Compose 运行微服务

要运行微服务，请创建一个 `docker-compose.yml` 文件并将如下内容添加到其中：

```dockerfile
version: '3.7'

services:
  movie_service:
    build: ./movie-service
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    volumes:
      - ./movie-service/:/app/
    ports:
      - 8001:8000
    environment:
      - DATABASE_URI=postgresql://movie_db_username:movie_db_password@movie_db/movie_db_dev
      - CAST_SERVICE_HOST_URL=http://cast_service:8000/api/v1/casts/

  movie_db:
    image: postgres:12.1-alpine
    volumes:
      - postgres_data_movie:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=movie_db_username
      - POSTGRES_PASSWORD=movie_db_password
      - POSTGRES_DB=movie_db_dev

  cast_service:
    build: ./cast-service
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    volumes:
      - ./cast-service/:/app/
    ports:
      - 8002:8000
    environment:
      - DATABASE_URI=postgresql://cast_db_username:cast_db_password@cast_db/cast_db_dev

  cast_db:
    image: postgres:12.1-alpine
    volumes:
      - postgres_data_cast:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=cast_db_username
      - POSTGRES_PASSWORD=cast_db_password
      - POSTGRES_DB=cast_db_dev

volumes:
  postgres_data_movie:
  postgres_data_cast:
```

这里有 4 个不同的服务，movie_service、movie_service 数据库、cast_service 和 cast_service 数据库。 已将 movie_service 暴露给端口 8001，类似地将
cast_service 暴露给端口 8002。

对于数据库，使用了卷，以便在 Docker 容器关闭时数据不会被破坏。

使用以下命令运行 `docker-compose`：

```shell
docker-compose up -d
```

如果 Docker 容器不存在，上述命令创建并运行它们。

前往 `http://localhost:8002/docs` 以在演员表服务中添加演员表。 同样，前往 `http://localhost:8001/docs` 将电影添加到电影服务中。

## 通过 Nginx 使用单个主机地址访问两个服务

已经使用 Docker Compose 部署了微服务，但有一个小问题。 每个微服务都需要使用不同的端口进行访问。 可以使用 Nginx 反向代理解决此问题，使用 Nginx 可以直接请求添加一个中间件，该中间件根据 API URL
将请求路由到不同的服务。

在 `python-microservices` 中添加一个新文件 `nginx_config.conf`，内容如下。

```nginx
server {
  listen 8080;

  location /api/v1/movies {
    proxy_pass http://movie_service:8000/api/v1/movies;
  }

  location /api/v1/casts {
    proxy_pass http://cast_service:8000/api/v1/casts;
  }

}
```

在这里，在端口 8080 上运行 Nginx，如果端点以 `/api/v1/movies` 开头，则将请求路由到电影服务；如果端点以 `/api/v1/casts` 开头，则将请求路由到演员表服务

现在，需要在 `docker-compose.yml` 中添加 Nginx 服务。 在 `cast_db` 服务之后添加以下服务：

```dockerfile
nginx:
    image: nginx:latest
    ports:
      - "8080:8080"
    volumes:
      - ./nginx_config.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - cast_service
      - movie_service
```

现在，使用以下命令关闭容器：

```shell
docker-compose down
```

然后使用下面的命令再次重启服务：

```shell
docker-compose up -d
```

现在，可以在端口 8080 访问电影服务和演员表服务。 前往 `http://localhost:8080/api/v1/movies/` 以获取电影列表。

现在，你可能想知道如何访问服务的文档。 为此，请更新电影服务的 `main.py`，将

```python
app = FastAPI()
```

替换为：

```python
app = FastAPI(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")
```

类似的，将演员表服务中的

```python
app = FastAPI()
```

替换为：

```python
app = FastAPI(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")
```

在这里，更改了提供文档的端点以及提供 `openapi.json` 的位置。

现在，可以从 `http://localhost:8080/api/v1/movies/docs` 访问电影服务的文档，从 `http://localhost:8080/api/v1/casts/docs` 访问演员表服务的文档。

# 总结和下一步

微服务架构非常适合将大型单体应用程序分解为单独的业务逻辑，但这也带来了复杂性。 Python 非常适合构建微服务，因为有大量的包和框架，可以提高开发人员的工作效率。

多亏了 Docker，部署微服务变得更加容易。
更多信息，参见[如何使用 Docker 和 Docker Compose 开发微服务](https://aws.amazon.com/blogs/publicsector/how-to-develop-microservices-using-aws-cloud9-docker-and-docker-compose/)。

