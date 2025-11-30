#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
```

**FILE 14:** `advanced_api_project/README.md` (same content as before)

---

## 🎯 CORRECTED File Structure:
```
advanced_api_project/              ← UNDERSCORES not hyphens!
├── manage.py
├── README.md
├── advanced_api_project/          ← UNDERSCORES!
│   ├── __init__.py
│   ├── settings.py               ← This is what checker looks for
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py                  ← Author and Book models
    ├── serializers.py             ← BookSerializer and AuthorSerializer
    ├── admin.py
    ├── apps.py
    ├── views.py
    └── tests.py
