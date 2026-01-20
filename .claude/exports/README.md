# Export Format Examples

This folder contains example exports from `dbt-conceptual` in all supported formats.

## Files

### 1. **example.png** (PNG Image)
- **Format**: Static raster image (captured from web UI canvas)
- **Use case**: Presentations, documentation, Slack/email, anywhere you need a visual diagram
- **Viewable**: Any image viewer
- **Editable**: No
- **Features**: Professional layout matching the interactive UI exactly - domain groupings, concept boxes, relationship arrows, status indicators

### 2. **coverage.html** (Coverage Dashboard)
- **Format**: Self-contained HTML dashboard
- **Use case**: View implementation coverage by domain and layer
- **Viewable**: Open in web browser
- **Editable**: No
- **Features**: Shows which concepts have implementing models in Silver/Gold layers, tracks completeness

### 3. **bus-matrix.html** (Kimball Bus Matrix)
- **Format**: Self-contained HTML matrix
- **Use case**: Dimensional modeling conformity analysis
- **Viewable**: Open in web browser
- **Editable**: No
- **Features**: Shows which dimensions are used by which facts (Kimball methodology), validates conformed dimensions

## How These Were Generated

All exports were generated from the sample conceptual model in `.claude/sample-project/`:

```bash
# PNG (screenshots the web UI canvas)
dbt-conceptual export --format png -o example.png

# Coverage Dashboard
dbt-conceptual export --format coverage -o coverage.html

# Bus Matrix
dbt-conceptual export --format bus-matrix -o bus-matrix.html
```

## Which Format Should I Use?

| Use Case | Best Format |
|----------|-------------|
| Visual diagrams for any purpose | PNG (`.png`) |
| Track implementation progress | Coverage Dashboard (`.html`) |
| Validate dimensional conformity | Bus Matrix (`.html`) |
| Presentations or slides | PNG (`.png`) |
| Quick sharing (Slack, email) | PNG (`.png`) |
| Documentation | PNG (`.png`) |

## Sample Conceptual Model

The examples use this simple e-commerce model:

- **Domains**: Party, Transaction, Catalog
- **Concepts**: Customer, Order, Product, Shipment
- **Relationships**:
  - Customer → places → Order (1:N)
  - Order → contains → Product (N:M)

## Why PNG?

The PNG export uses Playwright to screenshot the actual interactive web UI canvas. This ensures:
- **Visual consistency**: Exported diagrams look exactly like the interactive app
- **Professional appearance**: Proper layout, colors, and styling
- **Low maintenance**: One rendering engine (the frontend) for both interactive and static views
- **Automatic updates**: Visual improvements to the UI automatically improve PNG exports
