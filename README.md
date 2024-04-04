Project is in progress. Images and details may be outdated due to recent updates. *
  
<h1>Congress Trades Tracker</h1>
<p>
Congress Trades Tracker is a project that aims to make congressional stock trading more transparent. It utilizes an ELT pipeline to scrape, transform, and load data that can be accessed through an API, Streamlit dashboard, or front end website. 
</p>

<h2>Pipeline</h2>
<img src="./images/Congress Trades Pipeline Fargate.png">

<h2>DB Model</h2>
<img src="./images/db_model.png">

<h2>Tech Used</h2>
    <ul>
        <li>Python</li>
        <li>AWS</li>
        <li>Pandas</li>
        <li>DBT</li>
        <li>Flask</li>
        <li>PostgreSQL</li>
        <li>Pytest</li>
        <li>Prefect</li>
        <li>Selenium</li>
        <li>Beautiful Soup</li>
        <li>PyPDF</li>
        <li>React</li>
    </ul>

<h2>Optimizations/To Do List</h2>
    <ul>
        <li><s>Refactor SQL Alchemy into current API/ORM configuration</s></li>
        <li>Integrate trade tables in DBT and format stock/politician tables</li>
        <li>Add React Frontend</li>
        <li>Host Flask API on Cloud</li>
        <li>Adjust Senate scraper calendar dates to align with Prefect scraping schedule</li>
        <li>Additional tests for House and Senate adapters</li>
        <li><s>Integrate LLM (Hugging Face Model) into Streamlit dashboard</s>REVISE</li>
        <li><s>Add all PDF links for House trade reports to database</s></li>
    </ul>

<h2>Lessons Learned</h2>
    <ul>
        <li>Extracting table data from PDFs can be really hard</li>
        <li>Data Integrity is crucial to limiting edge cases</li>
    </ul>
