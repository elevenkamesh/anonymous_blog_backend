
python -m venv venv  ( for create the  virtual env )

.\venv\Scripts\Activate.ps1 (for activate it in windows )

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  ( if about not give access )

Uvicorn is a lightning-fast ASGI server (Asynchronous Server Gateway Interface) for Python 

For production, use:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

--host 0.0.0.0: Makes the server publicly accessible.
--port 8000: Specifies the port.
--workers 4: Runs multiple worker processes (for CPU-bound tasks).



uvicorn app.main:app --reload
