# UML-диаграммы бизнес-логики

Диаграммы написаны на Mermaid и отображаются в GitHub, GitLab, VS Code (расширение Markdown Preview Mermaid Support) и на сайте mermaid.live.

## 1. Диаграмма вариантов использования

```mermaid
flowchart LR
    R(["Читатель"])
    L(["Библиотекарь"])
    A(["Администратор"])

    subgraph IS["Информационная система библиотеки"]
        UC1("Поиск книги")
        UC2("Просмотр своих выдач")
        UC3("Регистрация читателя")
        UC4("Выдача книги")
        UC5("Приём возврата")
        UC6("Продление выдачи")
        UC7("Управление каталогом книг")
        UC8("Отчёт по просрочкам")
    end

    R --> UC1
    R --> UC2
    L --> UC1
    L --> UC3
    L --> UC4
    L --> UC5
    L --> UC6
    L --> UC2
    A --> UC7
    A --> UC8
```

## 2. Диаграмма классов

```mermaid
classDiagram
    class Book {
        +str isbn
        +str title
        +str author
        +int year
        +int total_copies
        +int available_copies
    }
    class Reader {
        +int reader_id
        +str full_name
        +str phone
        +bool is_blocked
    }
    class Loan {
        +int loan_id
        +date issued_at
        +date due_date
        +date returned_at
        +int renewals
        +is_overdue() bool
    }
    class BookCatalog {
        +add_book(book) None
        +find_by_isbn(isbn) Book
        +find_by_title(query) list
        +remove_book(isbn) None
    }
    class ReaderRegistry {
        +register(full_name, phone) Reader
        +get(reader_id) Reader
    }
    class LoanService {
        +issue_book(reader_id, isbn) Loan
        +return_book(loan_id) None
        +renew_loan(loan_id) Loan
        +list_overdue() list
    }

    BookCatalog "1" o-- "*" Book : содержит
    ReaderRegistry "1" o-- "*" Reader : содержит
    Loan "*" --> "1" Book : выдана книга
    Loan "*" --> "1" Reader : выдана читателю
    LoanService --> BookCatalog : использует
    LoanService --> ReaderRegistry : использует
    LoanService ..> Loan : создаёт
```

## 3. Диаграмма последовательности: выдача книги

```mermaid
sequenceDiagram
    actor Lib as Библиотекарь
    participant UI as Интерфейс
    participant LS as LoanService
    participant RR as ReaderRegistry
    participant BC as BookCatalog

    Lib->>UI: Выдать книгу (билет, ISBN)
    UI->>LS: issue_book(reader_id, isbn)
    LS->>RR: get(reader_id)
    RR-->>LS: Reader
    LS->>BC: find_by_isbn(isbn)
    BC-->>LS: Book
    alt читатель заблокирован, лимит 5 книг или нет экземпляров
        LS-->>UI: Отказ с указанием причины
        UI-->>Lib: Сообщение об ошибке
    else проверки пройдены
        LS->>LS: создать Loan, срок 14 дней
        LS->>BC: уменьшить available_copies
        LS-->>UI: Loan
        UI-->>Lib: Выдача оформлена
    end
```

## 4. Диаграмма состояний выдачи (Loan)

```mermaid
stateDiagram-v2
    state "Выдана" as Issued
    state "Продлена" as Renewed
    state "Просрочена" as Overdue
    state "Возвращена" as Returned

    [*] --> Issued : issue_book
    Issued --> Renewed : renew_loan (один раз)
    Issued --> Overdue : срок истёк
    Renewed --> Overdue : срок истёк
    Issued --> Returned : return_book
    Renewed --> Returned : return_book
    Overdue --> Returned : return_book
    Returned --> [*]
```
