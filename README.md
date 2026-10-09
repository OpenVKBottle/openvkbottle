<p align="center">
  <a href="https://github.com/cynexeso/openvkbottle">
    <img width="150px" height="150px" alt="openvkbottle" src="https://raw.githubusercontent.com/cynexeso/openvkbottle/master/docs/logo.svg">
  </a>
</p>
<h1 align="center">
  openvkbottle
</h1>
<p align="center">
    <em><b>Кастомизируемый, быстрый и удобный фреймворк для работы с OpenVK API</b></em>
</p>
<p align="center">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/cynexeso/openvkbottle/push-build.yml">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/openvkbottle">
  <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/cynexeso/openvkbottle/bug">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/openvkbottle?color=green&label=PyPI">
</p>

> OpenVKBottle - форк [VKBottle](https://github.com/vkbottle/vkbottle), адаптированный для работы с OpenVK.
> Основная цель проекта - упростить перенос существующих проектов с VKBottle на OpenVK с минимальными изменениями кода.
>
> OpenVKBottle не является официальным проектом VKCOM или оригинальных разработчиков VKBottle.
>
> API OpenVK может отличаться от VK API. Поэтому совместимость с оригинальным VKBottle не гарантируется во всех сценариях.

## Hello World

```python
from openvkbottle.user import User

bot = User("access_token")


@bot.on.message()
async def handler(_) -> str:
    return "Hello, World!"


bot.run()
````

Обратите внимание: для работы с OpenVK используются подходящие для OpenVK токены и методы API. Возможности авторизации и запуска бота зависят от используемого режима API.

[Смотреть больше примеров!](https://github.com/vkbottle/vkbottle/tree/master/examples)

## Документация

Поскольку OpenVKBottle сохраняет структуру и подходы оригинального VKBottle, большая часть документации остаётся актуальной.

[Туториал для новичков](https://vkbottle.rtfd.io/ru/latest/tutorial/)\
[Техническая документация](https://vkbottle.rtfd.io/ru/latest)

Документация написана для оригинального VKBottle. При её использовании учитывайте различия между VK API и OpenVK API, а также возможные отличия в поддерживаемых методах и типах.

## Установка

Установить последнюю опубликованную версию можно командой:

```console
pip install openvkbottle
```

## Отличия от VKBottle

OpenVKBottle стремится сохранить знакомый интерфейс VKBottle, чтобы существующие проекты можно было адаптировать с минимальными изменениями.

В простых случаях переход может сводиться к замене импортов:

```python
from vkbottle.user import User
```

на:

```python
from openvkbottle.user import User
```

Однако одной замены импортов может быть недостаточно: некоторые методы, типы, параметры запросов и механизмы API могут отличаться в OpenVK.

## Происхождение проекта

OpenVKBottle основан на [VKBottle](https://github.com/vkbottle/vkbottle). Проект сохраняет исходную структуру и подходы там, где они совместимы с OpenVK, и адаптирует необходимые компоненты для работы с OpenVK API.

## Contributing

ПР приветствуются! Перед созданием pull request ознакомьтесь с [CONTRIBUTION_GUIDE](CONTRIBUTION_GUIDE.md). Нам приятно видеть ваш вклад в развитие фреймворка.

Сообщайте об ошибках и задавайте вопросы в разделе [Issues](https://github.com/openvkbottle/openvkbottle/issues).

[Контрибьютеры](https://github.com/openvkbottle/openvkbottle/graphs/contributors)

## Лицензия

OpenVKBottle распространяется по лицензии [MIT](LICENSE).

Проект основан на VKBottle. Уведомления об авторских правах оригинальных авторов сохранены в файле LICENSE.
