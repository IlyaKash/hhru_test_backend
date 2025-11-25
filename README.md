# Lead Distribution CRM

Мини-CRM система для автоматического распределения лидов между операторами с учетом весов операторов по источникам и их текущей нагрузки.

### Запуск с Docker (рекомендуется)

# Сборка и запуск
```docker-compose up --build```

# Запуск в фоновом режиме
```docker-compose up -d```

# Остановка
```docker-compose down```

Доступ к приложению: [http://localhost:8000](http://localhost:8000)
Документация OpenAPI [http://localhost:8000/docs](http://localhost:8000/docs)


## Модели данных
Operator - оператор

id, name, is_active, max_load

Связи: Lead (one-to-many), OperatorCompetence (one-to-many)

Source - источник/бот

id, name

Связи: OperatorCompetence (one-to-many), Contact (one-to-many)

Lead - лид (клиент)

id, external_id, phone, email, operator_id

Связи: Contact (one-to-many), Operator (many-to-one)

Contact - обращение/контакт

id, lead_id, source_id, operator_id, created_at, message

Связывает Lead, Source и Operator

OperatorCompetence - компетенция оператора

id, operator_id, source_id, weight

Связывает Operator и Source с указанием веса

## Алгоритм распределения
Идентификация лидов
Лиды идентифицируются по приоритету:

external_id - внешний идентификатор

phone - телефон

email - email

Если лид не найден - создается новый.

Выбор оператора
Фильтрация доступных операторов:

Оператор активен (is_active = True)

Текущая нагрузка < максимальной (current_load < max_load)

Назначен на источник с весом > 0

Распределение по весам:

Используется вероятностный выбор с учетом весов

Вероятность = вес оператора / сумма весов

Учет нагрузки
Нагрузка оператора = количество активных обращений (Contact)

При достижении max_load оператор исключается из распределения

Нагрузка обновляется в реальном времени

Обработка edge cases
Нет доступных операторов - обращение создается без назначения оператора

Нет компетенций для источника - возвращается ошибка 400

Дубликаты лидов - автоматическое объединение по идентификаторам
