# North Star Unified Shell App

**Version:** 1.0.0 Lite  
**Platform:** Small Business Decision Support Platform

## Overview

North Star Business Lab is a unified platform container designed to provide small businesses with professional-grade financial analysis and decision support tools. The Lite edition launches with **Financial Modeler Lite** as the core module, with a clean, expandable architecture ready for future growth.

## Features

### Current (Lite Mode)
- **💰 Financial Modeler Lite**: Core financial projection and scenario modeling
  - Revenue and cost modeling
  - Multi-month projections
  - Profit analysis and visualization
  - Automated insights and recommendations
  
- **Clean Platform Shell**: Professional UI with modular architecture
  - Top navigation bar with client/mode indicators
  - Left sidebar navigation
  - Bottom insights/status strip
  - Expandable module framework

### Coming Soon (Advisor Mode)
- 💵 Cash Flow / LOC Engine
- 📊 Valuation Engine
- 📋 Business Plan Builder
- 🎯 Change Readiness Assessment
- 🧠 Intelligence Layer (NSBI)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the repository**
   ```bash
   cd SB_Analyst_v1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - The app will automatically open in your default browser
   - Default URL: `http://localhost:8501`

## Project Structure

```
SB_Analyst_v1/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── src/
│   ├── config/
│   │   └── settings.py            # Application configuration
│   ├── state/
│   │   └── app_state.py           # Session state management
│   ├── ui/
│   │   ├── shell.py               # Main shell layout
│   │   ├── topbar.py              # Top navigation bar
│   │   ├── sidebar.py             # Left sidebar navigation
│   │   └── footer.py              # Bottom status strip
│   └── modules/
│       ├── financial_modeler_lite.py  # Financial Modeler Lite module
│       └── insights_panel.py          # Insights panel (placeholder)
└── docs/
    └── windsurf_reports/          # Build documentation
```

## Usage

### Financial Modeler Lite

1. **Navigate to Model Inputs tab**
   - Enter your current monthly revenue
   - Set expected growth rate
   - Configure cost structure (COGS, fixed costs, variable costs)
   - Select projection period

2. **Click "Run Financial Model"**
   - System generates projections based on your inputs

3. **View Analysis tab**
   - See revenue and profit projections
   - Review key metrics
   - Analyze detailed month-by-month breakdown

4. **Check Insights tab**
   - Review automated insights
   - Get recommendations based on your financial model
   - Identify areas for improvement

## Architecture

### Modular Design

The app is built with a clean separation of concerns:

- **Shell Layer** (`src/ui/`): Reusable UI components that form the platform container
- **Module Layer** (`src/modules/`): Individual business tools (Financial Modeler, etc.)
- **State Layer** (`src/state/`): Session state management
- **Config Layer** (`src/config/`): Centralized configuration

### Adding New Modules

To add a new module to the platform:

1. **Create module file** in `src/modules/your_module.py`
   ```python
   def render_your_module():
       st.markdown("## Your Module")
       # Module content here
   ```

2. **Import in app.py**
   ```python
   from src.modules.your_module import render_your_module
   ```

3. **Add to module router** in `render_main_content()`:
   ```python
   elif active_module == "Your Module":
       render_your_module()
   ```

4. **Update sidebar** in `src/ui/sidebar.py` to include navigation button

5. **Update settings** in `src/config/settings.py` to register the module

## Configuration

### App Settings

Edit `src/config/settings.py` to customize:
- App name and branding
- Available modules per mode
- Feature flags
- UI theme settings

### Streamlit Config

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Browser behavior

## Development

### Code Style
- Clean, readable code with docstrings
- Modular architecture
- Separation of concerns
- Professional naming conventions

### State Management
- Lightweight session state via `st.session_state`
- Centralized state functions in `app_state.py`
- No heavy persistence (future enhancement)

### UI Guidelines
- Clean, modern design
- Professional platform feel
- Consistent spacing and layout
- Subtle upgrade hints (not aggressive upselling)

## Roadmap

### Phase 1 (Current) - Lite Foundation
- ✅ Shell architecture
- ✅ Financial Modeler Lite
- ✅ Basic insights

### Phase 2 - Advisor Mode
- Cash Flow / LOC Engine
- Valuation Engine
- Business Plan Builder
- Mode switching

### Phase 3 - Intelligence Layer
- NSBI integration
- Advanced analytics
- Predictive insights
- Alert system

## Support

For questions or issues:
- Review this README
- Check `docs/windsurf_reports/` for build documentation
- Review code comments and docstrings

## License

Proprietary - North Star Business Intelligence

---

**North Star Business Lab** - Small Business Decision Support Platform  
*Version 1.0.0 Lite*
