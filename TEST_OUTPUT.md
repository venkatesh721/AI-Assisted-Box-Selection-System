# Local test run output

Command run:

```text
python manage.py check
python manage.py test -v 2
```

Actual output excerpt from local verification (repetitive built-in migration lines omitted):

```text
System check identified no issues (0 silenced).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Found 26 test(s).
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles
  Apply all migrations: admin, auth, contenttypes, packaging, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying packaging.0001_initial... OK
  Applying packaging.0002_alter_product_height_alter_product_length_and_more... OK
  Applying sessions.0001_initial... OK
test_create_and_read_box ... ok
test_create_and_read_product ... ok
test_create_order_with_nested_items ... ok
test_invalid_payload_and_duplicate_product_return_400 ... ok
test_recommendation_endpoint_returns_best_box ... ok
test_recommendation_returns_422_when_nothing_fits ... ok
test_unknown_order_returns_404 ... ok
test_box_rejects_invalid_measurements_and_cost ... ok
test_decimal_values_are_preserved ... ok
test_order_item_rejects_zero_quantity ... ok
test_product_rejects_zero_or_negative_measurements ... ok
test_empty_order_raises_clear_error ... ok
test_equal_candidates_fall_back_to_id ... ok
test_equal_cost_uses_lower_unused_volume ... ok
test_lowest_cost_box_wins ... ok
test_multiple_products_exceed_single_row_length ... ok
test_multiple_products_fit_in_single_row ... ok
test_no_suitable_box_returns_none ... ok
test_product_can_fit_only_after_rotation ... ok
test_product_that_cannot_fit_any_orientation_is_rejected ... ok
test_single_product_fits_without_rotation ... ok
test_unique_orientations_deduplicates_repeated_dimensions ... ok
test_unit_that_cannot_fit_cross_section_rejects_box ... ok
test_volume_over_box_volume_is_rejected ... ok
test_weight_equal_to_capacity_is_accepted ... ok
test_weight_over_capacity_is_rejected ... ok

----------------------------------------------------------------------
Ran 26 tests in 0.043s

OK
Destroying test database for alias 'default'...
System check identified no issues (0 silenced).
```
