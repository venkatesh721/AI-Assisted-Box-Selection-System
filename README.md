# AI-Assisted Box Selection System

Repository URL: [https://github.com/venkatesh721/AI-Assisted-Box-Selection-System](https://github.com/venkatesh721/AI-Assisted-Box-Selection-System)

## Overview

This Django and Django REST Framework API recommends a shipping box for an ecommerce order. It considers product dimensions, product weight, box internal dimensions, box maximum weight, and box cost.

## Features

- Product, shipping-box, and order APIs.
- Nested order creation with product quantities.
- Decimal-based measurements and currency; floating-point values are not used.
- Rotation-aware dimension checking.
- Deterministic, cost-first box recommendation.
- Automated unit and API tests.

## Assumptions and packing limitation

This application uses a deterministic **single-row packing** simplification; it is **not** a complete general-purpose 3D bin-packing engine.

For each candidate box, every physical product unit is placed in one row along one of the box's three internal axes. A product may be rotated. Its two remaining dimensions must fit in the cross-section, and the sum of the dimensions along the row axis must fit in the box. This is a sufficient rule: an accepted result is physically feasible under this layout, but some boxes that could work with more sophisticated three-dimensional packing may be rejected.

## Technology stack

- Python 3.12 (CI); Django 5.2; Django REST Framework 3.17
- SQLite for local development
- GitHub Actions for continuous integration

## Project structure

```text
config/              Django project settings and root URLs
packaging/           Models, API, service layer, and tests
packaging/services.py  Pure selection logic
.github/workflows/   GitHub Actions configuration
```

## Setup

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Environment variables

Copy `.env.example` as a reference and set environment variables in your shell or deployment configuration. `DJANGO_SECRET_KEY` should always be changed in production. `DJANGO_DEBUG` defaults to `True` only for local development.

## Database setup and migrations

```bash
python manage.py migrate
```

## Running the server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

## Running tests

```bash
python manage.py check
python manage.py test -v 2
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET, POST | `/api/products/` | List or create products |
| GET, PATCH, DELETE | `/api/products/{id}/` | Manage a product |
| GET, POST | `/api/boxes/` | List or create shipping boxes |
| GET, PATCH, DELETE | `/api/boxes/{id}/` | Manage a shipping box |
| GET, POST | `/api/orders/` | List or create orders with items |
| GET | `/api/orders/{id}/` | Retrieve one order |
| POST | `/api/orders/{id}/recommend-box/` | Get a box recommendation |

## Example requests and responses

Create a product:

```json
POST /api/products/
{
  "name": "Coffee mug",
  "length": "10.000",
  "width": "8.000",
  "height": "9.000",
  "weight": "0.350"
}
```

Create an order:

```json
POST /api/orders/
{
  "reference": "WEB-1001",
  "order_items": [{"product_id": 1, "quantity": 2}]
}
```

The recommendation endpoint returns the selected box, total weight and volume, unused volume, and the packing axis. If no box qualifies, it returns HTTP 422 with a clear JSON message.

## Box-selection algorithm

1. Expand each order item by quantity.
2. Calculate total weight and total product volume.
3. Reject a box if total weight exceeds its maximum weight or total volume exceeds its internal volume.
4. For every remaining box, try each of its three possible row axes.
5. For each product unit, test every unique orientation and choose the valid orientation needing the least row-axis length.
6. Accept an axis when the sum of those lengths is within the box axis length.
7. Rank fitting boxes by lowest cost, then lowest unused volume, then lowest database ID.

Exact equality is accepted for both capacity and required packing length.

## Rotation/orientation handling

Each product is tested in all unique permutations of `(length, width, height)`. For example, a `2 × 3 × 4` product may fit a `4 × 2 × 3` box after rotation, even when its original orientation would not fit.

## Multiple-product packing simplification

Products are not assumed to fit merely because their total volume fits. The single-row rule checks a concrete non-overlapping arrangement. It deliberately avoids claiming to solve arbitrary 3D packing.

## Error handling

- Invalid dimensions, weights, cost, or quantity return HTTP 400.
- Duplicate products in an order-create payload return HTTP 400.
- Unknown resources return HTTP 404.
- A valid order for which no box fits returns HTTP 422.
- An order with no items returns HTTP 400 when recommendation is requested.

## Test evidence

Run output from the verified local test suite is stored in `TEST_OUTPUT.md`. GitHub Actions runs the same checks for pushes and pull requests to `main`.

## AI usage documentation

`AI_USAGE.md` must be written by the submitter and must contain only real AI-tool usage, prompts, accepted or rejected output, mistakes, and verification performed. It is intentionally not generated by this project.

## Submission notes

The assignment-required exported chat transcript and the personal “What did you learn in this assignment?” response must be written and added manually by the submitter because the assignment prohibits AI-generated versions.
