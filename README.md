# Route tracing

Simple route tracing programm that use Scapy library.

Этот код реализует утилиту трассировки маршрута (traceroute) на Python с использованием библиотеки scapy.

**1. Импорт библиотек:**

```python
from scapy.all import *
import sys
import time
import argparse
```

- `scapy.all`: Библиотека для работы с сетевыми пакетами.
- `sys`: Предоставляет доступ к некоторым переменным и функциям, взаимодействующим с интерпретатором Python.
- `time`: Предоставляет функции для работы со временем.
- `argparse`: Модуль для удобного разбора аргументов командной строки.

**2. Функция parser():**

```python
def parser():
    p = argparse.ArgumentParser(description="Ping the target IP with custom settings.")
    p.add_argument("target_ip", help="The IP address of destination.")
    p.add_argument("-p", "--protocol", default="I", help="Network protocol (default: ICMP).")
    p.add_argument("-m", "--max_hops", default=30, help="Maximum number of hops (default: 30).", type=int)
    p.add_argument("-t", "--timeout", default=2, help="Timeout in seconds (default: 2.0).", type=int)
    p.add_argument("-v", "--verbose", default=False, help="Verbose mode (default: False).")

    args = p.parse_args()
    return (args.protocol, args.target_ip, args.max_hops, args.timeout, args.verbose)
```

- Эта функция отвечает за разбор аргументов, переданных при запуске скрипта.
- `argparse.ArgumentParser()` создает объект парсера аргументов.
- `p.add_argument()`: Добавляет описание ожидаемых аргументов:
    - "`target_ip`": Обязательный аргумент - IP-адрес назначения.
    - "`-p`", "`--protocol`": Протокол (по умолчанию ICMP).
    - "`-m`", "`--max_hops`": Максимальное количество прыжков (по умолчанию 30).
    - "`-t`", "`--timeout`": Время ожидания ответа в секундах (по умолчанию 2).
    - "`-v`", "`--verbose`": Включение подробного режима (по умолчанию выключен).
- `p.parse_args()`: Производит разбор аргументов командной строки.
- Функция возвращает кортеж с разобранными аргументами.

**3. Функции udp(), tcp(), icmp():**

```python
def udp(target_ip, max_hops, timeout, verbose):
    # ...
def tcp(target_ip, max_hops, timeout, verbose):
    # ...
def icmp(target_ip, max_hops, timeout, verbose, icmp_id=random.randint(0, 65535)):
    # ...
```

- Эти функции реализуют отправку и прием пакетов по протоколам UDP, TCP и ICMP соответственно.
- Каждая функция принимает следующие аргументы:
    - `target_ip`: IP-адрес назначения.
    - `max_hops`: Максимальное количество прыжков.
    - `timeout`: Время ожидания ответа.
    - `verbose`: Флаг подробного режима.
- Функции формируют пакет соответствующего протокола, отправляют его с помощью `sr1()` (отправка и получение одного пакета) и анализируют ответ.
- В случае успеха возвращают строку с информацией о прыжке (номер прыжка, IP-адрес, имя хоста, время ответа) и IP-адрес.
- В случае ошибки возвращают строку с описанием ошибки и None.

**4. Словарь PROTOCOLS:**

```python
PROTOCOLS  = {
    "U": udp,
    "T": tcp,
    "I": icmp
}
```

- Словарь, связывающий буквенные обозначения протоколов с соответствующими функциями.

**5. Основной блок кода (if __name__ == "__main__":)**:

```python
if __name__ == "__main__":
    args = parser()
    protocol, target, max_hops, timeout, verbose = PROTOCOLS[args[0]], *args[1:]
    target_ip = socket.gethostbyname(target)

    print(f"Tracing route to {target} ({target_ip}) with a maximum of {max_hops} hops:")
    for mh in range(1, max_hops+1):
        res = protocol(target_ip, mh, timeout, verbose)
        print(res[0])
        if res[1] == target_ip:
            print("  \tAddress reached!")
            break
```

- `if __name__ == "__main__"`: Код внутри этого блока выполнится только при запуске скрипта напрямую, а не при импорте как модуля.
- `args = parser()`: Вызов функции `parser()` для разбора аргументов командной строки.
- `protocol, target, ... = PROTOCOLS[args[0]], *args[1:]`: Получение функции, соответствующей выбранному протоколу, и остальных аргументов.
- `target_ip = socket.gethostbyname(target)`: Получение IP-адреса по имени хоста.
- Цикл `for mh in range(1, max_hops+1)`: Итерация по количеству прыжков от 1 до `max_hops`.
- Внутри цикла:
    - `res = protocol(target_ip, mh, timeout, verbose)`: Вызов функции, соответствующей выбранному протоколу, для отправки пакета.
    - `print(res[0])`: Вывод информации о прыжке.
    - `if res[1] == target_ip`: Если IP-адрес прыжка совпадает с адресом назначения, то завершаем цикл, так как маршрут построен.

