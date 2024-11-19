# Automated Data Collection for Impact Startups in CEE

This project is a **Flask-based web application** designed to automate the collection, processing, and presentation of news and updates related to **impact startups** in the **Central and Eastern Europe (CEE)** region. It leverages external APIs such as **NewsAPI** and **Crunchbase API** to gather relevant data about startups, investors, funding rounds, and associated sources.

## Features

### 1. **Automated Data Collection**
- **NewsAPI Integration**:
  - Scrapes news articles to detect startup activities, funding rounds, and related updates.
  - Filters information by keywords like *funding*, *venture capital*, *Series A*, and similar phrases.
  - Supports both **Czech** and **English** language spaces.
- **Crunchbase API Integration**:
  - Fetches detailed startup and investor data.
  - Gathers funding round details and associated sources.

### 2. **Data Processing**
- Identifies relevant information such as:
  - Startup names, founders, funding amounts, and investors.
  - Industry sectors and geographical focus (broader CEE region).
  - Tags for impact-driven areas like healthtech, medtech, energy, and sustainability.
- Formats the data into structured JSON outputs for seamless integration into external systems.

### 3. **Endpoints**
The project provides several RESTful endpoints to access the collected and processed data.
