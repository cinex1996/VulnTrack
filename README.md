# VulnTrack

Platforma do zarządzania zgłoszeniami podatności (Vulnerability Management System) zbudowana w Django.

## Funkcjonalności

- Zgłaszanie podatności z poziomem ważności (low / medium / high / critical)
- Śledzenie statusu podatności (new → triaged → accepted → fixed / rejected / closed)
- System ról: **Researcher** (zgłasza), **Moderator** (zmienia statusy), **Admin** (usuwa)
- Historia zmian statusu przy każdym zgłoszeniu
- System powiadomień — komentarz i zmiana statusu trafiają do zgłaszającego
- Panel ze statystykami (wszystkie / krytyczne / naprawione / otwarte)
- Komentarze do zgłoszeń

## Technologie

- Python 3.13 / Django 6.0
- SQLite (dev) / PostgreSQL (prod)
- Bootstrap 5.3

## Uruchomienie lokalne

```bash
# 1. Sklonuj repozytorium
git clone <url>
cd VulnTrackAdmin

# 2. Utwórz i aktywuj środowisko wirtualne
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Skonfiguruj zmienne środowiskowe
cp .env.example .env             # uzupełnij SECRET_KEY i DEBUG

# 5. Wykonaj migracje i utwórz superusera
python manage.py migrate
python manage.py createsuperuser

# 6. Uruchom serwer deweloperski
python manage.py runserver
```

Aplikacja dostępna pod adresem: http://127.0.0.1:8000

## Zmienne środowiskowe (`.env`)

| Zmienna | Opis | Przykład |
|---|---|---|
| `SECRET_KEY` | Klucz Django | `django-insecure-...` |
| `DEBUG` | Tryb debugowania | `True` |
| `DATABASE_URL` | Adres bazy danych (opcjonalne) | `postgres://user:pass@host/db` |

## Uruchomienie z PostgreSQL

Odkomentuj `psycopg2-binary` w `requirements.txt`, zainstaluj i dodaj do `.env`:

```
DATABASE_URL=postgres://user:password@localhost:5432/vulntrack
```

## Uruchomienie testów

```bash
python manage.py test
```

## Struktura projektu

```
VulnTrackAdmin/
├── accounts/          # Rejestracja, logowanie, model użytkownika
├── vulnerabilities/   # Zgłoszenia podatności, komentarze, historia
├── notifications/     # System powiadomień
├── projects/          # Projekty (powiązanie z podatnościami)
└── templates/         # Bazowy szablon HTML
```

## Role użytkowników

| Rola | Zgłaszanie | Zmiana statusu | Usuwanie |
|---|---|---|---|
| Researcher | ✅ | ❌ | ❌ |
| Moderator | ✅ | ✅ | ✅ |
| Admin | ✅ | ✅ | ✅ |

Role nadawane są przez panel administracyjny Django (`/admin/`).
