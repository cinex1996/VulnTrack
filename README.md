# VulnTrack

Platforma do zarządzania zgłoszeniami podatności bezpieczeństwa. Umożliwia zespołom śledzenie, triażowanie i rozwiązywanie podatności w ramach projektów.

## Funkcjonalności

- Zgłaszanie podatności z poziomami krytyczności: `low`, `medium`, `high`, `critical`
- Cykl życia podatności ze statusami: `new → open → triaged → accepted/rejected → fixed → closed`
- Historia zmian statusów dla każdej podatności
- Komentarze do podatności
- Projekty grupujące podatności
- System powiadomień (nowy komentarz, zmiana statusu, nowa podatność, alert krytyczny)
- Role użytkowników z różnymi poziomami uprawnień

## Architektura

Projekt składa się z 4 aplikacji Django:

| Aplikacja | Odpowiedzialność |
|---|---|
| `accounts` | Rejestracja, logowanie, model użytkownika z rolami |
| `vulnerabilities` | Zgłaszanie, edycja, usuwanie podatności, komentarze, historia statusów |
| `projects` | Zarządzanie projektami grupującymi podatności |
| `notifications` | Tworzenie i wyświetlanie powiadomień dla użytkowników |

## Role użytkowników

| Rola | Uprawnienia |
|---|---|
| **Researcher** | Zgłasza podatności, edytuje własne zgłoszenia, dodaje komentarze |
| **Moderator** | Jak Researcher + zmiana statusu dowolnej podatności |
| **Admin** | Pełny dostęp + usuwanie podatności (panel `/admin/`) |

Role przypisywane są przez administratora w panelu Django Admin lub przy tworzeniu konta przez superusera.

## Wymagania

- Python 3.13
- Django 6.0.4
- django-environ 0.13.0

## Setup lokalny

```bash
git clone <repo-url>
cd VulnTrackAdmin

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Utwórz plik `.env` w katalogu głównym projektu:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Uruchom migracje i utwórz superusera:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Aplikacja dostępna pod adresem `http://127.0.0.1:8000/`.

## Testy i CI

```bash
python manage.py test
```

Testy uruchamiane automatycznie przez GitHub Actions przy każdym push/PR do gałęzi `main`.
