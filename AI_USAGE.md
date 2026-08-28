# AI Usage Disclosure

## AI tool used

- OpenAI Codex (an AI coding assistant), used through an interactive chat and local workspace session.

## Prompts and tasks given to the AI

The AI was asked to:

1. Analyse the Django hiring assignment and propose a practical, maintainable implementation plan before writing code.
2. Implement a Django + Django REST Framework application called `AI-Assisted Box Selection System`.
3. Use SQLite, Django models for products, boxes, orders, and order items, and a service layer for box selection.
4. Implement rotation-aware product fitting and a documented single-row simplification for multi-product packing instead of claiming full 3D bin packing.
5. Add API endpoints, validation, migrations, tests, README documentation, GitHub Actions CI, and real local test output.
6. Verify migrations, Django checks, tests, Git status, and the GitHub Actions workflow.

## Output accepted

The following AI-assisted output was reviewed and kept in the repository:

- Django project configuration and the `packaging` app.
- Product, `ShippingBox`, `Order`, and `OrderItem` models with decimal fields, validation, and database constraints.
- A deterministic box-selection service that checks all unique product orientations, weight capacity, total volume, and the documented single-row packing rule.
- Django REST Framework serializers, viewsets, API routes, and the order recommendation endpoint.
- Unit tests and API tests covering validation, rotation, weight, volume, row packing, ranking, API errors, and no-fit scenarios.
- README, GitHub Actions CI workflow, `.env.example`, and `TEST_OUTPUT.md`.

## Output rejected or modified

- The initial settings used a fixed development fallback string for Django's secret key. It was changed to generate a temporary local key when `DJANGO_SECRET_KEY` is not supplied, so no secret is hardcoded in the repository.
- The initial decimal validator used a Python float (`0.001`). Django REST Framework produced a warning. It was changed to `Decimal("0.001")`, and the tests were run again without that warning.
- A follow-up migration (`0002`) was created after the validator change and committed to keep model definitions and migrations synchronized.

## AI mistakes or limitations found

- The float-based validator created a Django REST Framework warning; it was fixed as described above.
- The AI cannot determine a warehouse's real packing policy. The repository therefore documents a conservative, deterministic single-row packing rule rather than incorrectly claiming to solve arbitrary 3D bin packing.
- The AI was not used to create the required personal learning response or an artificial chat transcript.

## Verification performed

The following commands were run locally after implementation:

```powershell
python manage.py makemigrations --check --dry-run
python manage.py check
python manage.py migrate --noinput
python manage.py test -v 2
git diff --check
```

Results:

- No model changes were missing from migrations.
- Django system checks passed.
- Database migrations applied successfully.
- All 26 tests passed.
- GitHub Actions CI also completed successfully for the pushed repository.

## Submitter review

This document records the actual AI-assisted development activity for this repository. The submitter should review it, correct anything that does not match their own process, and keep it truthful before submission.
